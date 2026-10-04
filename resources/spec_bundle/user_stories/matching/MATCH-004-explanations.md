# MATCH-004 - Build evidence-based recommendation explanations

- **Domain:** matching
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want each ranked result to explain matched requirements, gaps, and component scores so that I can review evidence instead of trusting an opaque score.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`

## Scope

Build deterministic template/structured explanations from matching evidence.

## Non-scope

Generative LLM explanations or unsupported inferred skills.

## Dependencies / preconditions

Eligibility/scoring output contains matched/missing evidence and component values.

## Acceptance criteria

- **AC1:** Every result contains component scores.
- **AC2:** Matched/missing skills/certifications are grounded in input evidence.
- **AC3:** Eligibility reasons are explicit.
- **AC4:** Explanation contains no unsupported skill claim.
- **AC5:** No generative model is required/called for MVP explanations.

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
