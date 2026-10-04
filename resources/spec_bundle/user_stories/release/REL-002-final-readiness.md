# REL-002 - Verify Unit 8 final repository readiness

- **Domain:** release
- **Phase:** Unit 8 Final
- **Priority:** Must
- **Status:** Ready

## User story

As the project team, I want a final evidence-backed release gate so that the portfolio repository is fully integrated, documented, tested, and ready for stakeholder demonstration.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/assignments/unit8_final_acceptance.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Run final repository checks covering complete workflow, AI value, database/migrations, frontend/backend integration, tests/coverage, performance/relevance/reproducibility, CI/CD evidence, documentation, version-control/collaboration evidence, and known defects.

## Non-scope

Inventing production-readiness evidence or automatically proceeding into presentation/paper work before the final repository evidence exists.

## Dependencies / preconditions

Unit 5 Alpha completed; final hardening stories and observed evidence are available.

## Acceptance criteria

- **AC1:** All core final requirements operate together with no known critical defect left undocumented.
- **AC2:** Final automated test/coverage/performance/relevance evidence is current and referenced.
- **AC3:** CI/CD/deployment evidence is current and traceable.
- **AC4:** README/API/install/user-manual documentation is complete.
- **AC5:** Individual contributions/collaboration evidence is documented.
- **AC6:** Remaining limitations are explicit and consistent with the final presentation/paper.

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
