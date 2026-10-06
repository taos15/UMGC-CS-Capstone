# Architecture and persistence follow-ups

The canonical backend is `backend/src/skillmatch/`; `app/` is removed. Profiles,
skill taxonomy, recommendation runs/results, and feedback use feature-local
repositories. Employee/job APIs expose canonical section 6 profiles; matching
uses private adapters that preserve structured evidence.

PostgreSQL is configured with psycopg and Alembic migrations. Demo data is loaded
explicitly from validated `data/mock` JSON. SQLite/direct table creation remains
an optional local/test shortcut, not PostgreSQL release evidence.

The current impacts, priorities, mitigations, and retirement criteria are in
[the Alpha register](alpha-register.md). Earlier staged integration notes are
historical; canonical scoring, eligibility, ranking, explanations, persistence,
and feedback are connected in the runtime recommendation workflow.
