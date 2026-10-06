# ERR-001 - Return stable RFC 9457-style problem details

- **Domain:** errors
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an API client developer, I want stable machine-readable problem details so that the React client can handle validation, auth, conflict, not-found, and dependency failures predictably.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/error_contract.md`
- `resources/spec_bundle/api/api_contract.md`

## Scope

Implement centralized problem-response translation and stable error codes.

## Non-scope

Exposing internal stack traces/database details.

## Dependencies / preconditions

Central error mapping location under canonical architecture.

## Acceptance criteria

- **AC1:** Canonical errors use `application/problem+json`.
- **AC2:** Body includes stable `code`, `request_id`, `detail`, and field errors when relevant.
- **AC3:** Status/code mappings follow `error_contract.md`.
- **AC4:** Internal failures never expose stack/database details.

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
