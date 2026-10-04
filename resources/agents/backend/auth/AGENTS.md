# Auth task router

Backend RBAC is authoritative. Never move protected-data authorization into the React client.

| User intent / story | Read |
| --- | --- |
| AUTH-001 - Exchange local credentials for a short-lived bearer token (Unit 5 Alpha) | `auth-001-login.md` |
| AUTH-002 - Enforce ADMIN, SUPERVISOR, and VIEWER authorization (Unit 5 Alpha) | `auth-002-rbac.md` |

Read only the selected leaf. Return here only if the task changes to a different story in this domain.
