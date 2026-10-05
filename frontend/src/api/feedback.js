import {apiRequest} from './client';

export const recordFeedback = (matchRunId, body) =>
  apiRequest(`/match-runs/${encodeURIComponent(matchRunId)}/feedback`, {method: 'POST', body});
