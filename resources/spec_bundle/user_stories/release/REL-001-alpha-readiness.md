# REL-001 - Verify Unit 5 Alpha release readiness

- **Domain:** release
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As the project team, I want an evidence-backed Alpha release gate so that the submitted repository demonstrates integrated MVP behavior instead of a collection of disconnected modules.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/assignments/unit5_alpha_acceptance.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Execute the Alpha checklist across core MVP workflow, AI operation, module integration, CI, error/security behavior, benchmark evidence, documentation, peer review, technical debt, and version-control evidence.

## Non-scope

Unit 8-only portfolio work unless explicitly requested; fabricated CI/review/benchmark evidence.

## Dependencies / preconditions

All Must Unit 5 stories required for the chosen Alpha scope are either Done or explicitly blocked with documented impact.

## Acceptance criteria

- **AC1:** Core recommendation workflow operates end-to-end in the Alpha environment.
- **AC2:** AI matching is functional and evidence/explanations are returned.
- **AC3:** Relevant CI/test results are observed and recorded.
- **AC4:** Documentation contains installation/usage instructions.
- **AC5:** Peer-review and technical-debt deliverables are based on real evidence.
- **AC6:** Release checklist records blockers/known limitations rather than hiding them.

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
