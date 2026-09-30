# UI-006 - Handle loading, empty, and typed error states

- **Domain:** frontend
- **Phase:** Unit 5 Alpha
- **Priority:** Should
- **Status:** Ready

## User story

As a supervisor, I want clear loading, empty, validation, authorization, and dependency-failure states so that the portal remains understandable when a workflow cannot complete.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/error_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Implement reusable user-facing states for the recommendation workflow and critical workforce requests using canonical problem details and request IDs.

## Non-scope

Displaying stack traces, database details, bearer tokens, or raw internal exception messages.

## Dependencies / preconditions

Canonical problem-details handling exists in the backend/client boundary.

## Acceptance criteria

- **AC1:** Loading and empty-result states are distinguishable from errors.
- **AC2:** 401/403 behavior does not reveal protected resource data.
- **AC3:** 422 field errors are presented at an actionable location when available.
- **AC4:** 500/503 messages remain safe and expose/request a `request_id` for support correlation where provided.
- **AC5:** Frontend tests cover representative success, validation, authorization, and dependency-failure rendering.

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
