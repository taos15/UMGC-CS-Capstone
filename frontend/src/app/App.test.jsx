import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, afterEach, expect, test, vi } from 'vitest';
import App from './App';
import { clearSession, setSession } from '../features/auth/session';
import { apiRequest } from '../api/client';

const reply = (body, status = 200) => new Response(JSON.stringify(body), { status });
const loginReply = () => reply({ access_token: 'test-token', token_type: 'bearer', expires_in: 900 });
beforeEach(() => { clearSession(); vi.stubGlobal('fetch', vi.fn()); });
afterEach(() => { clearSession(); vi.unstubAllGlobals(); vi.useRealTimers(); });

async function submitLogin() {
  const user = userEvent.setup();
  await user.type(screen.getByLabelText('Username'), 'test-user');
  await user.type(screen.getByLabelText('Password'), 'test-password');
  await user.click(screen.getByRole('button', { name: 'Sign in' }));
  return user;
}

test('login stores token, clears password, and authenticates subsequent requests', async () => {
  fetch.mockResolvedValueOnce(loginReply()).mockResolvedValueOnce(reply([]));
  render(<App />);
  await submitLogin();
  expect(await screen.findByRole('heading', { name: 'You’re signed in' })).toBeVisible();
  expect(fetch.mock.calls[0][0]).toBe('/api/v1/auth/login');
  expect(fetch.mock.calls[0][1].headers.has('Authorization')).toBe(false);
  expect(sessionStorage.getItem('skillmatch.session')).not.toContain('test-password');
  await apiRequest('/employees');
  expect(fetch.mock.calls[1][1].headers.get('Authorization')).toBe('Bearer test-token');
  await userEvent.click(screen.getByRole('button', { name: 'Sign out' }));
  expect(screen.getByLabelText('Password')).toHaveValue('');
  expect(sessionStorage.getItem('skillmatch.session')).toBeNull();
});

test('invalid credentials display generic messaging and never save a token', async () => {
  fetch.mockResolvedValue(reply({ code: 'AUTH_INVALID_CREDENTIALS', detail: 'private server detail' }, 401));
  render(<App />);
  await submitLogin();
  expect(await screen.findByRole('alert')).toHaveTextContent('Invalid username or password.');
  expect(screen.queryByText('private server detail')).not.toBeInTheDocument();
  expect(sessionStorage.getItem('skillmatch.session')).toBeNull();
  expect(screen.getByLabelText('Password')).toHaveValue('');
});

test('network failure provides retry messaging', async () => {
  fetch.mockRejectedValue(new Error('private network detail'));
  render(<App />);
  await submitLogin();
  expect(await screen.findByRole('alert')).toHaveTextContent('Unable to sign in. Please try again.');
});

test('expired or rejected sessions return to login', async () => {
  setSession({ access_token: 'test-token', token_type: 'bearer', expires_in: 900 });
  fetch.mockResolvedValue(reply({ code: 'AUTH_REQUIRED' }, 401));
  render(<App />);
  await expect(apiRequest('/employees')).rejects.toMatchObject({ status: 401 });
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeVisible();
  expect(sessionStorage.getItem('skillmatch.session')).toBeNull();
});

test('session timer clears authentication without a request', async () => {
  vi.useFakeTimers();
  setSession({ access_token: 'test-token', token_type: 'bearer', expires_in: 1 });
  render(<App />);
  const { act } = await import('@testing-library/react');
  await act(async () => { vi.advanceTimersByTime(1100); });
  expect(screen.getByLabelText('Username')).toBeVisible();
});

test('forbidden response does not log out a valid session', async () => {
  setSession({ access_token: 'test-token', token_type: 'bearer', expires_in: 900 });
  fetch.mockResolvedValue(reply({ code: 'FORBIDDEN' }, 403));
  await expect(apiRequest('/employees')).rejects.toMatchObject({ status: 403 });
  expect(sessionStorage.getItem('skillmatch.session')).not.toBeNull();
});

test('API client rejects external URLs before sending a token', async () => {
  setSession({ access_token: 'test-token', token_type: 'bearer', expires_in: 900 });
  await expect(apiRequest('//example.com')).rejects.toThrow();
  expect(fetch).not.toHaveBeenCalled();
});

test('pending login prevents duplicate submission', async () => {
  let complete;
  fetch.mockImplementation(() => new Promise(resolve => { complete = resolve; }));
  render(<App />);
  await submitLogin();
  const button = screen.getByRole('button', { name: 'Signing in…' });
  expect(button).toBeDisabled();
  await userEvent.click(button);
  expect(fetch).toHaveBeenCalledTimes(1);
  const { act } = await import('@testing-library/react');
  await act(async () => { complete(loginReply()); });
  expect(screen.getByRole('heading', { name: 'You’re signed in' })).toBeVisible();
});

test('session is restored on reload without storing credentials', async () => {
  setSession({ access_token: 'test-token', token_type: 'bearer', expires_in: 900 });
  vi.resetModules();
  const restored = await import('../features/auth/session');
  expect(restored.getToken()).toBe('test-token');
  restored.clearSession();
});

test('a late 401 from an old token does not clear a newer session', async () => {
  setSession({ access_token: 'old-token', token_type: 'bearer', expires_in: 900 });
  let complete;
  fetch.mockImplementation(() => new Promise(resolve => { complete = resolve; }));
  const request = apiRequest('/employees');
  setSession({ access_token: 'new-token', token_type: 'bearer', expires_in: 900 });
  complete(reply({ code: 'AUTH_REQUIRED' }, 401));
  await expect(request).rejects.toMatchObject({ status: 401 });
  expect(sessionStorage.getItem('skillmatch.session')).toContain('new-token');
});
