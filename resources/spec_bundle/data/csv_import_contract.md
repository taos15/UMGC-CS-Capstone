# Validated mock CSV import contract

Mock CSV import is in MVP scope; production HRIS/LMS/payroll/ATS/certification-provider integrations are not.

Implement the adapter under `backend/src/skillmatch/integrations/csv_import/` or an explicitly approved equivalent. It may translate validated rows into canonical Employee/Job/Skill services/repositories, but must not bypass business validation or write uncontrolled raw data directly into tables.

Required behavior:

- Validate required columns, types, enums/ranges, duplicate business keys, and cross-field relationships.
- Route imported data through the same domain validation/persistence rules as API-created records.
- Report malformed rows safely; do not leave uncontrolled partial/corrupt data.
- Do not introduce live enterprise credentials/integrations.

The Project Design Specification does not define exact CSV columns. Inspect current mock files/tests first; if still undefined, create an approved focused import-schema amendment before coding.
