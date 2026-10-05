import React from 'react';
import {render, screen, waitFor} from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import {beforeEach, afterEach, expect, test, vi} from 'vitest';
import FeedbackForm from './FeedbackForm';
import {setSession, clearSession} from '../auth/session';

const candidates = [{employee_id: 'eligible-id', rank: 1, score: 90, eligible: true}, {employee_id: 'ineligible-id', rank: 2, score: 70, eligible: false}];
const reply = (body, status = 201) => new Response(JSON.stringify(body), {status});
beforeEach(() => {
  setSession({access_token: 'test-token', token_type: 'bearer', expires_in: 900});
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(reply({match_run_id: 'run-1', decision: 'DEFERRED'})));
});
afterEach(() => {clearSession(); vi.unstubAllGlobals();});

for (const decision of ['SELECTED', 'NOT_SELECTED', 'DEFERRED']) {
  test(`${decision} posts canonical feedback against the exact run with optional comment`, async () => {
    render(<FeedbackForm matchRunId="run-1" candidates={candidates} />);
    await userEvent.selectOptions(screen.getByLabelText('Decision'), decision);
    if (decision === 'SELECTED') {
      expect(screen.queryByRole('option', {name: /ineligible-id/})).not.toBeInTheDocument();
      await userEvent.selectOptions(screen.getByLabelText('Selected employee'), 'eligible-id');
    }
    await userEvent.type(screen.getByLabelText('Comment (optional)'), 'Reviewed fit.');
    await userEvent.click(screen.getByRole('button', {name: 'Record feedback'}));
    expect(await screen.findByRole('status')).toHaveTextContent('Feedback recorded');
    const [url, options] = fetch.mock.calls[0];
    expect(url).toBe('/api/v1/match-runs/run-1/feedback');
    expect(options.method).toBe('POST');
    expect(options.headers.get('Authorization')).toBe('Bearer test-token');
    expect(JSON.parse(options.body)).toEqual({decision, comment: 'Reviewed fit.', ...(decision === 'SELECTED' ? {selected_employee_id: 'eligible-id'} : {})});
    expect(screen.getByRole('button', {name: 'Record feedback'})).toBeDisabled();
  });
}

test('changing from SELECTED omits employee ID and blank optional comment', async () => {
  render(<FeedbackForm matchRunId="run-1" candidates={candidates} />);
  await userEvent.selectOptions(screen.getByLabelText('Decision'), 'SELECTED');
  await userEvent.selectOptions(screen.getByLabelText('Selected employee'), 'eligible-id');
  await userEvent.selectOptions(screen.getByLabelText('Decision'), 'DEFERRED');
  expect(screen.queryByLabelText('Selected employee')).not.toBeInTheDocument();
  await userEvent.click(screen.getByRole('button', {name: 'Record feedback'}));
  await screen.findByRole('status');
  expect(JSON.parse(fetch.mock.calls[0][1].body)).toEqual({decision: 'DEFERRED'});
});

test('requires a decision and an eligible selection before submitting', async () => {
  render(<FeedbackForm matchRunId="run-1" candidates={[]} />);
  expect(screen.getByRole('button', {name: 'Record feedback'})).toBeDisabled();
  await userEvent.selectOptions(screen.getByLabelText('Decision'), 'SELECTED');
  expect(screen.getByRole('button', {name: 'Record feedback'})).toBeDisabled();
  expect(fetch).not.toHaveBeenCalled();
});

for (const [status, code, message] of [[403, 'FORBIDDEN', 'permission'], [409, 'FEEDBACK_CONFLICT', 'selection'], [503, 'DATABASE_UNAVAILABLE', 'temporarily unavailable']]) {
  test(`${code} keeps the draft and shows safe retry messaging`, async () => {
    fetch.mockResolvedValue(reply({code, detail: 'private details', request_id: 'trace-id'}, status));
    render(<FeedbackForm matchRunId="run-1" candidates={candidates} />);
    await userEvent.selectOptions(screen.getByLabelText('Decision'), 'DEFERRED');
    await userEvent.type(screen.getByLabelText('Comment (optional)'), 'Keep this draft');
    await userEvent.click(screen.getByRole('button', {name: 'Record feedback'}));
    expect(await screen.findByRole('alert')).toHaveTextContent(message);
    expect(screen.getByLabelText('Comment (optional)')).toHaveValue('Keep this draft');
    expect(screen.queryByText('private details')).not.toBeInTheDocument();
    expect(screen.getByRole('button', {name: 'Record feedback'})).toBeEnabled();
    expect(fetch).toHaveBeenCalledTimes(1);
  });
}

test('pending feedback cannot be submitted twice', async () => {
  let complete;
  fetch.mockImplementation(() => new Promise(resolve => {complete = resolve;}));
  render(<FeedbackForm matchRunId="run-1" candidates={candidates} />);
  await userEvent.selectOptions(screen.getByLabelText('Decision'), 'DEFERRED');
  await userEvent.click(screen.getByRole('button', {name: 'Record feedback'}));
  const submit = screen.getByRole('button', {name: 'Recording…'});
  expect(submit).toBeDisabled();
  await userEvent.click(submit);
  expect(fetch).toHaveBeenCalledTimes(1);
  complete(reply({decision: 'DEFERRED'}));
  await screen.findByRole('status');
});

test('a missing run ID cannot send feedback', () => {
  render(<FeedbackForm candidates={candidates} />);
  expect(screen.getByText(/Feedback requires a saved match run/)).toBeVisible();
  expect(screen.queryByRole('button', {name: 'Record feedback'})).not.toBeInTheDocument();
  expect(fetch).not.toHaveBeenCalled();
});

test('a network error preserves the draft without automatically retrying', async () => {
  fetch.mockRejectedValue(new Error('private network details'));
  render(<FeedbackForm matchRunId="run-1" candidates={candidates} />);
  await userEvent.selectOptions(screen.getByLabelText('Decision'), 'DEFERRED');
  await userEvent.type(screen.getByLabelText('Comment (optional)'), 'Keep me');
  await userEvent.click(screen.getByRole('button', {name: 'Record feedback'}));
  expect(await screen.findByRole('alert')).toHaveTextContent('Unable to confirm feedback was recorded');
  expect(screen.getByLabelText('Comment (optional)')).toHaveValue('Keep me');
  expect(fetch).toHaveBeenCalledTimes(1);
  expect(screen.queryByText('private network details')).not.toBeInTheDocument();
});
