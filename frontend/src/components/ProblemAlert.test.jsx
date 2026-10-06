import React from 'react';
import {render, screen} from '@testing-library/react';
import {expect, test} from 'vitest';
import ProblemAlert, {uiProblem} from './ProblemAlert';
import {ApiError} from '../api/client';

for (const [status, code, text] of [[503, 'DATABASE_UNAVAILABLE', 'database is temporarily unavailable'], [503, 'MATCH_ENGINE_UNAVAILABLE', 'Matching is temporarily unavailable'], [409, 'JOB_NOT_OPEN', 'no longer OPEN'], [422, 'JOB_HAS_NO_CRITERIA', 'no usable matching criteria'], [500, 'INTERNAL_ERROR', 'Something went wrong']]) {
  test(`${code} renders safe guidance and request correlation`, () => {
    const error = new ApiError(status, {code, detail: 'private SQL or stack trace', request_id: 'trace-42'});
    render(<ProblemAlert error={uiProblem(error, 'Please try again.')} />);
    expect(screen.getByRole('alert')).toHaveTextContent(text);
    expect(screen.getByText('Request ID: trace-42')).toBeVisible();
    expect(screen.queryByText(/private SQL/)).not.toBeInTheDocument();
  });
}

test('422 field issues link to the affected input without exposing raw messages', () => {
  const error = new ApiError(422, {code: 'VALIDATION_ERROR', field_errors: [null, {field: 'body.top_k', message: 'private validation context'}, {field: 'body.minimumScore'}, {field: '<script>private</script>'}]});
  render(<><input id="top-k" /><ProblemAlert error={uiProblem(error, 'Review your options.')} fieldTargets={{top_k: 'top-k'}} /></>);
  expect(screen.getByRole('link', {name: 'Check Maximum results.'})).toHaveAttribute('href', '#top-k');
  expect(screen.getByText('Check Minimum score.')).toBeVisible();
  expect(screen.queryByText(/private/)).not.toBeInTheDocument();
});

test('403 excludes server field errors and protected details', () => {
  const error = new ApiError(403, {detail: 'private employee name', field_errors: [{field: 'body.private_employee'}]});
  render(<ProblemAlert error={uiProblem(error, 'You do not have permission.')} />);
  expect(screen.getByRole('alert')).toHaveTextContent('You do not have permission');
  expect(screen.queryByText(/private/)).not.toBeInTheDocument();
});
