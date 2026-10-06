import React, { useEffect, useRef, useState } from 'react';
import { createProfile, deleteProfile, readProfile, updateProfile } from '../../api/profiles';
import { draftFromRecord, newDraft, payloadFromDraft, schema } from './fields';
import ProblemAlert, {uiProblem} from '../../components/ProblemAlert';
import EvidenceFields from './EvidenceFields';

export default function ProfileEditor({kind, recordId, onSaved, onCancel, onDeleted}) {
  const [draft, setDraft] = useState(recordId ? null : newDraft(kind));
  const [version, setVersion] = useState(null);
  const [loading, setLoading] = useState(Boolean(recordId));
  const [pending, setPending] = useState(false);
  const [conflict, setConflict] = useState(false);
  const [confirmReload, setConfirmReload] = useState(false);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const submission = useRef(false);
  const activeLoad = useRef(null);

  async function load() {
    activeLoad.current?.abort();
    const controller = new AbortController(); activeLoad.current = controller;
    setLoading(true); setError(null); setSaved(false);
    try {
      const record = await readProfile(kind, recordId, controller.signal);
      if (controller.signal.aborted) return;
      setDraft(draftFromRecord(kind, record));
      const valid = Number.isInteger(record.version) && record.version > 0;
      setVersion(valid ? record.version : null);
      if (valid) setConflict(false);
      else setError({message: 'This profile does not include a valid version. Editing is unavailable until the profile API supports versioned updates.'});
    } catch (failure) { if (!controller.signal.aborted) setError(safeError(failure)); }
    finally { if (!controller.signal.aborted) setLoading(false); }
  }
  useEffect(() => {
    if (recordId) load();
    return () => activeLoad.current?.abort();
  }, [kind, recordId]);

  function change(key, value) { setDraft(previous => ({...previous, [key]: value})); setSaved(false); }
  async function save(event) {
    event.preventDefault();
    if (submission.current || conflict || (recordId && version === null)) return;
    submission.current = true; setPending(true); setError(null); setSaved(false);
    try {
      const fields = payloadFromDraft(kind, draft);
      const updated = recordId ? await updateProfile(kind, recordId, fields, version) : await createProfile(kind, fields);
      if (recordId) {
        if (Number.isInteger(updated?.version) && updated.version > version) {
          setVersion(updated.version); setDraft(draftFromRecord(kind, updated));
        } else { setVersion(null); setError({message: 'Saved, but the server did not return a revised version. Reload before editing again.'}); }
      }
      setSaved(true); onSaved?.(updated);
    } catch (failure) {
      if (failure.status === 409 && failure.code === 'STALE_VERSION') setConflict(true);
      setError(safeError(failure));
    } finally { submission.current = false; setPending(false); }
  }
  async function remove() {
    if (submission.current || conflict || version === null) return;
    submission.current = true; setPending(true); setError(null); setConfirmDelete(false);
    try { await deleteProfile(kind, recordId, version); onDeleted?.(); }
    catch (failure) {
      if (failure.status === 409 && failure.code === 'STALE_VERSION') setConflict(true);
      setError(safeError(failure));
    } finally { submission.current = false; setPending(false); }
  }
  const readonly = recordId && version === null;
  return <section className="editor"><h2>{recordId ? 'Edit' : 'Create'} {kind === 'employees' ? 'employee' : 'job'} profile</h2>
    {loading && <p role="status">Loading profile…</p>}
    {error && <ProblemAlert error={error}>
      {conflict && <><p>Your unsaved changes are still here. Review or copy them before reloading.</p><button type="button" className="secondary" onClick={() => setConfirmReload(true)}>Reload latest version</button></>}
    </ProblemAlert>}
    {confirmReload && <div className="confirmation" role="alertdialog" aria-labelledby="reload-title"><h3 id="reload-title">Reloading will replace your unsaved changes.</h3><button className="secondary" onClick={() => setConfirmReload(false)}>Keep my changes</button><button className="secondary" onClick={() => {setConfirmReload(false); load();}}>Discard changes and reload</button></div>}
    {confirmDelete && <div className="confirmation" role="alertdialog" aria-labelledby="delete-title"><h3 id="delete-title">Permanently delete this profile?</h3><p>{draft?.name || draft?.title} will be permanently removed. This cannot be undone.</p><button className="secondary" onClick={() => setConfirmDelete(false)}>Cancel deletion</button><button className="danger" onClick={remove}>Confirm permanent deletion</button></div>}
    {saved && <p className="success" role="status">Profile saved.</p>}
    {draft && <form onSubmit={save} aria-busy={pending}><fieldset disabled={pending || loading || readonly}><legend>Profile details</legend><div className="form-grid">{schema[kind].map(([key, label, type]) => <label key={key}>{label}{type === 'textarea' ? <textarea value={draft[key]} required onChange={event => change(key, event.target.value)} /> : <input type={type} required value={draft[key]} min={type === 'number' ? 0 : undefined} step={type === 'number' ? 'any' : undefined} onChange={event => change(key, event.target.value)} />}</label>)}</div><EvidenceFields kind={kind} draft={draft} onChange={change} /></fieldset><div className="form-actions"><button className="primary" disabled={pending || loading || readonly || conflict}>{pending ? 'Saving…' : recordId ? 'Save changes' : 'Create profile'}</button><button type="button" className="secondary" disabled={pending} onClick={onCancel}>Back to profiles</button>{recordId && <button type="button" className="danger" disabled={pending || loading || readonly || conflict} onClick={() => setConfirmDelete(true)}>Delete permanently</button>}</div></form>}
    {!draft && !loading && !conflict && <button className="secondary" onClick={load}>Retry</button>}
  </section>;
}
function safeError(error) {
  let message = 'Unable to save this profile. Please try again.';
  if (error.status === 409 && error.code === 'STALE_VERSION') message = 'Someone else updated this profile. Your version is out of date.';
  else if (error.status === 409) message = 'A profile with this business identifier already exists. Check the employee number or job code.';
  else if (error.status === 403) message = 'You do not have permission to change this profile. An administrator is required.';
  else if (error.status === 404) message = 'This profile is no longer available.';
  else if (error.status === 422) message = 'Some profile fields are invalid. Check the fields below.';
  else if (error.status === 501) message = 'This operation is not available yet. Your changes have not been saved.';
  return uiProblem(error, message);
}
