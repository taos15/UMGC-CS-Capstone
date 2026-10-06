import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, afterEach, test, expect, vi } from 'vitest';
import JobListPage from './JobListPage';
import { setSession, clearSession } from '../auth/session';

const jobs = [
  { id: 'electrician', title: 'Commercial Electrician', status: 'OPEN', required_skills: ['Wiring'], preferred_skills: [], required_certifications: ['License'], minimum_years_experience: 5 },
  { id: 'hvac', title: 'HVAC Technician', status: 'OPEN', required_skills: [], required_certifications: [], minimum_years_experience: 3 },
  { id: 'closed', title: 'Closed position', status: 'CLOSED', required_skills: [], required_certifications: [], minimum_years_experience: 0 },
];
const reply = (body, status = 200) => new Response(JSON.stringify(body), { status });
beforeEach(() => {
  setSession({ access_token: 'test-token', token_type: 'bearer', expires_in: 900 });
  vi.stubGlobal('fetch', vi.fn(async path => {
    if (path === '/api/v1/jobs') return reply(jobs);
    return reply(jobs.find(job => path === `/api/v1/jobs/${job.id}`));
  }));
});
afterEach(() => { clearSession(); vi.unstubAllGlobals(); });

test('shows OPEN jobs by default and allows all-status filtering', async () => {
  render(<JobListPage onLogout={vi.fn()} />);
  expect(await screen.findByRole('button', { name: /Commercial Electrician/ })).toBeVisible();
  expect(screen.queryByRole('button', { name: /Closed position/ })).not.toBeInTheDocument();
  await userEvent.selectOptions(screen.getByLabelText('Job status'), 'ALL');
  expect(screen.getByRole('button', { name: /Closed position/ })).toBeVisible();
  expect(fetch.mock.calls[0][1].headers.get('Authorization')).toBe('Bearer test-token');
});

test('selected job details and snake_case request options use canonical URLs', async () => {
  fetch.mockImplementation(async path => {
    if (path.endsWith('/recommendations')) return reply({ jobId: 'electrician', match_run_id: 'run-id', model_version: 'rules-v1', recommendations: [
      { rank: 1, employee_id: 'emp-1', score: 90, eligible: true, component_scores: {required_skills: .9}, matched_skills: ['Wiring'], missing_skills: ['Inspection'], matched_certifications: ['License'], missing_certifications: [], ineligible_reasons: [], explanation: 'Matches required skills.' },
    ] });
    return reply(path === '/api/v1/jobs' ? jobs : jobs[0]);
  });
  render(<JobListPage onLogout={vi.fn()} />);
  await userEvent.click(await screen.findByRole('button', { name: /Commercial Electrician/ }));
  expect(await screen.findByText('Wiring')).toBeVisible();
  await userEvent.click(screen.getByRole('button', { name: 'Request recommendations' }));
  expect(await screen.findByText('Employee emp-1')).toBeVisible();
  expect(screen.getByText('Rank 1')).toBeVisible();
  expect(screen.getByText('Inspection')).toBeVisible();
  expect(screen.getByText('Eligible')).toBeVisible();
  expect(screen.getByText('0.9/1')).toBeVisible();
  const request = fetch.mock.calls.find(([path]) => path.endsWith('/recommendations'));
  expect(request[0]).toBe('/api/v1/jobs/electrician/recommendations');
  expect(JSON.parse(request[1].body)).toEqual({ top_k: 5, minimum_score: 0, include_missing_skills: true });
  expect(request[1].headers.get('Authorization')).toBe('Bearer test-token');
});

test('closed jobs can be viewed but not requested', async () => {
  render(<JobListPage onLogout={vi.fn()} />);
  await screen.findByRole('button', { name: /Commercial Electrician/ });
  await userEvent.selectOptions(screen.getByLabelText('Job status'), 'ALL');
  await userEvent.click(screen.getByRole('button', { name: /Closed position/ }));
  expect(await screen.findByText('Recommendations are available for OPEN jobs.')).toBeVisible();
  expect(screen.queryByRole('button', { name: 'Request recommendations' })).not.toBeInTheDocument();
});

test('loading, empty, and safe list failure states', async () => {
  fetch.mockResolvedValue(reply([], 200));
  const view = render(<JobListPage onLogout={vi.fn()} />);
  expect(screen.getByRole('status')).toHaveTextContent('Loading jobs');
  expect(await screen.findByText('No OPEN jobs found.')).toBeVisible();
  view.unmount();
  fetch.mockResolvedValue(reply({ code: 'FORBIDDEN', detail: 'private detail' }, 403));
  render(<JobListPage onLogout={vi.fn()} />);
  expect(await screen.findByRole('alert')).toHaveTextContent('You do not have permission to view jobs.');
  expect(screen.queryByText('private detail')).not.toBeInTheDocument();
});

test('viewer recommendation rejection is safe and request can be retried', async () => {
  fetch.mockImplementation(async path => {
    if (path.endsWith('/recommendations')) return reply({ code: 'FORBIDDEN', detail: 'private detail' }, 403);
    return reply(path === '/api/v1/jobs' ? jobs : jobs[0]);
  });
  render(<JobListPage onLogout={vi.fn()} />);
  await userEvent.click(await screen.findByRole('button', { name: /Commercial Electrician/ }));
  const submit = await screen.findByRole('button', { name: 'Request recommendations' });
  await userEvent.click(submit);
  expect(await screen.findByRole('alert')).toHaveTextContent('You do not have permission to request recommendations.');
  expect(submit).toBeEnabled();
});

test('duplicate requests are prevented while pending', async () => {
  let resolve;
  fetch.mockImplementation(async path => {
    if (path.endsWith('/recommendations')) return new Promise(complete => { resolve = complete; });
    return reply(path === '/api/v1/jobs' ? jobs : jobs[0]);
  });
  render(<JobListPage onLogout={vi.fn()} />);
  await userEvent.click(await screen.findByRole('button', { name: /Commercial Electrician/ }));
  await userEvent.click(await screen.findByRole('button', { name: 'Request recommendations' }));
  expect(screen.getByRole('button', { name: 'Requesting…' })).toBeDisabled();
  await userEvent.click(screen.getByRole('button', { name: 'Requesting…' }));
  expect(fetch.mock.calls.filter(([path]) => path.endsWith('/recommendations'))).toHaveLength(1);
  resolve(reply({ recommendations: [], model_version: 'rules-v1', match_run_id: 'run' }));
  await waitFor(() => expect(screen.getByText('No candidates meet these options.')).toBeVisible());
});

test('late recommendations for a previously selected job are discarded', async () => {
  let complete;
  fetch.mockImplementation(async path => {
    if (path.endsWith('/recommendations')) return new Promise(resolve => { complete = resolve; });
    return reply(path === '/api/v1/jobs' ? jobs : jobs.find(job => path.endsWith(`/${job.id}`)));
  });
  render(<JobListPage onLogout={vi.fn()} />);
  await userEvent.click(await screen.findByRole('button', { name: /Commercial Electrician/ }));
  await userEvent.click(await screen.findByRole('button', { name: 'Request recommendations' }));
  await userEvent.click(screen.getByRole('button', { name: /HVAC Technician/ }));
  const { act } = await import('@testing-library/react');
  await act(async () => { complete(reply({ recommendations: [{ rank: 1, employee_id: 'old', score: 90, eligible: true, component_scores: {}, matched_skills: [], missing_skills: [], matched_certifications: [], missing_certifications: [], ineligible_reasons: [], explanation: 'Old result' }] })); });
  expect(await screen.findByRole('heading', { name: 'HVAC Technician' })).toBeVisible();
  expect(screen.queryByText('Old result')).not.toBeInTheDocument();
});

test('updated non-OPEN detail prevents recommendation requests', async () => {
  fetch.mockImplementation(async path => reply(path === '/api/v1/jobs' ? jobs : { ...jobs[0], status: 'CLOSED' }));
  render(<JobListPage onLogout={vi.fn()} />);
  await userEvent.click(await screen.findByRole('button', { name: /Commercial Electrician/ }));
  expect(await screen.findByText('Recommendations are available for OPEN jobs.')).toBeVisible();
  expect(screen.queryByRole('button', { name: 'Request recommendations' })).not.toBeInTheDocument();
});

test('feedback targets the returned run and a new recommendation clears the previous draft', async () => {
  let runNumber = 0;
  fetch.mockImplementation(async (path, options) => {
    if (path.endsWith('/feedback')) return reply({decision: 'SELECTED'}, 201);
    if (path.endsWith('/recommendations')) return reply({
      match_run_id: `stored-run-${++runNumber}`, model_version: 'rules-v1', recommendations: [{
        rank: 1, employee_id: 'eligible-employee', eligible: true, score: 90, explanation: 'Server explanation.',
        component_scores: {}, matched_skills: [], missing_skills: [], matched_certifications: [], missing_certifications: [], ineligible_reasons: [],
      }],
    });
    return reply(path === '/api/v1/jobs' ? jobs : jobs[0]);
  });
  render(<JobListPage onLogout={vi.fn()} />);
  await userEvent.click(await screen.findByRole('button', {name: /Commercial Electrician/}));
  await userEvent.click(await screen.findByRole('button', {name: 'Request recommendations'}));
  await userEvent.selectOptions(await screen.findByLabelText('Decision'), 'SELECTED');
  await userEvent.selectOptions(screen.getByLabelText('Selected employee'), 'eligible-employee');
  await userEvent.type(screen.getByLabelText('Comment (optional)'), 'Reviewed first run');
  await userEvent.click(screen.getByRole('button', {name: 'Record feedback'}));
  expect(await screen.findByText(/Feedback recorded/)).toBeVisible();
  const request = fetch.mock.calls.find(([path]) => path.endsWith('/feedback'));
  expect(request[0]).toBe('/api/v1/match-runs/stored-run-1/feedback');
  expect(JSON.parse(request[1].body)).toEqual({decision: 'SELECTED', selected_employee_id: 'eligible-employee', comment: 'Reviewed first run'});
  await userEvent.click(screen.getByRole('button', {name: 'Request recommendations'}));
  await waitFor(() => expect(screen.getByLabelText('Decision')).toHaveValue(''));
  expect(screen.getByLabelText('Comment (optional)')).toHaveValue('');
  await userEvent.selectOptions(screen.getByLabelText('Decision'), 'DEFERRED');
  await userEvent.click(screen.getByRole('button', {name: 'Record feedback'}));
  await screen.findByText(/Feedback recorded/);
  expect(fetch.mock.calls.filter(([path]) => path.endsWith('/feedback'))[1][0]).toBe('/api/v1/match-runs/stored-run-2/feedback');
});

for (const [status, code, expected] of [[422, 'VALIDATION_ERROR', 'Check Maximum results.'], [503, 'MATCH_ENGINE_UNAVAILABLE', 'Matching is temporarily unavailable'], [409, 'JOB_NOT_OPEN', 'no longer OPEN']]) {
  test(`recommendation ${code} appears beside options with support correlation`, async () => {
    fetch.mockImplementation(async path => {
      if (path.endsWith('/recommendations')) return reply({code, request_id: 'support-trace', detail: 'private database details', field_errors: [{field: 'body.top_k', message: 'private context'}]}, status);
      return reply(path === '/api/v1/jobs' ? jobs : jobs[0]);
    });
    render(<JobListPage onLogout={vi.fn()} />);
    await userEvent.click(await screen.findByRole('button', {name: /Commercial Electrician/}));
    await userEvent.click(await screen.findByRole('button', {name: 'Request recommendations'}));
    expect(await screen.findByRole('alert')).toHaveTextContent(expected);
    expect(screen.getByText('Request ID: support-trace')).toBeVisible();
    expect(screen.queryByText(/private database/)).not.toBeInTheDocument();
    expect(screen.getByRole('button', {name: 'Request recommendations'})).toBeEnabled();
    if (status === 422) expect(screen.getByRole('link', {name: 'Check Maximum results.'})).toHaveAttribute('href', '#top-k');
  });
}
