# DB-001 - Establish canonical database/session infrastructure

- **Domain:** database
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a project contributor, I want one configurable database/session boundary so that features persist data consistently instead of depending on global in-memory objects.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/project/architecture_contract.md`
- `resources/spec_bundle/project/migration_contract.md`
- `resources/spec_bundle/data/data_contract.md`

## Scope

Move/create shared engine/session/base under `backend/src/skillmatch/db/` and externalize database configuration.

## Non-scope

Feature business rules inside shared DB infrastructure.

## Dependencies / preconditions

Characterize the latest current database setup before moving.

## Acceptance criteria

- **AC1:** Shared engine/session setup lives under canonical `skillmatch/db/` after migration.
- **AC2:** Features receive repository/session dependencies rather than importing global seed lists.
- **AC3:** Database configuration is externalized and secrets are not committed.
- **AC4:** Current local/CI database behavior remains testable during migration.

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
