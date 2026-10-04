# DEBT-001 - Track and mitigate concrete technical debt

- **Domain:** review
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As the project team, I want deliberate shortcuts recorded with impact and mitigation so that Alpha speed does not obscure reliability and maintenance costs.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/assignments/unit5_alpha_acceptance.md`
- `resources/spec_bundle/project/migration_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`

## Scope

Maintain a technical-debt record for actual shortcuts such as transitional `app/` compatibility, Alpha SQLite/direct table creation if retained, incomplete migration tooling, temporary mock data, or other observed debt.

## Non-scope

Inventing debt that does not exist, treating every unfinished feature as debt, or silently converting a scope decision into a defect.

## Dependencies / preconditions

Debt entries must be grounded in current code/PR decisions and distinguish deliberate scope from unwanted shortcuts.

## Acceptance criteria

- **AC1:** Each debt item states the shortcut/current state, immediate benefit, long-term cost/risk, affected areas, and mitigation/retirement plan.
- **AC2:** At least the debt discussed in the Unit 5 report is traceable to repository evidence.
- **AC3:** Resolved items record how/when they were retired.
- **AC4:** Unresolved high-risk security/reliability debt is not hidden behind release language.

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
