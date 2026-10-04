# MATCH-003 - Rank candidates deterministically

- **Domain:** matching
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want recommendation order deterministic so that the same evidence and model version reproduce the same results.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`
- `resources/spec_bundle/data/data_contract.md`

## Scope

Apply eligibility/options/filtering and canonical tie-break order.

## Non-scope

Random tie-breaking, personalization, online learning.

## Dependencies / preconditions

Eligibility and scoring functions.

## Acceptance criteria

- **AC1:** Eligibility and `include_ineligible` are respected.
- **AC2:** `minimum_score` is respected.
- **AC3:** Tie-break order is final score, required-skill coverage, certification coverage, employee_id.
- **AC4:** No more than `max_results` are returned.
- **AC5:** Identical input snapshot + model version produces identical order/scores.

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
