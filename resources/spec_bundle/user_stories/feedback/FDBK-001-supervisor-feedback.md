# FDBK-001 - Record supervisor feedback against a stored match run

- **Domain:** feedback
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want to record `SELECTED`, `NOT_SELECTED`, or `DEFERRED` feedback against a recommendation run so that the human decision is auditable and useful for offline evaluation without automating staffing.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/api/error_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`
- `resources/spec_bundle/matching/evaluation_contract.md`

## Scope

Implement `POST /api/v1/match-runs/{match_run_id}/feedback` through the distinct Feedback/Audit feature.

## Non-scope

Automatic assignment, automatic scoring-weight changes, or online retraining.

## Dependencies / preconditions

Stored match run and authenticated ADMIN/SUPERVISOR context.

## Acceptance criteria

- **AC1:** ADMIN/SUPERVISOR can record canonical feedback for an existing authorized run.
- **AC2:** Feedback references the run/caller and selected employee only when valid for that run/decision.
- **AC3:** Conflicting/invalid feedback returns canonical validation or `FEEDBACK_CONFLICT` behavior.
- **AC4:** Feedback is auditable but never changes live matching automatically.
- **AC5:** Feedback can be used by separate offline evaluation.

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
