# Build or update the complete SkillMatch lazy-load AGENTS package

## Objective

Generate the same class of repository-root overlay used here: root router, technical-domain routers/leaves, focused spec domains, domain-based TDD user stories, implementation/release docs, and a root-extractable ZIP.

## Read only for a complete rebuild

- `source_instructions.md`
- `package_contract.md`
- `package_manifest.md`
- `story_generation_contract.md`
- `validation_contract.md`
- `../project/project_design_contract.md`
- `../project/architecture_contract.md`
- `../project/repository_map.md`
- `../api/api_contract.md`
- `../api/error_contract.md`
- `../data/data_contract.md`
- `../data/csv_import_contract.md`
- `../matching/matching_contract.md`
- `../matching/evaluation_contract.md`
- `../quality/quality_contract.md`
- `../quality/tdd_story_contract.md`
- `../assignments/unit5_alpha_acceptance.md`
- `../assignments/unit8_final_acceptance.md`

A complete-package request is intentionally allowed to load several domains because the output is the whole instruction system.

Before regenerating against a newer branch, inspect only low-cost/high-authority repository facts: root tree, existing AGENTS, README, pyproject/uv files, CI, active entrypoints, tests, migrations/database setup. Update `repository_map.md` from observed facts. Do not load the entire repo.

Generate actual files, not an example. Treat `package_manifest.md` as the expected catalog: every listed story/domain/route must either be regenerated or deliberately amended because the approved Project Design changed. Preserve Project Design terminology/decisions. Route by domain, not team role. Keep routers concise. Put task-specific work in leaves and reusable contracts in spec files. Refresh real story contracts; never leave placeholders. Preserve the feature-oriented target and pure matching boundary unless an approved architecture amendment exists. Do not change production app code when the user only asked for the AGENTS overlay.

Run `validation_contract.md`, verify ZIP integrity, and provide at minimum the ZIP plus root `AGENTS.md`.
