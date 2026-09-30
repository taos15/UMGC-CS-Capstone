# TEST-005 - Verify deterministic matching reproducibility

- **Domain:** testing
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a maintainer, I want identical input snapshots and `model_version` to produce identical rankings and scores so that recommendation results are reproducible and auditable.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`
- `resources/spec_bundle/data/data_contract.md`

## Scope

Add deterministic repeated-run tests around matching and stored snapshot/version identifiers.

## Non-scope

Claiming determinism across different data/model versions or relying on database row order as a tie-break.

## Dependencies / preconditions

Matching tie-break and model-version contracts are implemented.

## Acceptance criteria

- **AC1:** Repeated matching of the same normalized input DTOs and model version produces identical result order and numeric scores.
- **AC2:** Tie cases follow score -> required-skill coverage -> certification coverage -> employee_id.
- **AC3:** Tests do not depend on incidental database insertion order.
- **AC4:** Any randomized library behavior is fixed/removed from the MVP matching path.

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
