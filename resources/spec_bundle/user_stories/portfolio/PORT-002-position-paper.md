# PORT-002 - Draft the evidence-based 1,300-word professional position paper

- **Domain:** portfolio
- **Phase:** Unit 8 Final
- **Priority:** Must
- **Status:** Ready

## User story

As an individual team member, I want a source- and evidence-grounded position paper so that I can critically evaluate system delivery, engineering methodology, and my professional growth plan.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/assignments/unit8_final_acceptance.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Draft the 1,300-word individual paper: approximately 400 words on delivery/integration, 450 on methodology/performance with quantitative evidence and industry standards, and 450 on professional-development roadmap with current authoritative trend sources.

## Non-scope

Fabricating personal contributions, metrics, team outcomes, peer feedback, or external-source conclusions.

## Dependencies / preconditions

The writer must supply/confirm their actual contributions and professional-development interests; final repository metrics/evidence must exist; external sources must be current and cited.

## Acceptance criteria

- **AC1:** The paper totals approximately 1,300 words with the required 400/450/450 section allocation.
- **AC2:** Section 1 cites concrete repository/development examples.
- **AC3:** Section 2 uses observed quantitative evidence and authoritative SEI/IEEE/equivalent standards.
- **AC4:** Section 3 identifies specific future technologies/methodologies/skills and supports them with current authoritative trend sources.
- **AC5:** Claims about personal/team work are truthful and traceable.

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

Stop and ask for missing personal contribution/career-goal facts instead of inventing them. Use current authoritative web research for industry/trend claims when drafting the final paper.
