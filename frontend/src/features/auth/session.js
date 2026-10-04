const KEY = 'skillmatch.session';
const listeners = new Set();
let session = restore();

function restore() {
  try {
    const value = JSON.parse(sessionStorage.getItem(KEY));
    if (typeof value?.accessToken === 'string' && value.accessToken &&
        Number.isFinite(value.expiresAt) && value.expiresAt > Date.now()) return value;
    sessionStorage.removeItem(KEY);
  } catch { /* Storage may be unavailable; authentication can remain in memory. */ }
  return null;
}

export function getSession() { return session; }
export function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function clearSession() {
  session = null;
  try { sessionStorage.removeItem(KEY); } catch { /* In-memory fallback. */ }
  listeners.forEach(listener => listener());
}

export function setSession(response) {
  if (typeof response?.access_token !== 'string' || !response.access_token ||
      response.token_type !== 'bearer' || !Number.isFinite(response.expires_in) ||
      response.expires_in <= 0 || response.expires_in > 900) {
    throw new Error('Invalid token response');
  }
  session = { accessToken: response.access_token, expiresAt: Date.now() + response.expires_in * 1000 };
  try { sessionStorage.setItem(KEY, JSON.stringify(session)); } catch { /* In-memory fallback. */ }
  listeners.forEach(listener => listener());
}

export function getToken() {
  if (session && session.expiresAt <= Date.now()) clearSession();
  return session?.accessToken;
}
