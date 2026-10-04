# Target architecture contract

## Decision

Use a **feature-oriented modular monolith in a monorepo**. This refines the Project Design Specification's layered modular monolith: separation of concerns is preserved inside features while each capability stays cohesive.

The latest repository's active `app/` plus scaffold/compatibility `backend/` split is transitional. The long-term contract is one canonical backend package under `backend/src/skillmatch/` plus a separate React frontend.

## Why

A repository-wide layer tree (`routers/`, `services/`, `repositories/`, `schemas/`) scatters one capability across unrelated directories. For this three-person, eight-week prototype, feature cohesion is more valuable. Normal features keep their router/schema/service/repository pieces together. Shared DB/config concerns remain centralized.

The matching package is intentionally different because the Project Design Specification defines it as a distinct AI package with **no HTTP or database access**. It therefore has no FastAPI router, ORM model, or repository merely for symmetry. Recommendation orchestration owns HTTP/repository interaction and passes immutable DTOs into matching.

## Target tree

```text
backend/
  src/skillmatch/
    main.py
    core/{config.py,security.py,errors.py,logging.py}
    db/{base.py,session.py}
    features/
      auth/
      skills/
      employees/
      jobs/
      recommendations/
      feedback/
      matching/{schemas.py,encoder.py,eligibility.py,scoring.py,ranking.py,explanations.py}
    integrations/csv_import/
  migrations/versions/
tests/{unit,integration/api,integration/database,contract}/
frontend/src/{app,api,components/shared,features/{employees,jobs,recommendations}}/
data/{sample,expected}/
scripts/{seed_data.py,benchmark_matching.py,evaluate_matching.py}
docs/{architecture,api,testing,peer_review,technical_debt,evidence/{unit5,unit8}}/
resources/{agents,spec_bundle}/
```

For `auth`, `skills`, `employees`, `jobs`, `recommendations`, and `feedback`, create only files actually needed from `router.py`, `schemas.py`, `models.py`, `repository.py`, `service.py`. Do not create empty ceremony files.

## Responsibility rules

- `router.py`: HTTP/FastAPI only.
- `schemas.py`: request/response contracts and immutable DTOs.
- `models.py`: persistence models only.
- `repository.py`: persistence operations only.
- `service.py`: application/domain orchestration.
- `features/matching/*`: pure/near-pure matching; no HTTP/direct DB.
- `features/recommendations/service.py`: recommendation orchestrator; may call repositories + matching; persists match runs.
- `features/feedback/`: feedback validation/audit/offline-export eligibility; never changes live matching automatically.
- `db/`: shared engine/session/base only.
- `core/`: truly cross-cutting config/security/errors/logging only.
- `integrations/csv_import/`: validated MVP CSV adapter.

## Dependency management

Keep repository-level `pyproject.toml`, `uv.lock`, and `.python-version`. Do not reintroduce a separately maintained `requirements.txt`. Frontend dependencies belong in `frontend/package.json`.

## Avoid over-engineering

Do not add generic `domain/`, `use_cases/`, `ports/`, `controllers/`, `managers/`, `helpers/`, `utils/`, `common/`, or `shared/` layers merely to imitate a larger system. Add abstractions only for real project boundaries.
