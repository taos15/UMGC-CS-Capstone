# CI-002 - Complete final CI/CD and deployment evidence

- **Domain:** cicd
- **Phase:** Unit 8 Final
- **Priority:** Must
- **Status:** Ready

## User story

As the project team, I want documented successful CI and deployment evidence so that the final portfolio demonstrates repeatable delivery rather than only local execution.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/assignments/unit8_final_acceptance.md`
- `resources/spec_bundle/quality/quality_contract.md`

## Scope

Finalize the agreed CI/CD/deployment workflow, execute it, and capture traceable evidence/screenshots/configuration references for the final portfolio.

## Non-scope

Fabricated screenshots, unobserved deployment success, or unnecessary production infrastructure beyond the project target.

## Dependencies / preconditions

A deployment target/approach must be explicitly agreed before implementation if the repository does not already define one.

## Acceptance criteria

- **AC1:** The final CI workflow runs the intended automated test/check suite.
- **AC2:** Deployment steps are documented and repeatable for the chosen target.
- **AC3:** Successful runs/deployment are evidenced with dates/identifiers or screenshots.
- **AC4:** Failures/limitations are disclosed instead of represented as success.
- **AC5:** Evidence is linked from final documentation.

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
