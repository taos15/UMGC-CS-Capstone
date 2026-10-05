import React, {useEffect, useState, useSyncExternalStore} from 'react';
import {apiRequest} from './api/client';
import {listProfiles} from './api/profiles';
import {getSession, subscribe, setSession, clearSession} from './features/auth/session';
import ProfileEditor from './features/profiles/ProfileEditor';

function Login() {
  const [error, setError] = useState(''); const [pending, setPending] = useState(false);
  async function submit(event) {
    event.preventDefault(); if (pending) return;
    const data = new FormData(event.currentTarget); setPending(true); setError('');
    try { setSession(await apiRequest('/auth/login', {method: 'POST', auth: false, body: {username: data.get('username'), password: data.get('password')}})); }
    catch (failure) { setError(failure.code === 'AUTH_INVALID_CREDENTIALS' ? 'Invalid username or password.' : 'Unable to sign in. Please try again.'); }
    finally { setPending(false); }
  }
  return <main><h1>SkillMatch</h1><h2>Sign in</h2>{error && <p role="alert">{error}</p>}<form onSubmit={submit}><label>Username<input name="username" autoComplete="username" required /></label><label>Password<input name="password" type="password" autoComplete="current-password" required /></label><button disabled={pending}>{pending ? 'Signing in…' : 'Sign in'}</button></form></main>;
}
function Profiles({kind}) {
  const [records, setRecords] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState('');
  const [editor, setEditor] = useState(null); const [refresh, setRefresh] = useState(0); const [message, setMessage] = useState('');
  useEffect(() => {
    const controller = new AbortController(); setLoading(true); setError('');
    listProfiles(kind, controller.signal).then(result => { if (!controller.signal.aborted) setRecords(Array.isArray(result) ? result : result.items || []); })
      .catch(failure => {if (!controller.signal.aborted) setError(failure.status === 501 ? 'Profile listing is not available yet.' : 'Unable to load profiles. Please try again.');})
      .finally(() => {if (!controller.signal.aborted) setLoading(false);});
    return () => controller.abort();
  }, [kind, refresh]);
  function back() {setEditor(null); setRefresh(value => value + 1);}
  if (editor) return <ProfileEditor key={editor.id || 'new'} kind={kind} recordId={editor.id} onCancel={back} onSaved={record => {if (!editor.id && record?.id) setEditor({id: record.id});}} onDeleted={() => {setMessage('Profile permanently deleted.'); back();}} />;
  return <section><h2>{kind === 'employees' ? 'Employees' : 'Jobs'}</h2><p>Profile changes and deletion require an administrator account.</p>{message && <p role="status">{message}</p>}<button onClick={() => setEditor({})}>Create profile</button>{loading && <p role="status">Loading profiles…</p>}{error && <p role="alert">{error} <button onClick={() => setRefresh(value => value + 1)}>Retry</button></p>}{!loading && !error && !records.length && <p>No profiles found.</p>}<ul>{records.map(record => <li key={record.id}><button className="secondary" onClick={() => setEditor({id: record.id})}>{record.name || record.title}</button></li>)}</ul><form onSubmit={event => {event.preventDefault(); const id = new FormData(event.currentTarget).get('id').trim(); if (id) setEditor({id});}}><label>Open profile by ID<input name="id" required /></label><button>Open profile</button></form></section>;
}
export default function App() {
  const session = useSyncExternalStore(subscribe, getSession); const [kind, setKind] = useState('employees');
  if (!session) return <Login />;
  return <main><header><h1>SkillMatch</h1><button className="secondary" onClick={clearSession}>Sign out</button></header><nav><button aria-pressed={kind === 'employees'} onClick={() => setKind('employees')}>Employees</button><button aria-pressed={kind === 'jobs'} onClick={() => setKind('jobs')}>Jobs</button></nav><Profiles key={kind} kind={kind} /></main>;
}
