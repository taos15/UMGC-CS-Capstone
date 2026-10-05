import React from 'react';

const employeeSkill = {skill_id: '', proficiency: '', years_experience: '', last_used_on: ''};
const certification = {code: '', name: '', issuer: '', issued_on: '', expires_on: ''};
const jobSkill = {skill_id: '', level: 'REQUIRED', minimum_proficiency: '', importance: ''};

function Rows({title, rows, onChange, template, fields}) {
  return <section className="evidence"><h3>{title}</h3>{rows.map((row, index) => <fieldset className="evidence-row" key={index}><legend>{title} {index + 1}</legend><div className="row-fields">{fields.map(([key, label, type, min, max]) => <label key={key}>{label}{type === 'level' ? <select value={row[key]} onChange={event => onChange(rows.map((value, i) => i === index ? {...value, [key]: event.target.value} : value))}><option value="REQUIRED">REQUIRED</option><option value="PREFERRED">PREFERRED</option></select> : <input type={type} value={row[key] ?? ''} min={key === 'expires_on' ? row.issued_on : min} max={max} step={type === 'number' ? (key.includes('proficiency') || key === 'importance' ? 1 : 'any') : undefined} required={!['last_used_on', 'expires_on'].includes(key)} onChange={event => onChange(rows.map((value, i) => i === index ? {...value, [key]: event.target.value} : value))} />}</label>)}</div><button type="button" className="secondary" onClick={() => onChange(rows.filter((_, i) => i !== index))}>Remove {title.toLowerCase()} {index + 1}</button></fieldset>)}<button type="button" className="secondary" onClick={() => onChange([...rows, {...template}])}>Add {title.toLowerCase()}</button></section>;
}

export default function EvidenceFields({kind, draft, onChange}) {
  if (kind === 'employees') return <>
    <Rows title="Skill" rows={draft.skills} onChange={value => onChange('skills', value)} template={employeeSkill} fields={[
      ['skill_id', 'Skill ID', 'text'], ['proficiency', 'Proficiency (1–5)', 'number', 1, 5], ['years_experience', 'Years of experience', 'number', 0], ['last_used_on', 'Last used on', 'date'],
    ]} />
    <Rows title="Certification" rows={draft.certifications} onChange={value => onChange('certifications', value)} template={certification} fields={[
      ['code', 'Code', 'text'], ['name', 'Certification name', 'text'], ['issuer', 'Issuer', 'text'], ['issued_on', 'Issued on', 'date'], ['expires_on', 'Expires on', 'date'],
    ]} />
  </>;
  return <><Rows title="Skill requirement" rows={draft.skill_requirements} onChange={value => onChange('skill_requirements', value)} template={jobSkill} fields={[
    ['skill_id', 'Skill ID', 'text'], ['level', 'Level', 'level'], ['minimum_proficiency', 'Minimum proficiency (1–5)', 'number', 1, 5], ['importance', 'Importance (1–3)', 'number', 1, 3],
  ]} /><label>Required certification codes (one per line)<textarea value={draft.certification_requirements.join('\n')} onChange={event => onChange('certification_requirements', event.target.value.split('\n'))} /></label></>;
}
