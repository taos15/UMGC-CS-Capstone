# PORT-001 - Prepare the 10-15 minute technical stakeholder presentation

- **Domain:** portfolio
- **Phase:** Unit 8 Final
- **Priority:** Must
- **Status:** Ready

## User story

As the project team, I want a concise evidence-based technical presentation so that senior technical stakeholders can understand SkillMatch AI, see the AI workflow live, and evaluate its engineering value.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/assignments/unit8_final_acceptance.md`
- `resources/spec_bundle/project/project_design_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`

## Scope

Prepare/demo the required problem statement, solution architecture, AI integration/value, implementation decisions, observed performance/reliability metrics, and stakeholder value within 10-15 minutes.

## Non-scope

Invented metrics, prerecorded behavior represented as live when it is not, or claims inconsistent with repository evidence.

## Dependencies / preconditions

Final repository/evidence must be stable enough to demonstrate; team contributions must be known.

## Acceptance criteria

- **AC1:** Presentation duration is 10-15 minutes.
- **AC2:** Architecture walkthrough matches the final feature-oriented implementation and distinct matcher boundary.
- **AC3:** AI demonstration shows structured input, ranking/evidence, and supervisor decision control.
- **AC4:** All metrics shown are traceable to final evidence.
- **AC5:** The value proposition is tied to actual implemented capability and limitations.

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
