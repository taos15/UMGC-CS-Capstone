# SKILL-001 - List and search the controlled skill taxonomy

- **Domain:** skills
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an authorized SkillMatch user, I want to browse/search the controlled skill taxonomy so that employees and jobs reference consistent skill identifiers.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`

## Scope

Implement `GET /api/v1/skills` for ADMIN/SUPERVISOR/VIEWER through the Skills feature boundary.

## Non-scope

Free-text skill extraction, taxonomy learning, or external taxonomy synchronization.

## Dependencies / preconditions

Exact Skill object fields and search parameters are underspecified; use current tested behavior or approve an amendment.

## Acceptance criteria

- **AC1:** Authorized roles can list/search skills through `/api/v1/skills`.
- **AC2:** Returned skill identifiers are usable by employee/job contracts.
- **AC3:** Pagination follows shared conventions when paginated.
- **AC4:** Unauthorized access follows canonical auth/error behavior.

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

Stop if implementing search requires undocumented query parameters and no tested current behavior exists; amend the contract first.
