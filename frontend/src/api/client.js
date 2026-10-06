import {getApiBaseUrl} from './config';
import { clearSession, getToken } from '../features/auth/session';
export class ApiError extends Error {
  constructor(status, problem = {}, requestId) {
    super('The request could not be completed.');
    problem = problem && typeof problem === 'object' && !Array.isArray(problem) ? problem : {};
    this.status = status;
    this.code = typeof problem.code === 'string' ? problem.code : 'HTTP_ERROR';
    this.requestId = [requestId, problem.request_id].find(value => typeof value === 'string' && /^[A-Za-z0-9._-]{1,128}$/.test(value));
    this.fieldErrors = status === 422 && Array.isArray(problem.field_errors) ? problem.field_errors.filter(item => item && typeof item.field === 'string' && /^[A-Za-z0-9_.[\]-]{1,120}$/.test(item.field)).map(item => ({field: item.field})) : [];
  }
}
export async function apiRequest(path, {method = 'GET', body, auth = true, signal} = {}) {
  if (!/^\/[a-zA-Z0-9_/-]*$/.test(path) || path.startsWith('//')) throw new Error('Use a relative API path');
  let base;
  try {base = getApiBaseUrl();} catch {throw new ApiError(0, {code: 'API_CONFIGURATION_ERROR'});}
  const token = auth ? getToken() : null;
  const headers = new Headers({Accept: 'application/json, application/problem+json'});
  if (body !== undefined) headers.set('Content-Type', 'application/json');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  let response;
  try { response = await fetch(`${base}${path}`, {method, headers, body: body === undefined ? undefined : JSON.stringify(body), signal, credentials: 'omit'}); }
  catch { throw new ApiError(0, {code: 'NETWORK_ERROR'}); }
  if (!response.ok) {
    if (response.status === 401 && token && token === getToken()) clearSession();
    throw new ApiError(response.status, await response.json().catch(() => ({})), response.headers.get('X-Request-ID'));
  }
  return response.status === 204 ? null : response.json();
}
