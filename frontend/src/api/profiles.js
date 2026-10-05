import { apiRequest } from './client';
function path(kind, id) {
  if (!['employees', 'jobs'].includes(kind)) throw new Error('Unsupported profile type');
  return `/${kind}${id ? `/${encodeURIComponent(id)}` : ''}`;
}
export const readProfile = (kind, id, signal) => apiRequest(path(kind, id), {signal});
export const listProfiles = (kind, signal) => apiRequest(path(kind), {signal});
export const createProfile = (kind, fields) => apiRequest(path(kind), {method: 'POST', body: fields});
export const updateProfile = (kind, id, fields, version) => {
  if (!Number.isInteger(version) || version < 1) throw new Error('A server version is required');
  return apiRequest(path(kind, id), {method: 'PUT', body: {...fields, version}});
};

export const deleteProfile = (kind, id, version) => {
  if (!Number.isInteger(version) || version < 1) throw new Error('A server version is required');
  return apiRequest(path(kind, id), {method: 'DELETE', body: {version}});
};
