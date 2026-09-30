# DOC-001 - Document Alpha installation, usage, and evidence

- **Domain:** documentation
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a reviewer, I want clear Alpha setup and usage documentation so that I can run the integrated prototype and verify its AI workflow without relying on tribal knowledge.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/assignments/unit5_alpha_acceptance.md`
- `resources/spec_bundle/project/architecture_contract.md`
- `resources/spec_bundle/api/api_contract.md`

## Scope

Update README and focused docs for uv setup, running FastAPI, running tests, starting the frontend when present, API/OpenAPI access, sample data, known Alpha limitations, and evidence locations.

## Non-scope

Claiming production readiness, deployed URLs, CI success, benchmark success, or completed features that have not been observed.

## Dependencies / preconditions

Commands must be validated against the current repository layout.

## Acceptance criteria

- **AC1:** A new contributor can identify prerequisites and exact setup/run/test commands.
- **AC2:** README reflects the canonical/current transitional structure accurately.
- **AC3:** Recommendation decision-support/human-authority boundary is stated.
- **AC4:** Known technical debt and incomplete features are linked rather than hidden.
- **AC5:** Observed CI/test/benchmark evidence is referenced where available.

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
