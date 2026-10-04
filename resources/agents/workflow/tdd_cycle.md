# TDD cycle for one SkillMatch story

## Read

- The selected story only.
- `resources/spec_bundle/quality/tdd_story_contract.md`.
- Only source contracts named by that story.

## Execute

1. Confirm the story/acceptance criterion and inspect the smallest current code/test surface.
2. RED: add the smallest failing test/check and confirm why it fails when feasible.
3. GREEN: implement the minimum compliant change.
4. REFACTOR: improve cohesion/naming/duplication without behavior drift.
5. Run focused checks, then the relevant regression suite.
6. Update approved contracts/docs when observable behavior changes.
7. Report changed files plus exact observed command results.

Never auto-implement the next story unless the user asked for a multi-story workflow.
