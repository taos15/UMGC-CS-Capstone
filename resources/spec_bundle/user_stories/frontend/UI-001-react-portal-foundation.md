# UI-001 - Establish the React supervisor portal foundation

- **Domain:** frontend
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want a usable React portal that communicates with the canonical `/api/v1` backend so that I can complete the recommendation workflow without calling endpoints manually.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/project/architecture_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`
- `resources/spec_bundle/api/api_contract.md`

## Scope

Create the React application shell, routing, shared API client boundary, environment-based backend URL, and accessible loading/error foundations under `frontend/`.

## Non-scope

Feature-specific employee/job management screens beyond the Alpha workflow; scoring formulas in the browser; browser-side authorization decisions.

## Dependencies / preconditions

The backend API contract is stable enough for the client to consume. Do not duplicate backend business rules in TypeScript.

## Acceptance criteria

- **AC1:** React runs from the documented frontend command and renders an application shell.
- **AC2:** All backend requests go through a shared typed API-client boundary using `/api/v1` contracts.
- **AC3:** The client does not implement scoring, raw SQL, or authoritative role decisions.
- **AC4:** Configuration does not hard-code a production backend URL.
- **AC5:** Frontend setup and run instructions are documented.

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
