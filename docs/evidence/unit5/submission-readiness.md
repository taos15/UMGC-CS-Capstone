# Unit 5 submission readiness

This packet describes the readiness changes made after baseline `bf02618`.
Local checks were observed before publication. This is not evidence that a
submitted commit has passed hosted CI, nor that an independent peer reviewed it.
The contributor will verify hosted CI and branch protection after publication.

## Implemented workflow

- Skills: authorized list/create with exact skill IDs, duplicate handling, and
  paginated reads. Profiles validate references against the persisted taxonomy.
- Employees/jobs: canonical profile list/read/create/update/permanent delete;
  server UUIDs, unique business keys, and atomic version conflicts.
- React: live OPEN-job listing and canonical requirement display; profile forms
  include versions and retain drafts on stale conflicts.
- Matching: eligibility, R/P/C/E scoring, deterministic ranking, explanations,
  evidence-aware snapshot hashing, stored run retrieval, and append-only feedback.
- PostgreSQL: psycopg driver, versioned Alembic schema, validated demo loading,
  and a reproducible real-browser test runner.
- CI: backend lint/tests, frontend lint/tests/build, PostgreSQL browser tests,
  and a fail-closed `CI required` aggregate.

## Observed local integration evidence

The disposable local PostgreSQL server was 14.24. It used a temporary cluster
and Unix socket, without administrator installation or external network binding.
A fresh `skillmatch_e2e` database was migrated from empty to Alembic head.
`alembic check` reported no new upgrade operations.

Command (with a disposable PostgreSQL URL supplied through the environment):

```sh
uv run --locked python scripts/run_postgres_e2e.py
```

With Node 24 and Playwright Chromium installed, three real browser scenarios
passed without intercepted/mocked API responses:

1. React login -> OPEN job -> canonical requirements -> recommendations ->
   displayed rank/score/explanation -> SELECTED feedback -> unchanged stored run.
2. Employee form create -> stale-version conflict -> retained draft -> explicit
   reload -> update -> confirmed permanent deletion -> typed missing response.
3. Job form create -> the same conflict/recovery/update/deletion workflow.

The runner's independent Python process/database session verified committed run,
candidate rows, and SELECTED feedback referencing an eligible stored candidate.
It generated temporary credentials and stopped Uvicorn/Vite after the checks.
SQLite API tests additionally verify that deleting live profiles leaves historical
runs unchanged and that failed matches leave no partial run.

## Final local regression checks

Observed on the completed working tree:

- `uv run --locked pytest -q`: **382 passed**, six existing dependency/schema warnings.
- `uv run --locked ruff check backend/src backend/migrations tests scripts`: passed.
- Frontend clean locked install, ESLint, **91 Vitest tests**, and production build: passed.
- PostgreSQL browser integration: **3 passed**, with independent persistence verification.
- `alembic check`: no new upgrade operations; `actionlint`: workflow passed.
- The prepared AI-assisted refinement report contains exactly **250 words**.

Node 24 was supplied through npm's executable package wrapper in the local
environment. Standard README commands apply when Node 24 is installed normally.
The backend's six warnings and deprecated React-compatible ESLint 9 are recorded
in the debt register rather than suppressed.

## Submission gates

| Gate | Status / evidence needed |
| --- | --- |
| Integrated recommendation/profile workflow | Observed locally against PostgreSQL and Chromium, as above |
| Locked backend/frontend checks | Observed locally above; hosted evidence still must match the final commit |
| Hosted CI on submitted SHA | Pending. Attach the Actions run URL and exact successful SHA; no local result substitutes for this |
| Merge enforcement | Pending administrator verification that `CI required` from GitHub Actions is required for `dev` and `main`, including up-to-date branches and existing review rules |
| Independent review / solo alternative | Pending real review or written instructor approval; [prepared report](../../peer_review/solo-refinement-report.md) is exactly 250 words and explicitly AI-assisted |
| Technical debt | [Current register](../../technical_debt/alpha-register.md) records impacts, priorities, mitigations, and retirement criteria |
| Performance / relevance targets | Not measured by these functional checks; do not infer latency or relevance quality from a green test suite |

## Final evidence to attach

- Submitted commit SHA, repository/PR URL, and successful Actions run URL.
- Local test/lint/build output and PostgreSQL browser scenario output for the
  same code, with environment versions and remaining warnings stated.
- Actual instructor response or reviewer identity/findings; contributor-reviewed
  refinement report and links to resulting changes.
- Debt register and setup/usage README. Keep the earlier failed integration pass
  labeled historical rather than presenting its obsolete blockers as current.

Suggested commit message:
`feat: complete Alpha profile workflows and PostgreSQL integration checks`
