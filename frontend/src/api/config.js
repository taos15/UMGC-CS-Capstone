// Includes the API version prefix. Empty configuration uses same-origin routing.
export function getApiBaseUrl() {
  const base = (import.meta.env.VITE_API_BASE_URL || '/api/v1').trim().replace(/\/+$/, '');
  if (base.startsWith('/') && !base.startsWith('//') && /^\/[A-Za-z0-9_./~-]+$/.test(base)) return base;
  const url = new URL(base);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) throw new Error('Invalid API configuration');
  return base;
}
