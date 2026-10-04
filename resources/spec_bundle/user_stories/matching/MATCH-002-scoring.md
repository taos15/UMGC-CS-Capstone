# MATCH-002 - Implement canonical versioned 55/20/15/10 scoring

- **Domain:** matching
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want candidates scored from transparent structured evidence so that I can understand how skills, certifications, and experience contribute to each recommendation.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`
- `resources/spec_bundle/data/data_contract.md`

## Scope

Implement R/P/C/E components, category renormalization, and 0-100 final score.

## Non-scope

Resume NLP, black-box scores, protected characteristics, current-title scoring.

## Dependencies / preconditions

Canonical immutable matching DTOs and named model/config version.

## Acceptance criteria

- **AC1:** R uses importance-weighted `min(employee_proficiency/minimum_proficiency,1.0)` for REQUIRED skills.
- **AC2:** P uses the same calculation for PREFERRED skills.
- **AC3:** C is valid required certifications / required certifications and is omitted when no required certifications exist.
- **AC4:** E is 1.0 for zero minimum experience, else `min(employee_total_years/job_minimum_years,1.0)`.
- **AC5:** Final = `100 * weighted_average(0.55R,0.20P,0.15C,0.10E)` with absent categories removed and weights renormalized.
- **AC6:** Scoring is independently unit-testable without FastAPI/live DB.

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
