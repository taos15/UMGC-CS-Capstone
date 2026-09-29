# DB-003 - Use PostgreSQL with reproducible Alembic migrations

- **Domain:** database
- **Phase:** Unit 8 Final (Alpha migration may begin earlier)
- **Priority:** Must
- **Status:** Ready

## User story

As a project maintainer, I want PostgreSQL schema changes versioned through migrations so that the final prototype matches the approved persistence target and can be created reproducibly.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/project/architecture_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Complete PostgreSQL configuration and Alembic migrations for canonical persistent models.

## Non-scope

Production HA/replication/managed-cloud operations.

## Dependencies / preconditions

Persistent feature models must be stable enough to migrate.

## Acceptance criteria

- **AC1:** PostgreSQL is the documented final database target.
- **AC2:** Alembic can create/upgrade the schema from an empty database.
- **AC3:** Unique keys, relationships, and needed indexes are migration-controlled.
- **AC4:** Any SQLite Alpha shortcut is removed or explicitly documented as transitional technical debt.

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
