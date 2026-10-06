import React from 'react';
import './recommendations.css';

const componentLabels = {
  required_skills: 'Required skills', preferred_skills: 'Preferred skills',
  required_certifications: 'Required certifications', experience: 'Experience',
};
const evidenceFields = ['matched_skills', 'missing_skills', 'matched_certifications', 'missing_certifications', 'ineligible_reasons'];

function validCandidate(candidate) {
  return candidate && typeof candidate.employee_id === 'string' && candidate.employee_id.length > 0
    && Number.isInteger(candidate.rank) && candidate.rank > 0
    && Number.isFinite(candidate.score) && candidate.score >= 0 && candidate.score <= 100
    && typeof candidate.eligible === 'boolean' && typeof candidate.explanation === 'string'
    && candidate.component_scores && typeof candidate.component_scores === 'object'
    && !Array.isArray(candidate.component_scores)
    && Object.values(candidate.component_scores).every(Number.isFinite)
    && evidenceFields.every(key => Array.isArray(candidate[key]) && candidate[key].every(value => typeof value === 'string'));
}

function Evidence({title, values, missing = false}) {
  return <section className={`candidate-evidence${missing ? ' evidence-gaps' : ''}`}>
    <h5>{title}</h5>
    {values.length ? <ul>{values.map((value, index) => <li key={index}>{value}</li>)}</ul> : <p>None reported.</p>}
  </section>;
}

export default function RecommendationResults({result}) {
  if (!Array.isArray(result?.recommendations) || !result.recommendations.every(validCandidate)) {
    return <p className="error" role="alert">Recommendation evidence is unavailable. Please request recommendations again.</p>;
  }
  return <section className="recommendation-results" aria-label="Recommendations">
    <h3>Recommendations</h3>
    <p className="result-note">Decision support only. Supervisor retains final staffing authority. These results do not assign employees.</p>
    <dl className="run-metadata"><div><dt>Match run</dt><dd>{result.match_run_id || 'Unavailable'}</dd></div><div><dt>Model version</dt><dd>{result.model_version || 'Unavailable'}</dd></div></dl>
    {!result.recommendations.length ? <p role="status">No candidates meet these options.</p> : <ol className="candidate-list">
      {result.recommendations.map(candidate => <li key={candidate.employee_id}>
        <article className="candidate-card" aria-label={`Employee ${candidate.employee_id}`}>
          <header className="candidate-header">
            <div><span className="candidate-rank">Rank {candidate.rank}</span><h4>Employee {candidate.employee_id}</h4></div>
            <strong className="candidate-score" aria-label={`Score ${candidate.score} out of 100`}>{candidate.score}/100</strong>
          </header>
          <p className={`candidate-eligibility ${candidate.eligible ? 'is-eligible' : 'is-ineligible'}`}>{candidate.eligible ? 'Eligible' : 'Ineligible'}</p>
          {candidate.ineligible_reasons.length > 0 && <Evidence title="Ineligibility reasons" values={candidate.ineligible_reasons} missing />}
          <div className="candidate-evidence-grid">
            <Evidence title="Matched skills" values={candidate.matched_skills} />
            <Evidence title="Missing skills" values={candidate.missing_skills} missing />
            <Evidence title="Matched certifications" values={candidate.matched_certifications} />
            <Evidence title="Missing certifications" values={candidate.missing_certifications} missing />
          </div>
          <section className="candidate-components"><h5>Component scores</h5><p className="component-note">Server component values on a 0–1 scale.</p>
            {Object.keys(candidate.component_scores).length ? <dl>{Object.entries(candidate.component_scores).map(([key, value]) => <div key={key}><dt>{componentLabels[key] || key.replaceAll('_', ' ')}</dt><dd>{value}/1</dd></div>)}</dl> : <p>No component scores reported.</p>}
          </section>
          <section className="candidate-explanation"><h5>Explanation</h5><p>{candidate.explanation || 'No explanation reported.'}</p></section>
        </article>
      </li>)}
    </ol>}
  </section>;
}
