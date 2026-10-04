# Architecture migration contract

The target structure is mandatory direction, but migration is incremental.

## Invariants

1. Never break a working public endpoint solely to move files.
2. Add `backend/src/skillmatch/` and canonical imports before deleting compatibility modules.
3. Move one feature at a time and keep focused tests green.
4. Delete legacy `app/` only after every active responsibility has a canonical replacement and relevant suites pass.
5. `backend/main.py` may temporarily re-export the canonical app, but eventually there is one real FastAPI app object.
6. Do not populate old placeholder `backend/api`, `backend/domain`, `backend/repositories`, or `backend/matching` merely because they exist.
7. Preserve root uv files and CI semantics during migration.
8. API/scoring/validation/persistence/auth behavior changes are dedicated stories, not incidental file-move changes.
9. Matching must emerge without HTTP/database ownership; recommendation orchestration owns repository interaction.
10. If current tested behavior conflicts with the Project Design Specification, characterize/report the conflict and change behavior only through an explicit story.

## Recommended sequence

Canonical package/entrypoint -> matching behavior-preserving move -> Employees/Jobs/Skills -> Recommendations/match runs -> Feedback/Audit -> Auth/errors/request IDs -> test reorganization -> remove old scaffold -> React -> PostgreSQL/Alembic completion -> CSV import/offline evaluation.
