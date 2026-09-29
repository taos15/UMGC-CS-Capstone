# UI-002 - Authenticate from the supervisor portal

- **Domain:** frontend
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an authorized SkillMatch user, I want to log in from the portal so that protected workforce functions use a bearer-authenticated session.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/api/error_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Implement the login form/client flow for `POST /api/v1/auth/login`, safe token handling appropriate to the prototype, authenticated API calls, and generic login failure messaging.

## Non-scope

Identity federation, password-reset flows, production SSO, or browser authorization as a substitute for backend RBAC.

## Dependencies / preconditions

`AUTH-001` and `AUTH-002` backend behavior must be available or mocked only through contract-faithful test doubles.

## Acceptance criteria

- **AC1:** Valid credentials transition the UI to authenticated application state and subsequent protected calls include the bearer token.
- **AC2:** Invalid credentials show a generic error without leaking credential details.
- **AC3:** Logout/session clearing removes the local authentication state.
- **AC4:** Frontend tests cover success and failure behavior without asserting secrets.

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
