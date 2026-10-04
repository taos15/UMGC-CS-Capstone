# TEST-001 - Organize unit, integration, and contract test suites

- **Domain:** testing
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a maintainer, I want tests separated by responsibility so that pure logic, integrated boundaries, and approved public contracts can fail independently and explain what regressed.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/project/architecture_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`

## Scope

Create/normalize `tests/unit/`, `tests/integration/api/`, `tests/integration/database/`, and `tests/contract/` and migrate/add tests without weakening existing coverage.

## Non-scope

Arbitrary coverage-percentage gates not required by the Project Design Specification; deleting working tests simply because paths change.

## Dependencies / preconditions

Canonical backend package migration may be incremental; tests must support compatibility while migration is in progress.

## Acceptance criteria

- **AC1:** Pure matching/domain logic is testable without FastAPI or a live database where the contract allows.
- **AC2:** API/database integration tests exercise real boundaries using isolated test state.
- **AC3:** Contract tests protect endpoint names, snake_case shapes, role behavior, and problem-details conventions that are implemented.
- **AC4:** Existing meaningful tests remain represented after reorganization.
- **AC5:** CI executes the intended test collection through the repository uv environment.

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
