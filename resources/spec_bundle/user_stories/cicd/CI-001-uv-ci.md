# CI-001 - Keep GitHub Actions aligned with the uv project

- **Domain:** cicd
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a contributor, I want pull requests and `dev`/`main` pushes to install from the committed uv project and run automated tests so that integration failures are caught consistently.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/assignments/unit5_alpha_acceptance.md`
- `resources/spec_bundle/project/architecture_contract.md`

## Scope

Maintain the repository GitHub Actions CI around root `pyproject.toml`, `.python-version`, and `uv.lock`, using the locked uv environment and test suite.

## Non-scope

Parallel requirements files as a second dependency source, claims that CI passed without observing a run, or deployment automation not required for Alpha.

## Dependencies / preconditions

The latest `dev` already contains the root uv files and a CI workflow; preserve/refine rather than replace without reason.

## Acceptance criteria

- **AC1:** CI checks out code and installs/configures uv.
- **AC2:** CI uses the committed project lock consistently and runs the repository test command.
- **AC3:** Dependency changes update `pyproject.toml` and `uv.lock` together.
- **AC4:** CI failures remain visible and are not suppressed to satisfy the rubric.
- **AC5:** README/team workflow states the matching local command.

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
