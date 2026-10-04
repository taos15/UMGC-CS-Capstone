import { clearSession, getToken } from '../features/auth/session';

export class ApiError extends Error {
  constructor(status, code) {
    super('The request could not be completed.');
    this.status = status;
    this.code = code;
  }
}

export async function apiRequest(path, { method = 'GET', body, auth = true, signal } = {}) {
  // Only same-origin API paths; never forward credentials to arbitrary URLs.
  if (!/^\/[a-zA-Z0-9_/-]*(?:\?[^#]*)?$/.test(path) || path.startsWith('//')) {
    throw new Error('Use a relative API path');
  }
  const token = auth ? getToken() : null;
  const headers = new Headers({ Accept: 'application/json, application/problem+json' });
  if (body !== undefined) headers.set('Content-Type', 'application/json');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  let response;
  try {
    response = await fetch(`/api/v1${path}`, {
      method, headers, body: body === undefined ? undefined : JSON.stringify(body),
      credentials: 'omit', signal,
    });
  } catch {
    throw new ApiError(0, 'NETWORK_ERROR');
  }
  if (!response.ok) {
    if (response.status === 401 && auth && token && token === getToken()) clearSession();
    const problem = await response.json().catch(() => ({}));
    throw new ApiError(response.status, problem.code || 'HTTP_ERROR');
  }
  if (response.status === 204) return null;
  return response.json();
}
