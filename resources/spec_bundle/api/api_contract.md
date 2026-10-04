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

The Project Design Specification does not fully define the full Skill object schema, search/filter query parameters, or the exact health response shape. Preserve tested current behavior if it exists; otherwise record an approved contract amendment instead of silently inventing a public schema.

## Approved local-login amendment

Approved by the user in this implementation session:

- `POST /auth/login` accepts JSON `username` and `password` strings.
- Success is HTTP 200 with `access_token`, `token_type: "bearer"`, and
  `expires_in: 900` (seconds). The response is not cacheable.
- JWTs use HS256 and contain `sub` (user UUID), `role` (ADMIN/SUPERVISOR/VIEWER),
  `iat` and `exp` (Unix seconds), with a 15-minute lifetime.
- Local accounts are configured as password hashes, with no built-in accounts.
  `SKILLMATCH_LOCAL_USERS` is a JSON object keyed by exact username, with
  `user_id`, `role`, and `password_hash` per entry. `SKILLMATCH_JWT_SECRET` is
  an externally supplied signing secret of at least 32 UTF-8 bytes.
- Hash format is `scrypt$<base64 salt>$<base64 digest>` with a random 16-byte
  salt, N=16384, r=8, p=1, and a 64-byte digest.
- Username length is 1–128; password length is 1–1024. Password values are
  excluded from validation errors and logging.
- Unknown usernames and wrong passwords return the same 401 problem:
  `AUTH_INVALID_CREDENTIALS`, detail `Invalid username or password.`, and
  `WWW-Authenticate: Bearer`. Missing/malformed/expired bearer credentials
  on workforce routes return generic 401 `AUTH_REQUIRED`.
- Configuration failures return generic 503 `AUTH_UNAVAILABLE`; no fallback
  signing secret or default account is used.
- Login and health remain public. Workforce routes validate bearer tokens;
  role authorization remains the separate AUTH-002 implementation.
