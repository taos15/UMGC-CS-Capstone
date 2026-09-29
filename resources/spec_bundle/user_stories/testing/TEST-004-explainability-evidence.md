# TEST-004 - Verify explanation evidence completeness

- **Domain:** testing
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want every returned recommendation to contain traceable match evidence so that rankings are explainable instead of opaque scores.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`
- `resources/spec_bundle/data/data_contract.md`

## Scope

Add automated checks over representative recommendation responses for component scores, matched/missing evidence, eligibility reasons, and explanation consistency.

## Non-scope

LLM-generated rationale, unsupported skill claims, or UI-only checks that bypass server response evidence.

## Dependencies / preconditions

`MATCH-004` and `REC-001` are implemented.

## Acceptance criteria

- **AC1:** Automated tests require evidence fields for every returned result.
- **AC2:** Matched/missing evidence agrees with the structured input facts used by matching.
- **AC3:** Explanation text/templates do not introduce unsupported skills/certifications.
- **AC4:** Observed completeness is summarized and compared to the 100% target.

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
