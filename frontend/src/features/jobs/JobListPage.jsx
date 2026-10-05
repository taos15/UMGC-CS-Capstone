import React, { useEffect, useRef, useState } from 'react';
import { getJob, listJobs, requestRecommendations } from '../../api/jobs';
import './jobs.css';
import FeedbackForm from '../feedback/FeedbackForm';
import RecommendationResults from '../recommendations/RecommendationResults';

function failureMessage(error, action) {
  if (error.status === 403) return `You do not have permission to ${action}.`;
  if (error.status === 422) return 'Check your recommendation options and try again.';
  if (error.status === 404) return 'This job is no longer available. Select another job.';
  if (error.status === 501) return 'Jobs are not available yet. Please try again later.';
  return `Unable to ${action}. Please try again.`;
}

export default function JobListPage({ onLogout }) {
  const [jobs, setJobs] = useState([]);
  const [status, setStatus] = useState('OPEN');
  const [listState, setListState] = useState('loading');
  const [listError, setListError] = useState('');
  const [retry, setRetry] = useState(0);
  const [selected, setSelected] = useState(null);
  const [detail, setDetail] = useState(null);
  const [detailError, setDetailError] = useState('');
  const [results, setResults] = useState(null);
  const [requestError, setRequestError] = useState('');
  const [pending, setPending] = useState(false);
  const [topK, setTopK] = useState(5);
  const [minimumScore, setMinimumScore] = useState(0);
  const [includeGaps, setIncludeGaps] = useState(true);
  const currentId = useRef(null);
  const currentRequest = useRef(null);

  useEffect(() => {
    const controller = new AbortController();
    setListState('loading');
    setListError('');
    listJobs(controller.signal).then(data => {
      if (!controller.signal.aborted) { setJobs(data); setListState('ready'); }
    }).catch(error => {
      if (!controller.signal.aborted) { setListError(failureMessage(error, 'view jobs')); setListState('error'); }
    });
    return () => controller.abort();
  }, [retry]);

  useEffect(() => {
    if (!selected) return;
    const controller = new AbortController();
    getJob(selected.id, controller.signal).then(data => {
      if (!controller.signal.aborted) setDetail({ ...selected, ...data });
    }).catch(error => {
      if (!controller.signal.aborted) setDetailError(failureMessage(error, 'view this job'));
    });
    return () => controller.abort();
  }, [selected]);
  useEffect(() => () => currentRequest.current?.abort(), []);

  function selectJob(job) {
    currentRequest.current?.abort();
    currentRequest.current = null;
    currentId.current = job?.id ?? null;
    setSelected(job); setDetail(null); setDetailError(''); setResults(null); setRequestError(''); setPending(false);
  }

  function filterJobs(value) {
    setStatus(value);
    if (selected && value === 'OPEN' && selected.status !== 'OPEN') selectJob(null);
  }

  async function request(event) {
    event.preventDefault();
    if (!detail || detail.status !== 'OPEN' || currentRequest.current) return;
    const id = detail.id;
    const controller = new AbortController();
    currentRequest.current = controller;
    setPending(true); setRequestError(''); setResults(null);
    try {
      const data = await requestRecommendations(id, {
        top_k: Number(topK), minimum_score: Number(minimumScore), include_missing_skills: includeGaps,
      }, controller.signal);
      if (!controller.signal.aborted && currentId.current === id) setResults(data);
    } catch (error) {
      if (!controller.signal.aborted && currentId.current === id) setRequestError(failureMessage(error, 'request recommendations'));
    } finally {
      if (currentRequest.current === controller) { currentRequest.current = null; setPending(false); }
    }
  }

  const visibleJobs = jobs.filter(job => status === 'ALL' || job.status === 'OPEN');
  return <main className="workspace">
    <header className="workspace-header"><a className="workspace-brand" href="/">SkillMatch <span>AI</span></a><button className="secondary" onClick={onLogout}>Sign out</button></header>
    <div className="workspace-content">
      <p className="eyebrow">WORKFORCE WORKSPACE</p><h1>Jobs</h1>
      <p className="intro">Explore open opportunities and review skill-based recommendations.</p>
      <div className="job-toolbar"><div><label htmlFor="job-status">Job status</label><select id="job-status" value={status} onChange={event => filterJobs(event.target.value)}><option value="OPEN">OPEN jobs</option><option value="ALL">All jobs</option></select></div><span>{listState === 'ready' && `${visibleJobs.length} ${visibleJobs.length === 1 ? 'job' : 'jobs'}`}</span></div>
      {listState === 'loading' && <p role="status">Loading jobs…</p>}
      {listError && <div><p className="error" role="alert">{listError}</p><button className="secondary" onClick={() => setRetry(value => value + 1)}>Retry</button></div>}
      {listState === 'ready' && <div className="jobs-layout"><section aria-label="Available jobs" className="jobs-list">
        {visibleJobs.length === 0 && <p className="empty-state">No {status === 'OPEN' ? 'OPEN ' : ''}jobs found.</p>}
        {visibleJobs.map(job => <button className="job-card" key={job.id} aria-pressed={selected?.id === job.id} onClick={() => selectJob(job)}><span className="job-card-top"><strong>{job.title}</strong><span className={`job-status ${job.status === 'OPEN' ? 'open' : ''}`}>{job.status || 'Status unavailable'}</span></span><span>{job.minimum_years_experience} years minimum experience</span><span className="job-select">View job →</span></button>)}
      </section><section className="job-detail" aria-label="Selected job">
          {!selected && <div className="empty-detail"><p className="eyebrow">YOUR NEXT MATCH</p><h2>Select a job to get started</h2><p>Review the requirements, then request recommendations for an open job.</p></div>}
          {selected && <><h2>{selected.title}</h2>{!detail && !detailError && <p role="status">Loading job details…</p>}{detailError && <p className="error" role="alert">{detailError}</p>}
            {detail && <><p className="detail-status">{detail.status || 'Status unavailable'} · {detail.minimum_years_experience} years minimum experience</p>{detail.description && <p>{detail.description}</p>}
              <h3>Required skills</h3><div className="skill-tags">{detail.required_skills?.length ? detail.required_skills.map(skill => <span key={skill}>{skill}</span>) : <span>No required skills listed.</span>}</div>
              <h3>Required certifications</h3><div className="skill-tags">{detail.required_certifications?.length ? detail.required_certifications.map(code => <span key={code}>{code}</span>) : <span>No mandatory certifications listed.</span>}</div>
              {detail.status !== 'OPEN' ? <p>Recommendations are available for OPEN jobs.</p> : <form onSubmit={request} aria-busy={pending} className="recommendation-form"><h3>Recommendation options</h3><div className="options-grid"><div><label htmlFor="top-k">Maximum results</label><input id="top-k" type="number" min="1" max="100" step="1" required value={topK} onChange={event => setTopK(event.target.value)} disabled={pending} /></div><div><label htmlFor="minimum-score">Minimum score</label><input id="minimum-score" type="number" min="0" max="100" step="any" required value={minimumScore} onChange={event => setMinimumScore(event.target.value)} disabled={pending} /></div></div><label className="checkbox-label"><input type="checkbox" checked={includeGaps} onChange={event => setIncludeGaps(event.target.checked)} disabled={pending} />Show missing skills and credentials</label>{requestError && <p className="error" role="alert">{requestError}</p>}<button className="primary" type="submit" disabled={pending}>{pending ? 'Requesting…' : 'Request recommendations'}</button></form>}
              {results && <section className="recommendation-results" aria-label="Recommendations"><h3>Recommendations</h3><p className="result-note">Review these results before making a staffing decision.</p>{results.recommendations?.length ? <ol>{results.recommendations.map(candidate => <li key={candidate.employee_id || candidate.employeeId}><div><strong>{candidate.employeeName || `Employee ${candidate.employee_id}`}</strong><span>{candidate.score}/100</span></div><p>{candidate.explanation}</p></li>)}</ol> : <p>No candidates meet these options.</p>}</section>}
              {results && <FeedbackForm key={results.match_run_id || 'missing-run'} matchRunId={results.match_run_id} candidates={results.recommendations || []} />}
            </>}
          </>}
        </section></div>}
    </div>
  </main>;
}
