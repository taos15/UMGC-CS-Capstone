# REC-002 - Persist and retrieve immutable match runs

- **Domain:** recommendations
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor or reviewer, I want recommendation runs stored immutably so that I can inspect exactly what the system returned without silently rescoring later.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/api/api_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/api/error_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Persist full recommendation evidence and implement `GET /api/v1/match-runs/{match_run_id}`.

## Non-scope

Mutable reranking or silent recomputation of historical runs.

## Dependencies / preconditions

Recommendation orchestration and persistence models/repository.

## Acceptance criteria

- **AC1:** A successful recommendation persists the full immutable run before returning.
- **AC2:** GET returns the stored snapshot rather than recomputing.
- **AC3:** Unknown run returns `MATCH_RUN_NOT_FOUND`.
- **AC4:** Run stores job/requester/model version/snapshot hash/options/generated_at/rankings/evidence needed for audit/reproducibility.

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
