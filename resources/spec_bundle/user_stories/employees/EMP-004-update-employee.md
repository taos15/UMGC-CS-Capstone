# EMP-004 - Update an employee profile with optimistic versioning

- **Domain:** employees
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an administrator, I want to update employee evidence with optimistic versioning so that stale edits do not overwrite newer workforce data.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/api/error_contract.md`

## Scope

Implement canonical `PUT /api/v1/employees/{employee_id}` replacement semantics for editable fields.

## Non-scope

PATCH semantics unless added by approved contract amendment.

## Dependencies / preconditions

Employee persistence includes server version/conflict detection.

## Acceptance criteria

- **AC1:** Valid ADMIN update persists and returns the revised profile.
- **AC2:** Missing employee returns `EMPLOYEE_NOT_FOUND`.
- **AC3:** Stale `version` returns `409 STALE_VERSION`.
- **AC4:** Updated skill/certification/status/experience evidence reuses create validation rules.

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
