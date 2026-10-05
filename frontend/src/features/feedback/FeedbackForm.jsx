import React, {useRef, useState} from 'react';
import {recordFeedback} from '../../api/feedback';
import './feedback.css';

const decisions = ['SELECTED', 'NOT_SELECTED', 'DEFERRED'];

function failureMessage(error) {
  if (error.status === 403) return 'You do not have permission to record feedback for this run. An administrator or the requesting supervisor is required.';
  if (error.status === 409) return 'This selection could not be recorded for this match run. Review your choice.';
  if (error.status === 404) return 'This match run is no longer available. Request a new run before recording feedback.';
  if (error.status === 422) return 'Some feedback fields are invalid. Review your decision and comment.';
  if (error.status === 503) return 'Feedback is temporarily unavailable. Your draft is still here; please try again.';
  return 'Unable to confirm feedback was recorded. Your draft is still here; please try again.';
}

export default function FeedbackForm({matchRunId, candidates = []}) {
  const [decision, setDecision] = useState('');
  const [selectedId, setSelectedId] = useState('');
  const [comment, setComment] = useState('');
  const [pending, setPending] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState(null);
  const submitting = useRef(false);
  const eligible = Array.isArray(candidates) ? candidates.filter(candidate => candidate?.eligible === true && typeof candidate.employee_id === 'string' && candidate.employee_id.length > 0) : [];
  const selectionAllowed = decision !== 'SELECTED' || eligible.some(candidate => candidate.employee_id === selectedId);
  const canSubmit = Boolean(matchRunId) && decisions.includes(decision) && selectionAllowed;

  function change(update) {update(); setSaved(false); setError(null);}
  async function submit(event) {
    event.preventDefault();
    if (!canSubmit || saved || submitting.current) return;
    submitting.current = true; setPending(true); setError(null);
    const body = {decision, ...(decision === 'SELECTED' ? {selected_employee_id: selectedId} : {}), ...(comment ? {comment} : {})};
    try {await recordFeedback(matchRunId, body); setSaved(true);}
    catch (failure) {setError({message: failureMessage(failure), requestId: failure.requestId});}
    finally {submitting.current = false; setPending(false);}
  }

  if (!matchRunId) return <p className="feedback-note">Feedback requires a saved match run. Request recommendations again.</p>;
  return <section className="feedback-panel" aria-label="Supervisor feedback">
    <h3>Supervisor feedback</h3>
    <p className="feedback-note">Record your decision for run {matchRunId}. Feedback adds an audit entry; it does not assign employees or update the matching model.</p>
    <form onSubmit={submit} aria-busy={pending}>
      <fieldset disabled={pending}>
        <legend>Decision and comment</legend>
        <label>Decision<select required value={decision} onChange={event => change(() => {setDecision(event.target.value); setSelectedId('');})}>
          <option value="">Choose a decision</option>{decisions.map(value => <option key={value} value={value}>{value}</option>)}
        </select></label>
        {decision === 'SELECTED' && <><label>Selected employee<select required value={selectedId} onChange={event => change(() => setSelectedId(event.target.value))}>
          <option value="">Choose an eligible candidate</option>{eligible.map(candidate => <option key={candidate.employee_id} value={candidate.employee_id}>Employee {candidate.employee_id} · Rank {candidate.rank} · {candidate.score}/100</option>)}
        </select></label>{!eligible.length && <p>No eligible candidates were returned for selection. You can record NOT_SELECTED or DEFERRED.</p>}</>}
        <label>Comment (optional)<textarea value={comment} onChange={event => change(() => setComment(event.target.value))} /></label>
      </fieldset>
      {error && <div className="error" role="alert"><p>{error.message}</p>{error.requestId && <small>Request ID: {error.requestId}</small>}</div>}
      {saved && <p className="feedback-success" role="status">Feedback recorded. This decision does not assign employees. Changing the form and submitting again adds another audit entry.</p>}
      <button className="primary" disabled={pending || saved || !canSubmit}>{pending ? 'Recording…' : 'Record feedback'}</button>
    </form>
  </section>;
}
