# REC-001 - Generate a recommendation run for an OPEN job

- **Domain:** recommendations
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want ranked employees for an `OPEN` job so that I can compare candidates using skills, certifications, experience, and explainable evidence.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`
- `resources/spec_bundle/api/error_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Implement `POST /api/v1/jobs/{job_id}/recommendations` as the orchestration boundary.

## Non-scope

Automatic assignment or online model changes.

## Dependencies / preconditions

Auth/RBAC, job/employee repositories, matching package, and match-run persistence.

## Acceptance criteria

- **AC1:** ADMIN/SUPERVISOR can request recommendations; VIEWER cannot.
- **AC2:** Job must exist, be `OPEN`, and contain usable criteria; canonical errors cover invalid states.
- **AC3:** Orchestrator snapshots job/options/ACTIVE candidates and passes immutable DTOs to matching.
- **AC4:** Success returns ranked results plus `match_run_id` and `model_version` only after the run is persisted.
- **AC5:** No eligible candidate is a handled result, not a crash.
- **AC6:** Matching/database failure returns safe 503 behavior without a partial match run.

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
