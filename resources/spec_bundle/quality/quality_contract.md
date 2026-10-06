# Quality and acceptance contract

These are prototype **targets**, not pre-existing results.

- **Performance:** P95 recommendation latency < 2 seconds for up to 100 `ACTIVE` profiles; measure at least 30 runs.
- **Top-3 relevance:** at least 12 of 15 curated jobs contain a manually designated acceptable employee in the top three (>=80%).
- **Explainability:** 100% of returned results include component scores + matched/missing evidence with no unsupported skill claims.
- **Reproducibility:** same input snapshot + `model_version` -> identical order/scores.
- **Human control:** no endpoint auto-assigns an employee.
- **Security:** TLS outside local development, bearer auth, role enforcement, least-privilege DB access; unauthorized -> 401/403 without protected data.
- **Reliability:** malformed/conflicting/incomplete/unavailable inputs produce typed errors, not crashes/partial match runs.

Testing discipline: RED -> GREEN -> REFACTOR; never weaken tests merely to make code pass; unit tests cover pure business/matching logic, integration tests cover API/DB boundaries, contract tests protect approved external behavior. Never claim metrics/CI/deployment/review evidence until observed.
