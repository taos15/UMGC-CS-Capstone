# Lazy-load package manifest

This manifest defines the expected **shape and catalog** for rebuilding the SkillMatch instruction overlay. It is intentionally more explicit than a router because it is used only by the package-generation workflow.

## Required specification domains

- `project/` — source provenance, scope, Project Design contract, target architecture, migration rules, repository map, traceability.
- `api/` — REST endpoint/role conventions and problem-details/error contract.
- `data/` — shared data vocabulary and mock CSV import contract.
- `matching/` — deterministic matching and offline evaluation contracts.
- `quality/` — acceptance targets and TDD story contract.
- `assignments/` — Unit 5 Alpha and Unit 8 final acceptance gates.
- `user_stories/` — domain routers plus individual TDD story contracts.
- `lazy_load/` — the package-generation rules, source instructions, manifest, and validation.

## Required user-story catalog

### Architecture

- ARCH-001 - Migrate to the canonical feature-oriented backend package

### Auth

- AUTH-001 - Exchange local credentials for a short-lived bearer token
- AUTH-002 - Enforce ADMIN, SUPERVISOR, and VIEWER authorization

### Cicd

- CI-001 - Keep GitHub Actions aligned with the uv project
- CI-002 - Complete final CI/CD and deployment evidence

### Database

- DB-001 - Establish canonical database/session infrastructure
- DB-002 - Use feature-local repository boundaries
- DB-003 - Use PostgreSQL with reproducible Alembic migrations

### Documentation

- DOC-001 - Document Alpha installation, usage, and evidence
- DOC-002 - Complete final technical documentation set

### Employees

- EMP-001 - List and filter employee profiles
- EMP-002 - Retrieve one employee profile
- EMP-003 - Create a structured employee profile
- EMP-004 - Update an employee profile with optimistic versioning

### Errors

- ERR-001 - Return stable RFC 9457-style problem details
- ERR-002 - Trace every API response with X-Request-ID

### Evaluation

- EVAL-001 - Evaluate matching offline without changing live behavior

### Feedback

- FDBK-001 - Record supervisor feedback against a stored match run

### Frontend

- UI-001 - Establish the React supervisor portal foundation
- UI-002 - Authenticate from the supervisor portal
- UI-003 - Select an OPEN job and request recommendations
- UI-004 - Display ranked recommendation evidence
- UI-005 - Record supervisor feedback from a stored match run
- UI-006 - Handle loading, empty, and typed error states

### Health

- OPS-001 - Expose service and dependency health

### Import

- IMP-001 - Import validated mock CSV data

### Jobs

- JOB-001 - List and filter job profiles
- JOB-002 - Retrieve one job profile
- JOB-003 - Create a match-ready structured job profile
- JOB-004 - Update a job with optimistic versioning

### Matching

- MATCH-001 - Evaluate candidate eligibility before ranking
- MATCH-002 - Implement canonical versioned 55/20/15/10 scoring
- MATCH-003 - Rank candidates deterministically
- MATCH-004 - Build evidence-based recommendation explanations

### Portfolio

- PORT-001 - Prepare the 10-15 minute technical stakeholder presentation
- PORT-002 - Draft the evidence-based 1,300-word professional position paper

### Recommendations

- REC-001 - Generate a recommendation run for an OPEN job
- REC-002 - Persist and retrieve immutable match runs

### Release

- REL-001 - Verify Unit 5 Alpha release readiness
- REL-002 - Verify Unit 8 final repository readiness

### Review

- DEBT-001 - Track and mitigate concrete technical debt
- REVIEW-001 - Conduct structured Unit 5 peer review and refinement

### Skills

- SKILL-001 - List and search the controlled skill taxonomy
- SKILL-002 - Create a controlled skill

### Testing

- TEST-001 - Organize unit, integration, and contract test suites
- TEST-002 - Benchmark recommendation P95 latency
- TEST-003 - Evaluate curated Top-3 relevance
- TEST-004 - Verify explanation evidence completeness
- TEST-005 - Verify deterministic matching reproducibility
- TEST-006 - Produce final testing and code-quality evidence

## Required agent routes

- `resources/agents/architecture/`
- `resources/agents/backend/{auth,skills,employees,jobs,matching,recommendations,feedback,errors,health}/`
- `resources/agents/database/`
- `resources/agents/import/`
- `resources/agents/frontend/`
- `resources/agents/testing/`
- `resources/agents/evaluation/`
- `resources/agents/cicd/`
- `resources/agents/documentation/`
- `resources/agents/review/`
- `resources/agents/release/{alpha,final}/`
- `resources/agents/portfolio/`
- `resources/agents/workflow/`

Each directory above has an `AGENTS.md` router. Every product/evidence story has a corresponding task leaf that points to exactly one story contract. Phase-wide workflows are explicit leaves and must not be auto-chained from narrow tasks.

## Required repository overlay documentation

- `docs/IMPLEMENTATION_PLAN.md`
- `docs/ARCHITECTURE_MIGRATION.md`

## Target empty directory skeleton

The ZIP may include empty target directories for the agreed architecture so extraction communicates direction without creating placeholder source modules. Do not create empty Python/TypeScript files just to make Git track the structure.

## Distribution

- Archive extracts directly into repository root.
- Top-level `AGENTS.md` is present.
- No outer wrapper directory.
- No source assignment DOCX/PDF, temp scripts, cache, `.venv`, or cloned `.git` data is packaged.
- The package must not delete/overwrite production source code. It may add/update `AGENTS.md`, `resources/`, focused planning docs, and empty target directories.
