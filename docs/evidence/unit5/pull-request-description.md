Job listing and profile writes returned 501, and runtime profiles came from in-memory seeds, preventing the normal React workflow from reaching persistent workforce data. This change activates the approved canonical profile and skill contracts, persists profiles/taxonomy, and adds atomic version checks and permanent deletion while retaining historical runs and feedback.

PostgreSQL migrations and explicit validated demo loading now support real browser scenarios for recommendations/feedback and both profile CRUD forms. Snapshot hashing includes matching evidence/date/model version. CI adds lint, frontend tests/build, PostgreSQL browser checks, and the fail-closed `CI required` gate. Setup docs, the debt register, and a labeled 250-word AI-assisted solo report record current behavior and remaining external submission gates.

Validation observed locally:

- Backend: 382 passed; six existing warnings. Ruff passed.
- Frontend: 91 tests passed; ESLint and production build passed.
- Three real Chromium/PostgreSQL scenarios passed; a separate database session verified persisted results/feedback.
- Alembic reported no schema drift; actionlint and six aggregate-gate cases passed.

Hosted CI on the final commit and required checks on dev/main remain for contributor verification. The prepared solo report does not establish independent peer review; instructor approval or an actual reviewer remains necessary. SQLite and JSON profile evidence remain documented prototype shortcuts.
