# PHASE 3C-3 — ACCOUNTING API VERIFICATION & HARDENING

Accounting API implementation has been completed.

Inventory API has already passed its Verification & Hardening phase
and is the reference architecture.

This phase is ONLY for verification and hardening.

DO NOT implement Working API.
DO NOT implement React.
DO NOT add new Accounting features.

==================================================
1. AUTHENTICATION
==================================================

Verify:

- no JWT → 401
- invalid JWT → 401
- valid JWT → authenticated
- inactive/unapproved AppUser → rejected
- request.user is the correct custom AppUser

==================================================
2. ROLE AUTHORIZATION
==================================================

Verify every relevant role against every Accounting endpoint:

/api/v1/accounting/prices/
/api/v1/accounting/exports/
/api/v1/accounting/payments/
/api/v1/accounting/dashboard/
/api/v1/accounting/team-revenue/

Test:

- GET
- POST
- PUT
- PATCH
- DELETE

where applicable.

Do not invent permissions.

Compare implementation with the approved Phase 3C-1 design
and the existing legacy Django behavior.

Produce an explicit permission matrix.

==================================================
3. SENSITIVE / READ-ONLY FIELDS
==================================================

Inspect every serializer.

Identify fields that:

- must be read-only
- must be calculated by backend
- must be populated from request.user
- must not be spoofable by clients

Attempt to submit modified values for these fields.

Expected result:

Client cannot override authoritative backend values.

==================================================
4. BUSINESS LOGIC
==================================================

For:

- ProductPrice
- ExportReport
- PaymentReport
- dashboard
- team-revenue

trace all existing business logic.

Verify the API does not bypass:

- calculations
- validation
- status rules
- relationships
- approval rules
- accounting rules

If legacy logic exists in services.py, verify API and legacy views
share it where appropriate.

==================================================
5. FINANCIAL DATA INTEGRITY
==================================================

Pay special attention to:

- prices
- revenue
- payments
- export values
- totals
- calculated fields

Verify clients cannot directly manipulate values that should be
derived from authoritative database/business data.

Do not move calculations into React.

==================================================
6. IDOR / OBJECT-LEVEL SECURITY
==================================================

Determine whether Accounting records are:

- globally shared
- restricted by user
- restricted by team
- restricted by role

Verify that the API cannot expose or modify unauthorized objects.

Document the business justification if object-level restrictions
are intentionally not required.

==================================================
7. FILTERING
==================================================

Verify django-filter behavior.

Test:

- valid filters
- invalid filters
- empty filters
- multiple filters
- unauthorized filtering attempts

Ensure malformed filters return controlled API responses rather than
500 errors.

==================================================
8. PAGINATION
==================================================

Verify pagination for all list endpoints.

Check:

- count
- next
- previous
- results
- page size

==================================================
9. REPORTING ENDPOINTS
==================================================

Test:

GET /api/v1/accounting/dashboard/
GET /api/v1/accounting/team-revenue/

Verify:

- authentication
- authorization
- response structure
- calculations
- empty data behavior
- date/filter behavior if supported
- query efficiency

These endpoints must not expose information to unauthorized roles.

==================================================
10. QUERY PERFORMANCE
==================================================

Inspect:

- select_related
- prefetch_related
- aggregation queries
- N+1 problems
- unnecessary queries

Use query-count tests where appropriate.

Do not perform speculative optimization.

==================================================
11. CRUD COVERAGE
==================================================

Verify all supported operations:

ProductPrice:
- list
- retrieve
- create
- update
- partial update
- delete

ExportReport:
- list
- retrieve
- create
- update
- partial update
- delete

PaymentReport:
- list
- retrieve
- create
- update
- partial update
- delete

If an operation is intentionally unsupported, document why.

==================================================
12. API CONTRACT
==================================================

Verify against docs/api.md:

- URLs
- HTTP methods
- status codes
- JSON response structure
- validation errors
- authentication errors
- authorization errors
- not-found errors

Documentation must match actual implementation.

==================================================
13. REGRESSION TESTING
==================================================

Run at minimum:

1. Accounting API tests
2. Accounting legacy tests
3. Authentication tests
4. Inventory tests
5. Full project test suite if feasible

Report exact commands and exact results.

Example:

X tests passed
Y tests failed

Do not only report "tests passed".

==================================================
14. DATABASE SAFETY
==================================================

Confirm:

- no unintended model changes
- no unintended migration changes
- no unintended database schema changes

Report:

git diff
git status

where appropriate.

==================================================
15. FILE CHANGE AUDIT
==================================================

List every modified/created file.

For each file explain why it changed.

Pay special attention to:

- settings.py
- requirements.txt
- ProcessMonitoring/api/urls.py
- Accounting/*
- global DRF settings

==================================================
16. FINAL VERIFICATION REPORT
==================================================

Return:

1. Authentication verification
2. Complete role matrix
3. Sensitive/read-only field verification
4. Business logic verification
5. Financial data integrity
6. IDOR analysis
7. Filtering verification
8. Pagination verification
9. Reporting endpoint verification
10. Query performance
11. CRUD coverage
12. API contract verification
13. Regression test results
14. Database/migration status
15. Complete file-change audit
16. Remaining risks / technical debt

==================================================
STOP
==================================================

After producing the report:

STOP.

Do NOT implement Working API.
Do NOT implement React.

Wait for explicit approval.