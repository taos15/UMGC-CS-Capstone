import {afterEach, beforeEach, expect, test, vi} from 'vitest';
import {apiRequest} from './client';
import {setSession, clearSession} from '../features/auth/session';

beforeEach(() => {
  setSession({access_token: 'test-token', token_type: 'bearer', expires_in: 900});
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('[]')));
});
afterEach(() => {clearSession(); vi.unstubAllEnvs(); vi.unstubAllGlobals();});

test('uses same-origin canonical base by default', async () => {
  vi.stubEnv('VITE_API_BASE_URL', '');
  await apiRequest('/jobs');
  expect(fetch.mock.calls[0][0]).toBe('/api/v1/jobs');
});

for (const base of ['https://api.example.test/api/v1/', '/gateway/api/v1/']) {
  test(`uses configured base ${base} for authenticated requests`, async () => {
    vi.stubEnv('VITE_API_BASE_URL', base);
    await apiRequest('/jobs');
    expect(fetch.mock.calls[0][0]).toBe(`${base.replace(/\/$/, '')}/jobs`);
    expect(fetch.mock.calls[0][1].headers.get('Authorization')).toBe('Bearer test-token');
  });
}

for (const base of ['//untrusted.test', 'javascript:alert(1)', 'https://user:secret@api.test/api/v1', 'https://api.test/api/v1?token=secret']) {
  test(`invalid configuration is rejected before sending credentials: ${base}`, async () => {
    vi.stubEnv('VITE_API_BASE_URL', base);
    await expect(apiRequest('/jobs')).rejects.toMatchObject({code: 'API_CONFIGURATION_ERROR'});
    expect(fetch).not.toHaveBeenCalled();
  });
}

for (const body of [null, [], 'private failure', {code: 'DATABASE_UNAVAILABLE', detail: 'private SQL', field_errors: [null, {field: 'body.top_k', code: 'greater_than', message: 'private validation context'}]}]) {
  test(`problem parsing tolerates ${JSON.stringify(body)} without exposing internals`, async () => {
    fetch.mockResolvedValue(new Response(JSON.stringify(body), {status: 503, headers: {'X-Request-ID': 'trace-123'}}));
    try {await apiRequest('/jobs'); expect.unreachable();}
    catch (error) {expect(error.status).toBe(503); expect(error.requestId).toBe('trace-123'); expect(error.message).not.toContain('private');}
  });
}

test('an expired token is removed before the request is sent', async () => {
  vi.useFakeTimers();
  try {
    setSession({access_token: 'expired-token', token_type: 'bearer', expires_in: 1});
    vi.advanceTimersByTime(1001);
    await apiRequest('/jobs');
    expect(fetch.mock.calls[0][1].headers.has('Authorization')).toBe(false);
    expect(sessionStorage.getItem('skillmatch.session')).toBeNull();
  } finally {vi.useRealTimers();}
});

test('a delayed 401 for an old token preserves a newly signed-in session', async () => {
  let complete;
  fetch.mockImplementationOnce(() => new Promise(resolve => {complete = resolve;}));
  const pending = apiRequest('/jobs');
  setSession({access_token: 'replacement-token', token_type: 'bearer', expires_in: 900});
  complete(new Response(JSON.stringify({code: 'AUTH_REQUIRED'}), {status: 401}));
  await expect(pending).rejects.toMatchObject({status: 401, code: 'AUTH_REQUIRED'});
  await apiRequest('/jobs');
  expect(fetch.mock.calls[1][1].headers.get('Authorization')).toBe('Bearer replacement-token');
});

test('public login failure does not clear an existing bearer session', async () => {
  fetch.mockResolvedValueOnce(new Response('{}', {status: 401}));
  await expect(apiRequest('/auth/login', {method: 'POST', auth: false, body: {username: 'unknown', password: 'wrong'}})).rejects.toMatchObject({status: 401});
  expect(fetch.mock.calls[0][1].headers.has('Authorization')).toBe(false);
  await apiRequest('/jobs');
  expect(fetch.mock.calls[1][1].headers.get('Authorization')).toBe('Bearer test-token');
});

test('non-JSON gateway errors retain status and header correlation', async () => {
  fetch.mockResolvedValue(new Response('<html>private gateway failure</html>', {status: 502, headers: {'X-Request-ID': 'gateway-42'}}));
  await expect(apiRequest('/jobs')).rejects.toMatchObject({status: 502, code: 'HTTP_ERROR', requestId: 'gateway-42'});
});

test('204 deletion responses do not attempt JSON parsing', async () => {
  fetch.mockResolvedValue(new Response(null, {status: 204}));
  await expect(apiRequest('/jobs/job-1', {method: 'DELETE', body: {version: 2}})).resolves.toBeNull();
});
