# JOB-003 - Create a match-ready structured job profile

- **Domain:** jobs
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an administrator, I want to create a structured job with required/preferred skills, certification rules, and minimum experience so that supervisors can request consistent recommendations.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/api/error_contract.md`

## Scope

Implement `POST /api/v1/jobs` and match-readiness validation.

## Non-scope

Location/schedule optimization, automatic assignment, training catalog workflow.

## Dependencies / preconditions

Referenced skills/certification rules must satisfy finalized domain validation.

## Acceptance criteria

- **AC1:** ADMIN can create a valid job and receive 201.
- **AC2:** Duplicate `job_code` returns a stable conflict.
- **AC3:** Skill requirements enforce REQUIRED/PREFERRED, proficiency 1-5, importance 1-3.
- **AC4:** An `OPEN` job with no usable criteria is rejected using canonical `JOB_HAS_NO_CRITERIA`/validation behavior.
- **AC5:** Non-ADMIN callers are forbidden.

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
