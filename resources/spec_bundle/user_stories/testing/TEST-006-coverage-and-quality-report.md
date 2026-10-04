# TEST-006 - Produce final testing and code-quality evidence

- **Domain:** testing
- **Phase:** Unit 8 Final
- **Priority:** Must
- **Status:** Ready

## User story

As the project team, I want reproducible coverage and code-quality evidence so that the final portfolio demonstrates implementation quality with observed data.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/assignments/unit8_final_acceptance.md`
- `resources/spec_bundle/quality/quality_contract.md`

## Scope

Run the agreed automated test/coverage and code-quality tooling against the final repository and store commands, versions, and reports/screenshots needed for the portfolio.

## Non-scope

Invented percentages, cherry-picked passing commands while hiding failures, or adding heavyweight tooling without a demonstrated need.

## Dependencies / preconditions

Final code and test suites are stable enough for portfolio measurement.

## Acceptance criteria

- **AC1:** The exact coverage/tool commands and versions are recorded.
- **AC2:** Reports reflect the complete intended test suite, not only a convenient subset.
- **AC3:** Any failing checks/known exclusions are disclosed.
- **AC4:** Evidence is stored under `docs/evidence/unit8/` and referenced from final documentation.

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
