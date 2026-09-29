# Error and failure contract

| HTTP | Code | Required handling |
| ---: | --- | --- |
| 400 | `MALFORMED_JSON` | Correct syntax; do not retry unchanged. |
| 401 | `AUTH_REQUIRED` / `AUTH_INVALID_CREDENTIALS` | Authenticate again; login failure remains generic. |
| 403 | `FORBIDDEN` | Caller lacks role/scope; do not expose protected resource data. |
| 404 | `EMPLOYEE_NOT_FOUND` / `JOB_NOT_FOUND` / `MATCH_RUN_NOT_FOUND` | Verify identifier and caller scope. |
| 409 | `*_EXISTS` / `STALE_VERSION` / `JOB_NOT_OPEN` / `FEEDBACK_CONFLICT` | Resolve state/unique-key conflict before retry. |
| 422 | `VALIDATION_ERROR` / `JOB_HAS_NO_CRITERIA` | Correct field/cross-field rules. |
| 429 | `RATE_LIMITED` | Honor `Retry-After`. |
| 500 | `INTERNAL_ERROR` | Log `request_id`; never expose stack/database details. |
| 503 | `DATABASE_UNAVAILABLE` / `MATCH_ENGINE_UNAVAILABLE` | Fail safely; do not persist a partial match run. |

Use `application/problem+json` with RFC 9457-style structure. Body includes stable `code`, `request_id`, `detail`, and field errors where applicable. Every response includes `X-Request-ID`; error-body `request_id` matches it.

If matching is unavailable, recommendation may fail safely while the rest of the workforce data system remains usable. Never write a partial match run after matching/database failure.
