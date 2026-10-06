import React from 'react';
import {render, screen, within} from '@testing-library/react';
import {test, expect} from 'vitest';
import RecommendationResults from './RecommendationResults';

const candidate = {
  rank: 1, employee_id: 'employee-1', score: 83.42, eligible: true,
  component_scores: {required_skills: .8, preferred_skills: .5, required_certifications: 1, experience: .9},
  matched_skills: ['wiring'], missing_skills: ['inspection'],
  matched_certifications: ['license'], missing_certifications: ['safety'],
  ineligible_reasons: [], explanation: 'Saved server explanation.',
};
const result = recommendations => ({match_run_id: 'run-1', model_version: 'rules-v1', recommendations});

test('renders canonical evidence and preserves server ordering without recalculating scores', () => {
  render(<RecommendationResults result={result([
    {...candidate, rank: 2, employee_id: 'server-first', score: 70},
    {...candidate, rank: 1, employee_id: 'server-second', score: 95},
  ])} />);
  const cards = screen.getAllByRole('article');
  expect(within(cards[0]).getByRole('heading', {name: 'Employee server-first'})).toBeVisible();
  expect(within(cards[0]).getByText('Rank 2')).toBeVisible();
  expect(within(cards[0]).getByText('70/100')).toBeVisible();
  expect(within(cards[1]).getByText('Rank 1')).toBeVisible();
  for (const label of ['Matched skills', 'Missing skills', 'Matched certifications', 'Missing certifications', 'Component scores', 'Explanation']) {
    expect(within(cards[0]).getByRole('heading', {name: label})).toBeVisible();
  }
  for (const evidence of ['wiring', 'inspection', 'license', 'safety', 'Saved server explanation.', 'Eligible']) {
    expect(within(cards[0]).getByText(evidence)).toBeVisible();
  }
  expect(within(cards[0]).getByText('0.8/1')).toBeVisible();
  expect(screen.getByText(/Supervisor retains final staffing authority/)).toBeVisible();
  expect(screen.getByText('run-1')).toBeVisible();
  expect(screen.getByText('rules-v1')).toBeVisible();
});

test('ineligible candidates expose the server reasons and explanation', () => {
  render(<RecommendationResults result={result([{...candidate, eligible: false, ineligible_reasons: ['Expired mandatory certification']}])} />);
  expect(screen.getByText('Ineligible')).toBeVisible();
  expect(screen.getByText('Expired mandatory certification')).toBeVisible();
});

test('empty results and empty evidence are explicit without inventing facts', () => {
  const view = render(<RecommendationResults result={result([])} />);
  expect(screen.getByText('No candidates meet these options.')).toBeVisible();
  view.rerender(<RecommendationResults result={result([{...candidate, matched_skills: [], missing_skills: [], matched_certifications: [], missing_certifications: [], component_scores: {}}])} />);
  expect(screen.getAllByText('None reported.')).toHaveLength(4);
  expect(screen.getByText('No component scores reported.')).toBeVisible();
});

test('malformed responses show an error instead of unsupported candidate facts', () => {
  render(<RecommendationResults result={result([{employeeId: 'legacy', score: 99}])} />);
  expect(screen.getByRole('alert')).toHaveTextContent('Recommendation evidence is unavailable');
  expect(screen.queryByRole('article')).not.toBeInTheDocument();
});

test('server text is displayed as text, never executed as markup', () => {
  render(<RecommendationResults result={result([{...candidate, explanation: '<script>malicious()</script>'}])} />);
  expect(screen.getByText('<script>malicious()</script>')).toBeVisible();
  expect(document.querySelector('script')).toBeNull();
});

for (const [field, value] of [
  ['employee_id', ''], ['rank', 0], ['rank', 1.5],
  ['score', -1], ['score', 101], ['score', '83.42'], ['score', NaN],
  ['eligible', 'true'], ['explanation', null],
  ['component_scores', []], ['component_scores', {experience: Infinity}],
  ['matched_skills', null], ['missing_skills', [42]],
  ['matched_certifications', 'license'], ['missing_certifications', [{}]],
  ['ineligible_reasons', undefined],
]) {
  test(`invalid ${field} rejects the entire evidence response`, () => {
    render(<RecommendationResults result={result([candidate, {...candidate, employee_id: 'employee-2', [field]: value}])} />);
    expect(screen.getByRole('alert')).toHaveTextContent('Recommendation evidence is unavailable');
    expect(screen.queryByRole('article')).not.toBeInTheDocument();
  });
}

for (const score of [0, 100]) {
  test(`score boundary ${score} renders all four server components`, () => {
    render(<RecommendationResults result={result([{...candidate, score}])} />);
    expect(screen.getByLabelText(`Score ${score} out of 100`)).toBeVisible();
    for (const name of ['Required skills', 'Preferred skills', 'Required certifications', 'Experience']) {
      expect(screen.getByText(name)).toBeVisible();
    }
    expect(screen.getByText('0.5/1')).toBeVisible();
    expect(screen.getByText('1/1')).toBeVisible();
    expect(screen.getByText('0.9/1')).toBeVisible();
  });
}
