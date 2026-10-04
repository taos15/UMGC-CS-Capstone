# Lazy-load package validation contract

## Routing

- Root `AGENTS.md` is brief and broad.
- Every directory under `resources/agents/` has `AGENTS.md`.
- Every router/leaf target exists.
- Narrow requests reach narrow leaves without sibling loading.
- Complete workflows are explicit routes only.

## Specifications

- `resources/spec_bundle/AGENTS.md` exists.
- `resources/spec_bundle/lazy_load/AGENTS.md` exists and is reachable from root's spec route.
- Project Design decisions are represented in focused project/api/data/matching/quality contracts.
- No generic placeholder user stories.
- Every story listed in `package_manifest.md` exists and every generated story is represented by the manifest/story routers.
- Every product/evidence story has a reachable implementation leaf under `resources/agents/`.
- Stories are domain-based, not role-based.
- Endpoints/roles/errors/scoring match canonical project spec unless an amendment exists.
- Internal Markdown path references resolve.

## Story/TDD

Each story contains Domain, Phase, Priority, User story, Source contracts, Scope, Non-scope, Dependencies/preconditions, Acceptance criteria, RED, GREEN, REFACTOR, Completion evidence, Definition of Done, and Stop conditions.

## Distribution

ZIP opens successfully; top-level contains `AGENTS.md` and project overlay directories with no wrapper; no temp sources/caches/.venv/assignment documents are accidentally included; package does not delete production code.
