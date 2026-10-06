# Complete Unit 8 final workflow

Use this leaf **only** when the user explicitly asks to complete the whole phase.

## Read

- `resources/spec_bundle/assignments/unit8_final_acceptance.md`
- `resources/spec_bundle/project/project_design_contract.md`
- `resources/spec_bundle/project/architecture_contract.md`
- `resources/spec_bundle/quality/tdd_story_contract.md`

## Execution rule

Work story-by-story. For each ID below, locate it through `resources/spec_bundle/user_stories/AGENTS.md`, run its TDD cycle, and stop the phase on a blocking contract conflict rather than skipping silently. Do not load every story at once. Load the next story only after the current one is Done or explicitly recorded as blocked/deferred with user approval.

## Planned order

1. `DB-003`
2. `EVAL-001`
3. `TEST-003`
4. `TEST-006`
5. `CI-002`
6. `DOC-002`
7. `REL-002`
8. `PORT-001`
9. `PORT-002`

The order is dependency-oriented, not ownership-oriented. Reorder only when current repository/PR dependencies justify it and the change does not bypass prerequisites.
