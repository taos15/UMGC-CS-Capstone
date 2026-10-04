# UI-005 - Record supervisor feedback from a stored match run

- **Domain:** frontend
- **Phase:** Unit 5 Alpha
- **Priority:** Should
- **Status:** Ready

## User story

As a supervisor, I want to record `SELECTED`, `NOT_SELECTED`, or `DEFERRED` feedback for a stored recommendation run so that the team can audit and evaluate recommendation usefulness.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Implement feedback controls tied to the returned `match_run_id` and submit the canonical feedback contract.

## Non-scope

Automatically changing model weights, assigning an employee, or treating feedback as online training.

## Dependencies / preconditions

`FDBK-001` feedback endpoint and immutable match-run identity are implemented.

## Acceptance criteria

- **AC1:** Feedback is submitted against the exact stored `match_run_id`.
- **AC2:** Only canonical decision values are sent.
- **AC3:** Selected employee identifiers are only sent when allowed by the finalized feedback schema.
- **AC4:** Success/failure state is communicated clearly and duplicate/conflicting feedback follows canonical API behavior.
- **AC5:** UI copy does not imply that feedback instantly retrains the matcher.

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
