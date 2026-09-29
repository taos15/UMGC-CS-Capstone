# TDD user-story contract

Stories are organized by domain, not by team member. Course roles never restrict implementation.

Every story contains: ID/title; Domain; Phase; Priority; user story in `As a ... I want ... so that ...` form; smallest source contracts; Scope; Non-scope; Dependencies/preconditions; objective Acceptance criteria; RED; GREEN; REFACTOR; Completion evidence; Definition of Done; Stop conditions when needed.

## RED

Add the smallest failing test/check for one unmet criterion and verify the failure reason when feasible. If behavior already exists, add characterization/contract coverage instead of manufacturing a fake failure. Pure moves may use import/contract tests that protect legacy behavior while proving the canonical path is not yet active.

## GREEN

Implement the minimum change that satisfies the criterion. Preserve unrelated API/data/matching/auth/persistence behavior. Do not bypass boundaries merely to make the test green.

## REFACTOR

Improve names/cohesion/duplication/test setup without changing observable behavior. Re-run focused checks and then the relevant full suite.

A story is Done only when every criterion is objectively verified, relevant tests pass, public docs/contracts are updated, deliberate shortcuts are recorded as technical debt, and exact observed commands/results are reported.
