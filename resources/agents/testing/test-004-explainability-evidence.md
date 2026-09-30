# TEST-004 - Verify explanation evidence completeness

## Objective

Complete `TEST-004` by implementing the selected story contract without loading unrelated work.

## Read

1. `resources/spec_bundle/user_stories/testing/TEST-004-explainability-evidence.md`
2. `resources/spec_bundle/quality/tdd_story_contract.md`
3. Then read only the source contracts named by that story that are necessary to complete the selected acceptance criteria.

## Implementation area

`tests/`, focused fixtures, and evidence files required by the selected quality story.

## Workflow

- Inspect the smallest current production/test surface needed for the story before editing.
- Follow RED -> GREEN -> REFACTOR from the story contract.
- Preserve unrelated public behavior and the feature-oriented target architecture.
- Run the focused tests/checks first, then the relevant regression suite.
- Update canonical contracts/docs first when an approved public interface, scoring rule, data contract, or module boundary changes.
- Report exact changed files and observed command/check results.

## Stop conditions

Stop instead of guessing when the story's own stop condition applies, an unmerged change owns the same paths, or source/test behavior conflicts with a canonical contract and no approved amendment exists.
