# PHASE 3B-3C — INVENTORY API VERIFICATION & HARDENING

Inventory API implementation is complete.

Do NOT implement Accounting, Working, Dashboard, or React.

The purpose of this phase is to verify and harden the existing
Inventory API before it becomes the reference architecture for future
module APIs.

==================================================
DO NOT CHANGE FUNCTIONAL SCOPE
==================================================

Do NOT:

- create new Inventory endpoints
- redesign the API
- change existing business rules
- modify models
- modify migrations
- modify database schema
- create React
- implement Accounting API
- implement Working API
- change JWT architecture
- change existing Django authentication

Only fix issues discovered during verification if they are clearly
required for correctness or security.

==================================================
1. AUTHENTICATION TESTING
==================================================

Verify:

- unauthenticated request → 401
- invalid JWT → 401
- valid JWT → authenticated
- inactive/unapproved user cannot access protected Inventory API

==================================================
2. AUTHORIZATION TESTING
==================================================

For every existing Inventory role, verify actual behavior for:

- GET
- POST
- PUT
- PATCH
- DELETE

Do not invent permissions.

Compare implementation against the approved Phase 3A authorization
matrix and the existing Django Inventory behavior.

Report any discrepancy.

==================================================
3. OBJECT-LEVEL AUTHORIZATION / IDOR
==================================================

Inspect whether Inventory endpoints can expose or modify records that
the authenticated user should not be allowed to access.

Test object-level access where applicable.

If no object-level restriction is required by the business rules,
document why.

==================================================
4. CRUD TEST COVERAGE
==================================================

Ensure tests cover:

Receipts:
- list
- retrieve
- create
- update
- partial update
- delete

Issues:
- list
- retrieve
- create
- update
- partial update
- delete

Summary:
- retrieve
- filtering

==================================================
5. SERIALIZER VALIDATION
==================================================

Test:

- required fields
- invalid values
- quantity validation
- unit-specific validation
- read-only fields
- unauthorized modification of nguoi_nhap
- unauthorized modification of nguoi_xuat

==================================================
6. BUSINESS LOGIC
==================================================

Verify that API writes do not bypass existing business rules.

Compare:

Django Template workflow

against:

REST API workflow

The API must not introduce a second conflicting implementation of
business rules.

==================================================
7. QUERY PERFORMANCE
==================================================

Inspect Inventory API query behavior.

Look for:

- N+1 queries
- unnecessary database queries
- missing select_related
- missing prefetch_related
- inefficient filtering

Do not perform speculative optimization.

Only make changes where there is a clear issue.

==================================================
8. PAGINATION
==================================================

Verify pagination works correctly for:

- receipts
- issues

Verify:

- page size
- next
- previous
- total/count behavior

Do not change global pagination unless necessary.

==================================================
9. FILTERING
==================================================

Verify existing summary filters:

- ma_hang
- mau
- other documented filters

Ensure invalid filters do not cause server errors.

==================================================
10. API CONTRACT
==================================================

Verify the actual API responses against docs/api.md.

Check:

- status codes
- JSON structure
- validation errors
- authentication errors
- permission errors
- not found errors

Documentation must match the implementation.

==================================================
11. REGRESSION
==================================================

Run:

- all Inventory legacy tests
- all Inventory API tests
- authentication tests
- relevant project tests

Existing Django Template functionality must remain intact.

==================================================
12. DATABASE SAFETY
==================================================

Confirm:

- no model changes
- no migration changes
- no schema changes

==================================================
13. FINAL REPORT
==================================================

Report:

1. Authentication verification
2. Authorization matrix
3. IDOR analysis
4. CRUD test coverage
5. Validation coverage
6. Business logic verification
7. Query analysis
8. Pagination verification
9. Filtering verification
10. API contract verification
11. Regression test results
12. Files modified
13. Database/model/migration changes

If changes were required, explain each one.

==================================================
STOP
==================================================

After verification, STOP.

Do not proceed to Accounting API.

Wait for explicit approval for the next phase.