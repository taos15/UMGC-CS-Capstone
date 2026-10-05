import React, {useEffect, useState} from 'react';
import {listProfiles} from '../../api/profiles';
import ProfileEditor from './ProfileEditor';
export default function ProfilesPage({kind}) {
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
