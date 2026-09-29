# UI-003 - Select an OPEN job and request recommendations

- **Domain:** frontend
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want to select an `OPEN` job and request recommendations so that I can evaluate employees for that job.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Implement job selection plus recommendation-options input and call `POST /api/v1/jobs/{job_id}/recommendations` through the typed API client.

## Non-scope

Automatic assignment, location/schedule optimization, or client-side recomputation of recommendation scores.

## Dependencies / preconditions

Jobs listing/retrieval and `REC-001` recommendation API are implemented or available through contract-faithful tests.

## Acceptance criteria

- **AC1:** The UI lists/selects authorized jobs and clearly identifies the selected job.
- **AC2:** Submitting a recommendation request uses snake_case contract fields and the canonical endpoint.
- **AC3:** The UI supports canonical recommendation options without inventing undocumented defaults.
- **AC4:** The UI prevents accidental duplicate submission while a request is in flight.
- **AC5:** Authorization/validation failures are displayed using safe problem details.

## TDD contract

### RED

Add the smallest focused test/check that fails for the unmet acceptance criterion for the expected reason. If the behavior already exists, add characterization/contract coverage rather than manufacturing a false failure.

### GREEN

Implement the minimum change required by the acceptance criteria while preserving architecture, API, data, matching, authorization, and persistence boundaries.

### REFACTOR

Improve naming, cohesion, duplication, and test setup without changing observable behavior. Re-run focused checks and then the relevant full suite.

## Completion evidence

- Exact changed files.
- Exact commands/checks run and observed results.
- Updated OpenAPI/docs/contracts when externally visible behavior changes.
- Deliberate shortcuts recorded in `docs/technical_debt/` or equivalent evidence.

## Definition of Done

Every acceptance criterion is objectively verified; relevant focused and regression tests pass; no unrelated contract regresses; no unobserved CI/deployment/review/metric claim is made.

## Stop conditions

Stop instead of guessing if current code/tests contradict a canonical contract, another unmerged change owns the same paths, or the story requires an unrelated public-contract change.
