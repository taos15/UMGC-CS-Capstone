# TEST-003 - Evaluate curated Top-3 relevance

- **Domain:** testing
- **Phase:** Unit 8 Final
- **Priority:** Must
- **Status:** Ready

## User story

As the project team, I want reproducible curated relevance evaluation so that we can quantify whether acceptable employees appear in the top three recommendations.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/matching/evaluation_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`

## Scope

Create/version at least 15 curated job evaluation cases with manually designated acceptable employees and run the offline evaluator against the current `model_version`.

## Non-scope

Presenting curated relevance as production accuracy, training on evaluation labels during the same run, or fabricating expected employees after seeing results.

## Dependencies / preconditions

The finalized matching engine, versioned evaluation data, and offline evaluation runner are available.

## Acceptance criteria

- **AC1:** At least 15 curated jobs have pre-recorded acceptable-employee evidence.
- **AC2:** Evaluation reports how many jobs contain an acceptable employee in ranks 1-3 and the percentage.
- **AC3:** The result is compared to the >=12/15 (>=80%) target.
- **AC4:** Dataset/model version or hash and exact command/environment are recorded.
- **AC5:** Failure to meet target triggers documented analysis rather than hidden label/weight changes.

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
