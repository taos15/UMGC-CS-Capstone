# MATCH-001 - Evaluate candidate eligibility before ranking

- **Domain:** matching
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want ineligible employees identified consistently so that inactive employees or candidates missing mandatory credentials are not presented as eligible.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`
- `resources/spec_bundle/data/data_contract.md`

## Scope

Implement pure eligibility evaluation for active status and mandatory certification validity.

## Non-scope

Hard-excluding candidates merely for missing required skills.

## Dependencies / preconditions

Immutable Employee/Job DTOs with status/certification evidence.

## Acceptance criteria

- **AC1:** Non-ACTIVE employees are ineligible.
- **AC2:** Missing or expired mandatory certification makes a candidate ineligible.
- **AC3:** Missing required skill remains a scored gap, not automatic hard exclusion.
- **AC4:** Eligibility returns stable reasons/evidence for CandidateResult.

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
