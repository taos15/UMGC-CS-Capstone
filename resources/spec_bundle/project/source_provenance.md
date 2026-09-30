# Source provenance and precedence

## Supplied project source

Primary supplied requirements source: **SkillMatch AI Project Design Specification**, Group 5, dated September 10, 2026.

The source defines the product scope, modular-monolith architecture, REST interface set, data vocabulary, matching formula, quality targets, failure behavior, and future/deferred boundaries. The focused files in `resources/spec_bundle/` are a lazy-loaded implementation form of that source, not a replacement for its intent.

## Current user-approved refinements

The following later user instructions intentionally refine how the repository is organized without changing the product behavior defined by the Project Design Specification:

1. Use a **feature-oriented modular monolith** under one canonical `backend/src/skillmatch/` package instead of preserving the temporary `app/` + scaffolded `backend/` split.
2. Keep the current repository-level uv project (`pyproject.toml`, `.python-version`, `uv.lock`) rather than moving Python dependency ownership under `backend/`.
3. Course roles are accountability/documentation context only. They do **not** restrict who may implement any story or source area.
4. Organize implementation stories/instructions by technical/product domain, not by James/Angel/Frank ownership.
5. Make the lazy-load workflow generator itself a first-class specification domain at `resources/spec_bundle/lazy_load/` so a future agent can rebuild/update the same class of package.

These refinements have precedence over older package organization choices, but they do not authorize silent changes to endpoints, matching math, data semantics, assignment boundaries, or other Project Design behavior.

## Repository-derived facts

`resources/spec_bundle/project/repository_map.md` records observed facts from the latest supplied `dev` archive. Repository observations are authoritative for **current paths and already-implemented behavior**, but they do not silently override approved Project Design contracts. When current code/tests conflict with a canonical contract, characterize the conflict and resolve it through an explicit story/approved amendment.

## Assignment sources

Unit 5 and Unit 8 acceptance files under `resources/spec_bundle/assignments/` capture course deliverable gates. They govern evidence/release work but do not expand the product MVP beyond the approved project scope unless the team explicitly amends the design.
