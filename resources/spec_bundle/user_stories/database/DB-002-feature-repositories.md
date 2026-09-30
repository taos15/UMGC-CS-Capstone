# DB-002 - Use feature-local repository boundaries

- **Domain:** database
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a maintainer, I want feature-local repositories so that persistence changes do not leak raw SQL/ORM behavior into routers or the matching engine.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/project/architecture_contract.md`
- `resources/spec_bundle/data/data_contract.md`

## Scope

Create repositories only for features that persist data: auth/skills/employees/jobs/recommendations/feedback as needed.

## Non-scope

A generic repository framework or repository inside matching.

## Dependencies / preconditions

Canonical database/session boundary.

## Acceptance criteria

- **AC1:** Persistent features use feature-local repositories where needed.
- **AC2:** Routers do not issue raw persistence queries.
- **AC3:** Matching never queries repositories/database directly.
- **AC4:** Repository tests cover core query/transaction behavior.

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
