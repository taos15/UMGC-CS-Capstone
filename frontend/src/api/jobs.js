import { apiRequest } from './client';

export async function listJobs(signal) {
  const jobs = await apiRequest('/jobs', { signal });
  if (!Array.isArray(jobs)) throw new Error('Invalid jobs response');
  return jobs;
}

export const getJob = (id, signal) => apiRequest(`/jobs/${encodeURIComponent(id)}`, { signal });
export const requestRecommendations = (id, options, signal) =>
  apiRequest(`/jobs/${encodeURIComponent(id)}/recommendations`, { method: 'POST', body: options, signal });
