# TEST-002 - Benchmark recommendation P95 latency

- **Domain:** testing
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As the project team, I want a repeatable recommendation benchmark so that we can verify the prototype responds within the stated performance target.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/quality/quality_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Create a repeatable benchmark for up to 100 `ACTIVE` profiles, execute at least 30 measured runs in the declared team test environment, and record observed P95 latency.

## Non-scope

Production-scale load claims, 10,000-user concurrency claims, or invented benchmark numbers.

## Dependencies / preconditions

The representative data set and recommendation workflow are stable enough to benchmark.

## Acceptance criteria

- **AC1:** Benchmark data contains no more than the documented prototype scale and identifies active-candidate count.
- **AC2:** At least 30 recommendation runs are measured under a documented environment/configuration.
- **AC3:** P95 is calculated from observed timings and compared to the <2 second target.
- **AC4:** Raw/summary evidence is stored under `docs/evidence/unit5/` or an approved evidence path.
- **AC5:** A miss is reported as a miss with follow-up work; the target is not silently changed.

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
