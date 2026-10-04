# IMP-001 - Import validated mock CSV data

- **Domain:** import
- **Phase:** Unit 5 Alpha
- **Priority:** Must
- **Status:** Ready

## User story

As an administrator or project tester, I want to import validated mock CSV data so that the MVP can load reproducible employee/job evidence without production enterprise integrations.

## Source contracts

- `resources/spec_bundle/quality/tdd_story_contract.md`
- `resources/spec_bundle/data/csv_import_contract.md`
- `resources/spec_bundle/data/data_contract.md`
- `resources/spec_bundle/project/project_design_contract.md`

## Scope

Implement only the validated MVP CSV adapter and route imported records through canonical validation/persistence.

## Non-scope

Live HRIS/LMS/payroll/ATS/certification-provider APIs.

## Dependencies / preconditions

Mock CSV schema must be found in current files/tests or explicitly approved before coding.

## Acceptance criteria

- **AC1:** Importer validates the project mock format before persistence.
- **AC2:** Imported records obey the same Employee/Job/Skill business rules as API-created records.
- **AC3:** Malformed rows are reported safely without uncontrolled partial/corrupt data.
- **AC4:** No live external-system credentials/integration are introduced.

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

Stop if exact CSV columns or atomicity behavior remain undefined after inspecting current project artifacts; define a focused import-schema amendment first.
