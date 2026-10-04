# ERR-002 - Trace every API response with X-Request-ID

- **Domain:** errors
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a maintainer, I want every API response traceable by request ID so that failures and recommendation runs can be correlated during testing and review.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/api/error_contract.md`

## Scope

Generate/propagate request IDs in middleware/request context and include them in headers/errors.

## Non-scope

Distributed tracing platform integration.

## Dependencies / preconditions

FastAPI request middleware/context.

## Acceptance criteria

- **AC1:** Every response includes `X-Request-ID`.
- **AC2:** Problem-detail `request_id` matches the response trace ID.
- **AC3:** Request ID is available to logs/error handling without leaking sensitive data.
- **AC4:** Recommendation responses still expose `match_run_id` and `model_version` separately.

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
