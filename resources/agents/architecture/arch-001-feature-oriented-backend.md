# ARCH-001 - Migrate to the canonical feature-oriented backend package

## Objective

Complete `ARCH-001` by implementing the selected story contract without loading unrelated work.

## Read

1. `resources/spec_bundle/user_stories/architecture/ARCH-001-feature-oriented-backend.md`
2. `resources/spec_bundle/quality/tdd_story_contract.md`
3. Then read only the source contracts named by that story that are necessary to complete the selected acceptance criteria.

## Implementation area

Repository structure; `backend/src/skillmatch/`; compatibility imports; test/package paths.

## Workflow

- Inspect the smallest current production/test surface needed for the story before editing.
- Follow RED -> GREEN -> REFACTOR from the story contract.
- Preserve unrelated public behavior and the feature-oriented target architecture.
- Run the focused tests/checks first, then the relevant regression suite.
- Update canonical contracts/docs first when an approved public interface, scoring rule, data contract, or module boundary changes.
- Report exact changed files and observed command/check results.

## Stop conditions

Stop instead of guessing when the story's own stop condition applies, an unmerged change owns the same paths, or source/test behavior conflicts with a canonical contract and no approved amendment exists.
