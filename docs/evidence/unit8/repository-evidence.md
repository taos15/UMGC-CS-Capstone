# Unit 8 repository evidence

Prepared for James Lambert. These are observed local results, not a declaration
that the final submission, hosted CI, deployment, or independent review is complete.

## Build identity and method

The measurements used backend source at commit
`24578791460c82b6876c59f1c5aabb11a827fc62`, with uncommitted coverage tooling,
benchmark, CI, and documentation changes. The benchmark records the backend
source SHA-256 and its actual UTC measurement timestamp in the raw report.
Recheck the final submitted commit in GitHub Actions after committing these changes.

| Check | Observed result | Evidence |
| --- | --- | --- |
| Backend unit/API suite | 382 passed; 6 warnings | [Coverage JSON](backend-coverage.json) |
| Backend statement coverage | 97.21% (1,149/1,182) | Same JSON, totals |
| Backend branch coverage | 89.23% (116/130) | Same JSON, totals |
| Backend combined coverage | 96.42% | Same JSON; do not label this line coverage |
| Frontend suite | 91 passed across 7 files | [Coverage summary](frontend-coverage-summary.json) |
| Frontend coverage | Statements 85.29%; branches 81.81%; functions 77.93%; lines 94.89% | Same summary; includes all 18 application JS/JSX files |
| Recommendation latency | P95 39.02 ms; nearest-rank median 18.61 ms | [Raw benchmark](recommendation-benchmark.json) |
| PostgreSQL browser integration | 3 passed; independent session verified stored run, candidates, and SELECTED feedback | `scripts/run_postgres_e2e.py` rerun |
| Migration drift | No new upgrade operations detected | `alembic check` against the browser PostgreSQL database |
| Local lint/build | Ruff, ESLint, Vite build, and Actionlint passed | Actual local command results; hosted workflow still unverified |
| Benchmark persistence | All 30 measured runs persisted 100 candidates each | Raw report includes run IDs and independently checked counts |

Coverage measures the local unit/API and jsdom test suites. Most backend API
coverage uses isolated SQLite, and frontend tests mock HTTP. Actual PostgreSQL
browser integration is a separate check; it is not included in these coverage
percentages. Lower coverage remains in profile evidence editing and some error
branches. High coverage alone does not establish correctness or user relevance.

## Benchmark scope

The benchmark used Python 3.12.14, PostgreSQL 14.24, WSL2/Linux, one Uvicorn
worker, and one sequential loopback HTTP client. It cloned the nine ACTIVE mock
profiles cyclically into 100 ACTIVE profiles and used one Commercial Electrician
job. Five warm-up requests were excluded; all 30 measured requests returned and
persisted 100 candidates, including ineligible candidates.

Timing includes bearer validation, PostgreSQL reads, matching and explanations,
committing the stored run/results, HTTP response, and client decoding. Login,
migrations, and fixture preparation are excluded. The observed P95 meets the
specified local target of under two seconds. This is synthetic, warm-cache,
single-job evidence, not production capacity, concurrent-user scalability,
network latency, or independently evaluated staffing relevance.

The AI component is a deterministic rule-based recommendation engine with
R/P/C/E scoring, eligibility checks, explanations, and stable ordering. It does
not train a model or automatically assign employees.

## Reproducing the measurements

From the repository root:

```bash
uv sync --locked
uv run --locked pytest -q --cov=skillmatch --cov-branch --cov-report=term-missing --cov-report=json:coverage-backend.json --cov-report=html:htmlcov
npm --prefix frontend ci
npm --prefix frontend run test:coverage
```

Use Node 24 for frontend commands. The benchmark requires a dedicated, empty
PostgreSQL database with a name ending in `_benchmark`; it refuses populated
profile/taxonomy tables. Set `SKILLMATCH_BENCHMARK_DATABASE_URL` to its
`postgresql+psycopg://` connection URL, then run:

```bash
uv run --locked python scripts/benchmark_matching.py
```

Use a new empty database for another benchmark. Do not point it at production.
See the script's argument help for output selection. Raw coverage reports and
benchmark data are included beside this document; HTML coverage is generated
locally and uploaded as an artifact by the updated CI workflow.

## Hosted CI evidence supplied by the contributor

Run: [GitHub Actions 37408365442](https://github.com/taos15/UMGC-CS-Capstone/actions/runs/37408365442).
The repository/run is inaccessible to this environment. James supplied the
frontend summary: **7 files passed, 91 tests passed**. The excerpt does not
establish the overall conclusion, commit SHA, backend result, PostgreSQL browser
result, or aggregate `CI required` result. Those remain unverified here.

The supplied annotations contain three Node 20 action-runtime warnings and four
Ubuntu runner-image migration notices. The updated workflow pins Ubuntu 24.04
and uses observed Node 24 action releases: checkout 7.0.1, setup-node 7.0.0,
setup-uv 10.2.0, and upload-artifact 7.0.1. It also collects backend/frontend
coverage artifacts. A new hosted run is required to validate this updated workflow;
local lint and tests cannot establish hosted execution or branch protection.

## Remaining submission evidence

- Successful CI for the actual final commit: overall conclusion, commit SHA,
  each required job's result, and screenshots or saved job summaries.
- Actual deployment target, repeatable deployment steps, and observed deployment
  evidence. No hosting choice or deployed environment has been confirmed.
- Independent review, or instructor approval of the solo alternative. Neither
  has been established; an AI-assisted report is not independent peer review.
- Curated relevance evaluation before claiming the stated Top-3 relevance target.
- Final video and 1,300-word position paper with verified
  references and section counts.

The [user manual](../../user/manual.md) documents the observed portal flows.
