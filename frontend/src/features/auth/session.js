const KEY = 'skillmatch.session';
const listeners = new Set();
let session = null;
try { const saved = JSON.parse(sessionStorage.getItem(KEY)); if (saved?.accessToken && saved.expiresAt > Date.now()) session = saved; else sessionStorage.removeItem(KEY); } catch { /* Memory-only fallback. */ }
export const getSession = () => session;
export function subscribe(listener) { listeners.add(listener); return () => listeners.delete(listener); }
export function clearSession() { session = null; try { sessionStorage.removeItem(KEY); } catch {} listeners.forEach(listener => listener()); }
export function setSession(value) {
  if (!value?.access_token || value.token_type !== 'bearer' || !(value.expires_in > 0 && value.expires_in <= 900)) throw new Error('Invalid session');
  session = { accessToken: value.access_token, expiresAt: Date.now() + value.expires_in * 1000 };
  try { sessionStorage.setItem(KEY, JSON.stringify(session)); } catch {}
  listeners.forEach(listener => listener());
}
export function getToken() { if (session?.expiresAt <= Date.now()) clearSession(); return session?.accessToken; }
