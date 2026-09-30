# Lazy-loaded agent workflow generator

Use these instructions when the user asks for a **lazy-load agent workflow**, a reusable `AGENTS.md` hierarchy, or task-routed agent instructions for any project.

## Objective

Create an agent-instruction structure where:

- Only the project-root `AGENTS.md` is expected to load automatically.
- The root file routes the current request to the smallest relevant instruction area.
- Nested `AGENTS.md` files are routers, not complete operating manuals.
- Leaf Markdown files contain the instructions for one specific task.
- Canonical project context, requirements, schemas, policies, and contracts live outside the routers and are loaded only when the selected task needs them.
- The user’s current request determines which route is read. Do not automatically load or execute every stage of a larger workflow.

## Determine the source of project context

Before designing the hierarchy, determine which of these cases applies.

### 1. The user supplied project context

Examples include requirements, specifications, workflows, examples, policies, schemas, architecture notes, or existing agent instructions.

- Treat the supplied material as the primary source of truth.
- Preserve its terminology and intent.
- Extract reusable project context into focused files under `resources/spec_bundle/` or another clearly named canonical-context directory requested by the user.
- Do not replace supplied rules with assumptions derived from the source code.
- Inspect source code only when needed to confirm paths, interfaces, formats, or implementation details.

### 2. The user did not supply project context, but a project exists in the current directory

- Analyze the existing project before creating the instruction hierarchy.
- Start with low-cost discovery: directory tree, root documentation, manifests, configuration files, entry points, tests, and existing `AGENTS.md` files.
- Use targeted searches to locate the files that define each recurring task or contract.
- Do not load the entire repository into context.
- Derive focused context documents from the repository and clearly distinguish observed facts from inferred conventions.
- Prefer current tests, schemas, configuration, and production behavior over stale prose documentation when they conflict. Record important conflicts instead of silently resolving them.

### 3. Neither context nor an existing project is available

Ask only for the minimum information needed to identify:

- the project’s purpose;
- the repeated tasks agents will perform;
- the expected artifacts or code changes;
- the authoritative source of requirements.

Do not invent a detailed workflow without this information.

## Required architecture

Use this pattern unless the user requests another location:

```text
AGENTS.md
resources/
  agents/
    <task-area>/
      AGENTS.md
      <subtask>/
        AGENTS.md
        <specific-task>.md
  spec_bundle/
    <focused-project-context>.md
```

Add deeper directories only when they improve routing precision. A task area with several distinct scenarios should normally become a directory with its own router.

Examples:

```text
resources/agents/testing/AGENTS.md
resources/agents/testing/unit/AGENTS.md
resources/agents/testing/unit/add_test.md
resources/agents/testing/integration/AGENTS.md
resources/agents/testing/integration/run_suite.md
```

```text
resources/agents/data_import/AGENTS.md
resources/agents/data_import/single_source/AGENTS.md
resources/agents/data_import/single_source/import.md
resources/agents/data_import/multiple_sources/AGENTS.md
resources/agents/data_import/multiple_sources/merge_with_base.md
resources/agents/data_import/multiple_sources/merge_without_base.md
```

## Root `AGENTS.md` rules

The root `AGENTS.md` is the only instruction file assumed to be always present in context. Keep it short.

It should contain:

- one brief statement describing the lazy-load system;
- a routing table mapping broad user intents to the next router file;
- a rule to read only the route needed for the current request;
- a rule not to continue into downstream tasks unless the user requested them;
- a rule to ask a clarifying question only when the selected task cannot be determined safely.

It should not contain:

- task-specific decisions;
- detailed implementation steps;
- complete project specifications;
- a copy of every route;
- instructions to read all files;
- automatic workflow chaining such as “after this, continue to the next stage.”

Do not create a separate file index merely to list the hierarchy. The routers are the index.

## Router `AGENTS.md` rules

Every nested `AGENTS.md` is a router for its directory.

A router should contain only:

- the purpose of that task area;
- a compact intent-to-file routing table;
- the smallest required-context references for each route;
- local rules that apply to every task below that router.

A router should tell the agent **where to read for the selected task**, not tell it to read every related file.

Good routing language:

```markdown
| User intent | Read |
| --- | --- |
| Compare existing database files | `compare/AGENTS.md` |
| Generate a database from normalized records | `generate/AGENTS.md` |
| Validate a generated database | `validate/AGENTS.md` |
```

Bad routing language:

```markdown
Read `compare.md`, `generate.md`, `validate.md`, and all files in `resources/spec_bundle/` before starting.
```

Create another router directory when one route still covers several materially different tasks or decision paths.

## Leaf instruction rules

A leaf Markdown file should address one specific task and be usable without loading unrelated instructions.

Include only what that task needs:

- task objective;
- required inputs;
- authoritative context files to read;
- task-specific decisions and clarifying questions;
- constraints and invariants;
- expected output location and format;
- focused validation requirements;
- conditions that require stopping instead of guessing.

Do not include broad project history or instructions for unrelated downstream work.

A leaf file may route to another area only when the user explicitly requested a multi-stage workflow. Otherwise, finish the requested task and stop.

## Canonical context and contracts

Store reusable project knowledge outside `resources/agents/` so routers remain small.

Use focused files such as:

```text
resources/spec_bundle/domain_terms.md
resources/spec_bundle/file_schema.md
resources/spec_bundle/naming_rules.md
resources/spec_bundle/merge_policy.md
resources/spec_bundle/repository_map.md
resources/spec_bundle/validation_contract.md
resources/spec_bundle/artifact_layout.md
```

Rules:

- One subject per file.
- Link to the smallest relevant context file from the leaf task that needs it.
- Do not require every task to load the entire bundle.
- Avoid duplicating the same rule across routers and leaf files.
- When context was derived from source code rather than supplied by the user, identify the files or behavior that support it and mark uncertain conclusions as inferred.
- Keep volatile implementation locations in a repository map rather than repeating paths throughout many task files.

## Task decomposition principles

Organize instructions by **user intent and decision path**, not merely by code directory.

Break a task into a nested route when any of the following differ:

- required inputs;
- source format;
- decision rules;
- output format;
- validation method;
- whether existing content is preserved or regenerated;
- whether the task changes production code, tests, documentation, data, or artifacts.

Do not over-fragment trivial tasks. A directory and router should exist only when it prevents unrelated context from being loaded or makes routing materially clearer.

## Repository analysis rules

When generating the workflow from an existing project:

1. Inspect the root tree and existing agent instructions.
2. Identify recurring user tasks from documentation, scripts, tests, CI, and code organization.
3. Locate authoritative schemas, interfaces, and validation logic with targeted searches.
4. Build a concise repository map containing only paths agents repeatedly need.
5. Create canonical context files for stable rules.
6. Create routers by intent.
7. Create leaf instructions for repeated, specific tasks.
8. Verify each route can be followed without reading unrelated files.

Use file hashes or byte comparisons when the task is only to determine whether files are identical. Do not place whole large files into context merely to compare equality.

## Workflow-generation behavior

When the user asks to create the lazy-loaded workflow:

- Generate the actual directory structure and files, not just an example.
- Preserve any existing compatible instructions unless the user asked for replacement.
- Avoid creating empty placeholder task areas without a known use.
- Include an empty output/artifact directory only when the project workflow requires one.
- Validate Markdown links and referenced paths.
- Check that every non-root router is reachable from the root through a clear intent route.
- Check that no router instructs the agent to read all sibling files.
- Check that task-specific decisions appear in leaf instructions or the narrowest applicable router, not at the root.

When the environment supports file creation, also provide a ZIP archive that extracts directly into the intended project root. The archive should expose `AGENTS.md` at its top level rather than adding an unnecessary wrapper directory, unless the user requests a wrapper.

## Quality checks

Before delivery, verify:

- The root `AGENTS.md` is brief and contains only broad routing.
- There is no redundant `FILE_INDEX.md` unless the user explicitly requested one.
- Nested `AGENTS.md` files are routers.
- Leaf files are task-specific.
- A narrow request reaches a narrow leaf without loading unrelated instructions.
- Complete workflows are available only through an explicit complete-workflow route.
- Canonical context is separated from agent-routing instructions.
- Supplied context and repository-derived context are not silently mixed.
- All paths, filenames, and links are valid.
- The delivered ZIP has the correct extraction structure.

## Response expectations

State the generated root path and summarize the major routes. Provide the complete ZIP and the root `AGENTS.md` individually. Provide additional individual files only when the user requests them or when reviewing a specific route.
