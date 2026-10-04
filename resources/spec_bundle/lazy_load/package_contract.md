# SkillMatch lazy-load package contract

This adapts the user's generic lazy-load instructions to SkillMatch AI.

- Only root `AGENTS.md` is assumed to auto-load.
- Root is a short broad-intent router.
- Every directory under `resources/agents/` has an `AGENTS.md` router.
- Agent leaf files contain one specific implementation workflow.
- Canonical project knowledge lives under `resources/spec_bundle/` and loads only when selected.
- `resources/spec_bundle/AGENTS.md` is the spec router.
- `resources/spec_bundle/lazy_load/` is a first-class spec domain so the repo can regenerate this same package later.
- User stories are organized by domain, never by team member.

Required routes: architecture, auth, skills, employees, jobs, matching, recommendations/match runs, feedback/audit, errors/request IDs, health, database, CSV import, frontend, testing, offline evaluation, CI/CD, docs, peer review/technical debt, Unit 5, Unit 8, TDD.

Source precedence: explicit current user instruction -> approved Project Design Specification/amendments -> assignment/rubric gates -> current repository/tests for paths or already-established underspecified details -> existing package where compatible.

A complete archive extracts directly into project root with top-level `AGENTS.md`; no wrapper folder.
