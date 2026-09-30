# REST API contract

Canonical base path: `/api/v1`.

## Authorization roles

- `ADMIN`: create/update skills, employees, jobs; request recommendations; submit feedback; read within scope.
- `SUPERVISOR`: read skills/employees/jobs; request recommendations; read authorized match runs; submit feedback.
- `VIEWER`: read skills/employees/jobs and authorized prior match runs only.
- `POST /auth/login` is public.
- `GET /health` is an operations endpoint; the Project Design Specification does not define its exact exposure/auth policy.

## Endpoint set

| Method | Path | Allowed role(s) | Purpose |
| --- | --- | --- | --- |
| POST | `/auth/login` | Public | Exchange local credentials for a short-lived bearer token. |
| GET | `/skills` | ADMIN / SUPERVISOR / VIEWER | List/search controlled skill taxonomy. |
| POST | `/skills` | ADMIN | Create a skill. |
| GET | `/employees` | ADMIN / SUPERVISOR / VIEWER | List/filter employee profiles. |
| POST | `/employees` | ADMIN | Create an employee profile. |
| GET | `/employees/{employee_id}` | ADMIN / SUPERVISOR / VIEWER | Retrieve one employee. |
| PUT | `/employees/{employee_id}` | ADMIN | Replace editable fields using optimistic versioning. |
| GET | `/jobs` | ADMIN / SUPERVISOR / VIEWER | List/filter jobs. |
| POST | `/jobs` | ADMIN | Create a job profile. |
| GET | `/jobs/{job_id}` | ADMIN / SUPERVISOR / VIEWER | Retrieve one job. |
| PUT | `/jobs/{job_id}` | ADMIN | Update using optimistic versioning. |
| POST | `/jobs/{job_id}/recommendations` | ADMIN / SUPERVISOR | Generate, store, return ranked recommendation run. |
| GET | `/match-runs/{match_run_id}` | Authorized roles within scope | Return immutable stored recommendation snapshot; never silently recompute. |
| POST | `/match-runs/{match_run_id}/feedback` | ADMIN / SUPERVISOR | Record supervisor feedback tied to the run. |
| GET | `/health` | Operations | Return service/dependency health. |

## Shared conventions

- JSON uses `snake_case`.
- Server identifiers are UUID strings. `employee_number` and `job_code` are unique business keys.
- Timestamps are UTC ISO 8601 with `Z`; date-only values use `YYYY-MM-DD`.
- Pagination: `page >= 1`, `page_size` 1-100, default 25.
- `PUT` includes `version`; stale update -> `409 STALE_VERSION`.
- Errors use `application/problem+json`, RFC 9457-style fields with stable `code`, `request_id`, `detail`, and field errors.
- Every response carries `X-Request-ID`.
- Recommendation responses also expose `match_run_id` and `model_version`.

## Underspecified details

The Project Design Specification does not fully define login credential field names/token response schema, the full Skill object schema, search/filter query parameters, or the exact health response shape. Preserve tested current behavior if it exists; otherwise record an approved contract amendment instead of silently inventing a public schema.
