# Backend task router

Route backend work to the smallest feature boundary.

| Intent | Read |
| --- | --- |
| Authentication / RBAC | `auth/AGENTS.md` |
| Skill taxonomy | `skills/AGENTS.md` |
| Employee profiles | `employees/AGENTS.md` |
| Job requirements | `jobs/AGENTS.md` |
| Matching logic | `matching/AGENTS.md` |
| Recommendation orchestration / match runs | `recommendations/AGENTS.md` |
| Feedback / audit | `feedback/AGENTS.md` |
| Problem details / request IDs | `errors/AGENTS.md` |
| Health / dependency status | `health/AGENTS.md` |

- Keep FastAPI HTTP concerns in routers, persistence in repositories, and orchestration in services.
- Matching is the exception to normal feature symmetry: it has no HTTP/repository/ORM ownership.
- Do not create empty ceremony files merely to satisfy a pattern.
