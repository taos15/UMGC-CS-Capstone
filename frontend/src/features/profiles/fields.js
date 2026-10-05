export const schema = {
  employees: [
    ['employee_number', 'Employee number', 'text'], ['name', 'Name', 'text'],
    ['current_title', 'Current title', 'text'], ['status', 'Status', 'text'],
    ['total_years_experience', 'Total years of experience', 'number'],
  ],
  jobs: [
    ['job_code', 'Job code', 'text'], ['title', 'Title', 'text'],
    ['description', 'Description', 'textarea'], ['status', 'Status', 'text'],
    ['minimum_years_experience', 'Minimum years of experience', 'number'],
  ],
};
export function newDraft(kind) {
  return {...Object.fromEntries(schema[kind].map(([key]) => [key, ''])),
    ...(kind === 'employees' ? {skills: [], certifications: []} : {skill_requirements: [], certification_requirements: []})};
}
export function draftFromRecord(kind, record) {
  const draft = newDraft(kind);
  for (const key of Object.keys(draft)) if (record[key] !== undefined) draft[key] = structuredClone(record[key]);
  return draft;
}
export function payloadFromDraft(kind, draft) {
  const payload = Object.fromEntries(schema[kind].map(([key, , type]) => [key, type === 'number' ? Number(draft[key]) : draft[key]]));
  if (kind === 'employees') {
    payload.skills = draft.skills.map(skill => ({skill_id: skill.skill_id, proficiency: Number(skill.proficiency), years_experience: Number(skill.years_experience), last_used_on: skill.last_used_on || null}));
    payload.certifications = draft.certifications.map(cert => ({code: cert.code, name: cert.name, issuer: cert.issuer, issued_on: cert.issued_on, expires_on: cert.expires_on || null}));
  } else {
    payload.skill_requirements = draft.skill_requirements.map(skill => ({skill_id: skill.skill_id, level: skill.level, minimum_proficiency: Number(skill.minimum_proficiency), importance: Number(skill.importance)}));
    payload.certification_requirements = draft.certification_requirements.map(code => code.trim()).filter(Boolean);
  }
  return payload;
}
