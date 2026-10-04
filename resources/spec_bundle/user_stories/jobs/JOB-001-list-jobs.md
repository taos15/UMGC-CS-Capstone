# JOB-001 - List and filter job profiles

- **Domain:** jobs
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an authorized workforce user, I want to list/filter job profiles so that I can select an `OPEN` job and inspect its structured requirements.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/api/error_contract.md`

## Scope

Implement `GET /api/v1/jobs`.

## Non-scope

Location/schedule/training-catalog optimization.

## Dependencies / preconditions

Job repository and authorization context.

## Acceptance criteria

- **AC1:** ADMIN/SUPERVISOR/VIEWER can list authorized jobs.
- **AC2:** Responses expose structured required/preferred criteria.
- **AC3:** Pagination follows shared conventions.
- **AC4:** Filters are added only when defined by current tests/OpenAPI or an approved amendment.

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
