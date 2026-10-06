import React from 'react';

const messages = {
  JOB_NOT_OPEN: 'This job is no longer OPEN. Select another open job.',
  JOB_HAS_NO_CRITERIA: 'This job has no usable matching criteria. Ask an administrator to update its requirements.',
  DATABASE_UNAVAILABLE: 'The database is temporarily unavailable. Please try again.',
  MATCH_ENGINE_UNAVAILABLE: 'Matching is temporarily unavailable. Please try again.',
  AUTH_UNAVAILABLE: 'Sign-in is temporarily unavailable. Please try again.',
  AUTH_REQUIRED: 'Your session has ended. Please sign in again.',
  API_CONFIGURATION_ERROR: 'The API connection is not configured correctly. Contact your administrator.',
};
const labels = {
  top_k: 'Maximum results', topK: 'Maximum results', minimum_score: 'Minimum score', minimumScore: 'Minimum score',
  decision: 'Decision', selected_employee_id: 'Selected employee', comment: 'Comment',
  username: 'Username', password: 'Password', employee_number: 'Employee number', job_code: 'Job code',
  name: 'Name', title: 'Title', status: 'Status',
};

export function uiProblem(error, fallback) {
  return {
    message: messages[error?.code] || (error?.status === 500 ? 'Something went wrong. Please try again.' : fallback),
    requestId: error?.requestId,
    fields: error?.fieldErrors?.map(item => item.field) || [],
  };
}

export default function ProblemAlert({error, id, fieldTargets = {}, children}) {
  return <div className="error" role="alert" id={id}>
    <p>{error.message}</p>
    {error.fields?.length > 0 && <ul>{error.fields.map((field, index) => {
      const key = field.replace(/^body\./, '');
      const label = labels[key] || key.replaceAll('_', ' ');
      return <li key={index}>{fieldTargets[key] ? <a href={`#${fieldTargets[key]}`}>Check {label}.</a> : `Check ${label}.`}</li>;
    })}</ul>}
    {error.requestId && <small>Request ID: {error.requestId}</small>}
    {children}
  </div>;
}
