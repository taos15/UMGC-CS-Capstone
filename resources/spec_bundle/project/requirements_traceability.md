# Project Design requirement traceability

This table maps the approved Project Design Specification and course gates to focused contracts and executable TDD stories. It is traceability, not an instruction to load every listed file for every task.

| Requirement / evidence need | Canonical contract | Primary stories |
| --- | --- | --- |
| React + one FastAPI app + PostgreSQL modular monolith | `architecture_contract.md`, `project_design_contract.md` | ARCH-001, DB-001, DB-003, UI-001 |
| Current uv project / locked CI environment | `architecture_contract.md`, `repository_map.md` | CI-001 |
| Bearer login + ADMIN/SUPERVISOR/VIEWER RBAC | `../api/api_contract.md`, `../api/error_contract.md` | AUTH-001, AUTH-002, UI-002 |
| Controlled skill taxonomy | `../api/api_contract.md` | SKILL-001, SKILL-002 |
| Employee profile list/get/create/update | `../api/api_contract.md`, `../data/data_contract.md` | EMP-001..004 |
| Job list/get/create/update + match-readiness rules | `../api/api_contract.md`, `../data/data_contract.md` | JOB-001..004 |
| Distinct DB/HTTP-free matching package | `../matching/matching_contract.md`, `architecture_contract.md` | MATCH-001..004 |
| Eligibility: ACTIVE + mandatory-cert rules | `../matching/matching_contract.md` | MATCH-001 |
| 55/20/15/10 normalized score formula | `../matching/matching_contract.md` | MATCH-002 |
| Deterministic tie-break/reproducibility | `../matching/matching_contract.md`, `../quality/quality_contract.md` | MATCH-003, TEST-005 |
| Structured evidence explanations | `../matching/matching_contract.md` | MATCH-004, TEST-004, UI-004 |
| Recommendation orchestration + immutable stored match runs | `../api/api_contract.md`, `project_design_contract.md` | REC-001, REC-002, UI-003 |
| Supervisor feedback/audit; no online training | `project_design_contract.md`, `../data/data_contract.md` | FDBK-001, UI-005 |
| RFC 9457-style problems + stable request IDs | `../api/error_contract.md` | ERR-001, ERR-002, UI-006 |
| Health/dependency endpoint | `../api/api_contract.md` | OPS-001 |
| Validated mock CSV adapter | `../data/csv_import_contract.md` | IMP-001 |
| Offline evaluation/model review | `../matching/evaluation_contract.md` | EVAL-001 |
| P95 <2s / 100 ACTIVE / >=30 runs | `../quality/quality_contract.md` | TEST-002 |
| Top-3 >=12/15 curated jobs | `../quality/quality_contract.md`, `../matching/evaluation_contract.md` | TEST-003 |
| 100% explanation evidence target | `../quality/quality_contract.md` | TEST-004 |
| Unit/integration/contract testing organization | `../quality/tdd_story_contract.md`, `architecture_contract.md` | TEST-001 |
| Final coverage/code-quality evidence | `../assignments/unit8_final_acceptance.md` | TEST-006 |
| React supervisor workflow | `project_design_contract.md`, `../api/api_contract.md` | UI-001..006 |
| Unit 5 CI / integrated Alpha | `../assignments/unit5_alpha_acceptance.md` | CI-001, DOC-001, REL-001 |
| Unit 5 peer review | `../assignments/unit5_alpha_acceptance.md` | REVIEW-001 |
| Unit 5 technical-debt analysis | `../assignments/unit5_alpha_acceptance.md` | DEBT-001 |
| Unit 8 final documentation / CI-CD / metrics | `../assignments/unit8_final_acceptance.md` | DOC-002, CI-002, TEST-003, TEST-006, REL-002 |
| Unit 8 stakeholder video | `../assignments/unit8_final_acceptance.md` | PORT-001 |
| Unit 8 individual position paper | `../assignments/unit8_final_acceptance.md` | PORT-002 |
| Lazy-loaded package can rebuild itself | `../lazy_load/package_contract.md`, `../lazy_load/package_manifest.md` | Package-generation workflow, not a product story |
