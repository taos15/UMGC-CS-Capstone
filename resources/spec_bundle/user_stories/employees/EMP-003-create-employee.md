# EMP-003 - Create a structured employee profile

- **Domain:** employees
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an administrator, I want to create a structured employee profile so that SkillMatch has validated skills, certifications, experience, and status evidence for matching.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/api/error_contract.md`

## Scope

Implement `POST /api/v1/employees` with structured validation.

## Non-scope

Resume/free-text NLP or automatic skill inference.

## Dependencies / preconditions

Referenced skills must satisfy the finalized taxonomy/data model.

## Acceptance criteria

- **AC1:** ADMIN can create a valid profile and receive 201.
- **AC2:** Non-ADMIN callers are forbidden.
- **AC3:** Duplicate `employee_number` returns a stable conflict.
- **AC4:** Proficiency is 1-5 and certification/date relationships are validated.
- **AC5:** Protected personal characteristics are not introduced into matching inputs.

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
