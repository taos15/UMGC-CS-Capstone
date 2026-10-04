# Complete Unit 5 Alpha workflow

Use this leaf **only** when the user explicitly asks to complete the whole phase.

## Read

- `resources/spec_bundle/assignments/unit5_alpha_acceptance.md`
- `resources/spec_bundle/project/project_design_contract.md`
- `resources/spec_bundle/project/architecture_contract.md`
- `resources/spec_bundle/quality/tdd_story_contract.md`

## Execution rule

Work story-by-story. For each ID below, locate it through `resources/spec_bundle/user_stories/AGENTS.md`, run its TDD cycle, and stop the phase on a blocking contract conflict rather than skipping silently. Do not load every story at once. Load the next story only after the current one is Done or explicitly recorded as blocked/deferred with user approval.

## Planned order

1. `ARCH-001`
2. `DB-001`
3. `ERR-001`
4. `ERR-002`
5. `OPS-001`
6. `AUTH-001`
7. `AUTH-002`
8. `SKILL-001`
9. `SKILL-002`
10. `EMP-001`
11. `EMP-002`
12. `EMP-003`
13. `EMP-004`
14. `JOB-001`
15. `JOB-002`
16. `JOB-003`
17. `JOB-004`
18. `IMP-001`
19. `MATCH-001`
20. `MATCH-002`
21. `MATCH-003`
22. `MATCH-004`
23. `REC-001`
24. `REC-002`
25. `FDBK-001`
26. `UI-001`
27. `UI-002`
28. `UI-003`
29. `UI-004`
30. `UI-005`
31. `UI-006`
32. `TEST-001`
33. `TEST-004`
34. `TEST-005`
35. `TEST-002`
36. `CI-001`
37. `DOC-001`
38. `REVIEW-001`
39. `DEBT-001`
40. `REL-001`

The order is dependency-oriented, not ownership-oriented. Reorder only when current repository/PR dependencies justify it and the change does not bypass prerequisites.
