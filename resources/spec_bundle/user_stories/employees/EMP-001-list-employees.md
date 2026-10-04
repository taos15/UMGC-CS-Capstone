# EMP-001 - List and filter employee profiles

- **Domain:** employees
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an authorized workforce user, I want to list/filter employee profiles so that I can inspect the structured evidence used by recommendations.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/api/error_contract.md`

## Scope

Implement `GET /api/v1/employees` through employee service/repository boundaries.

## Non-scope

Self-service employee editing or production HRIS synchronization.

## Dependencies / preconditions

Employee persistence/repository boundary must exist or be introduced by this slice.

## Acceptance criteria

- **AC1:** ADMIN/SUPERVISOR/VIEWER can retrieve authorized employee profiles.
- **AC2:** Responses use canonical EmployeeProfile vocabulary and do not add protected characteristics.
- **AC3:** Pagination uses `page >= 1`, `page_size` 1-100, default 25.
- **AC4:** Runtime reads do not depend on global in-memory seed lists once persistence is enabled.

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
