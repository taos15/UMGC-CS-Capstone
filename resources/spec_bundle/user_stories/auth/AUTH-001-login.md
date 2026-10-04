# AUTH-001 - Exchange local credentials for a short-lived bearer token

- **Domain:** auth
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an authorized SkillMatch user, I want to log in and receive a short-lived bearer token so that protected workforce data and recommendation actions are not anonymously accessible.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/api/error_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Implement `POST /api/v1/auth/login` and safe credential-failure behavior.

## Non-scope

SSO, MFA, password reset, or production enterprise IAM.

## Dependencies / preconditions

The Project Design Specification does not define exact credential field names/token response shape; preserve tested current behavior or approve an amendment first.

## Acceptance criteria

- **AC1:** Valid local credentials return a short-lived bearer token from the canonical endpoint.
- **AC2:** Invalid credentials return generic `AUTH_INVALID_CREDENTIALS` behavior without revealing which credential failed.
- **AC3:** Protected endpoints reject missing/invalid tokens with canonical 401 behavior.
- **AC4:** No real secrets or plaintext production credentials are committed.

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

Stop if no credential/token schema exists in current code/tests and no approved amendment defines one; do not invent a public auth schema silently.
