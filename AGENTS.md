# SkillMatch AI agent router

This repository uses lazy-loaded instructions. Only this root file is assumed to load automatically. Route the current request to the smallest relevant domain, then read only the selected router, leaf instruction, and specification files named by that leaf.

| User intent | Read first |
| --- | --- |
| Architecture or source-layout migration | `resources/agents/architecture/AGENTS.md` |
| Authentication / bearer JWT / RBAC | `resources/agents/backend/auth/AGENTS.md` |
| Skill taxonomy | `resources/agents/backend/skills/AGENTS.md` |
| Employee profiles | `resources/agents/backend/employees/AGENTS.md` |
| Job requirements | `resources/agents/backend/jobs/AGENTS.md` |
| Matching eligibility / scoring / ranking / explanations | `resources/agents/backend/matching/AGENTS.md` |
| Recommendation orchestration / match runs | `resources/agents/backend/recommendations/AGENTS.md` |
| Supervisor feedback / audit | `resources/agents/backend/feedback/AGENTS.md` |
| API errors / request IDs | `resources/agents/backend/errors/AGENTS.md` |
| Health endpoint | `resources/agents/backend/health/AGENTS.md` |
| Database / repositories / PostgreSQL / migrations | `resources/agents/database/AGENTS.md` |
| Validated mock CSV import | `resources/agents/import/AGENTS.md` |
| React frontend | `resources/agents/frontend/AGENTS.md` |
| Testing / performance / relevance / reproducibility | `resources/agents/testing/AGENTS.md` |
| Offline matching evaluation | `resources/agents/evaluation/AGENTS.md` |
| GitHub Actions / uv CI/CD | `resources/agents/cicd/AGENTS.md` |
| Documentation / evidence | `resources/agents/documentation/AGENTS.md` |
| Peer review / technical debt | `resources/agents/review/AGENTS.md` |
| Unit 5 Alpha workflow | `resources/agents/release/alpha/AGENTS.md` |
| Unit 8 final workflow | `resources/agents/release/final/AGENTS.md` |
| Unit 8 portfolio video / position paper | `resources/agents/portfolio/AGENTS.md` |
| TDD / contract-change workflow | `resources/agents/workflow/AGENTS.md` |
| Inspect/amend canonical specifications | `resources/spec_bundle/AGENTS.md` |
| Rebuild/update this lazy-load AGENTS package | `resources/spec_bundle/lazy_load/AGENTS.md` |
| Unfamiliar implementation task | `resources/agents/AGENTS.md` |

## Global rules

- Do not preload `resources/agents/` or `resources/spec_bundle/`.
- Read only the route needed for the current request; do not recursively load sibling directories.
- Course team roles are accountability/documentation roles only. They do **not** restrict who may implement any story.
- The current SkillMatch Project Design Specification is the behavioral source of truth. Focused files under `resources/spec_bundle/` are its lazy-loaded implementation form.
- The source-layout target is the feature-oriented modular-monolith refinement in `resources/spec_bundle/project/architecture_contract.md`.
- The current `app/` plus scaffolded `backend/` layout is transitional. Migrate incrementally; do not do a big-bang rewrite solely to satisfy the target tree.
- Repository-level `pyproject.toml`, `.python-version`, and `uv.lock` remain the current Python dependency source of truth.
- Use story contracts as executable TDD contracts: RED -> GREEN -> REFACTOR -> relevant full suite.
- SkillMatch is decision support only. Never auto-assign an employee; a supervisor retains final authority.
- The matching package must not own HTTP, ORM/database sessions, or automatic staffing decisions.
- If the Project Design Specification does not define an exact public field/behavior, inspect current tests/code first. If still undefined, stop or record an approved contract amendment instead of inventing it silently.
- Never claim tests, CI, deployment, review, screenshots, coverage, or metrics passed unless actually observed.
