# EVAL-001 - Evaluate matching offline without changing live behavior

- **Domain:** evaluation
- **Phase:** Unit 8 Final (Alpha evidence may begin earlier)
- **Priority:** Must
- **Status:** Ready

## User story

As the project team, I want a reproducible offline evaluation workflow so that we can compare recommendations with curated expected matches and supervisor feedback without online retraining.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/matching/evaluation_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`

## Scope

Implement evaluation script/data/reporting outside the production request path.

## Non-scope

Nightly continuous training, online learning, automatic config promotion.

## Dependencies / preconditions

Versioned expected cases and stable `model_version`.

## Acceptance criteria

- **AC1:** Evaluation records dataset/model version and reproducible metrics.
- **AC2:** Top-3 relevance/recall is measured against the project target.
- **AC3:** Supervisor feedback may be analyzed offline but never mutates the live matcher automatically.
- **AC4:** Any scoring/config change requires explicit versioning/review/regression tests.

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
