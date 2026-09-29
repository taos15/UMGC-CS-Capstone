# UI-004 - Display ranked recommendation evidence

- **Domain:** frontend
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As a supervisor, I want each recommendation to show its rank, score, eligibility, component scores, and matched/missing evidence so that I can understand why candidates were ranked.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/matching/matching_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Render the canonical `CandidateResult` evidence returned by the server, including structured explanation and ineligible reasons when returned.

## Non-scope

Generating explanations in the browser, hiding gaps to make recommendations look stronger, or converting scores into automatic staffing decisions.

## Dependencies / preconditions

`REC-001` response and matching evidence contracts are implemented.

## Acceptance criteria

- **AC1:** Results preserve server ordering and display rank and 0-100 score.
- **AC2:** Every displayed candidate exposes component scores and matched/missing skill/certification evidence returned by the API.
- **AC3:** Ineligibility reasons are visible when applicable.
- **AC4:** The UI does not claim unsupported skills or derive new match facts not returned by the API.
- **AC5:** The page clearly states that recommendations are decision support and the supervisor retains final authority.

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
