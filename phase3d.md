# PHASE 3D-3 — WORKING API VERIFICATION & HARDENING

The Working REST API has now been implemented.

IMPORTANT:

The implementation report claims 100% test success.

Do NOT assume the implementation is correct.

This phase is an independent verification and security audit.

DO NOT add new Working features unless a concrete defect is discovered.

DO NOT implement React.

DO NOT modify unrelated modules.

==================================================
1. COMPLETE API INVENTORY
==================================================

Enumerate every implemented Working API endpoint.

For each endpoint report:

- URL
- HTTP method
- ViewSet/APIView
- model/service used
- authentication requirement
- allowed roles
- object-level restrictions
- business actions

Compare actual implementation against:

docs/api.md
docs/architecture.md
docs/migration.md


==================================================
2. AUTHENTICATION
==================================================

Verify:

- no JWT → 401
- invalid JWT → 401
- valid JWT → authenticated
- inactive/unapproved AppUser → rejected
- request.user is the correct AppUser

Ensure API requests do not fall back to HTML login redirects.

==================================================
3. ROLE ISOLATION
==================================================

This is a HIGH PRIORITY audit.

Verify each production report endpoint against the actual
business role:

- CutReport → NHA_CAT
- ProcessReport → BASIC
- KcsReport → KCS
- FinishingReport → HOAN_THIEN

Test:

- correct role
- incorrect role
- QUAN_LY
- PREMIUM
- KE_TOAN
- unapproved users
- unauthenticated users

Do NOT assume that management roles automatically have access.

Compare against the approved Phase 3D-1 permission matrix.


==================================================
4. APpUSER SECURITY
==================================================

Audit AppUserViewSet.

Verify that responses NEVER expose:

- password
- password hashes
- authentication secrets
- internal security fields

Test whether a client can modify:

- account
- role
- approval status
- password
- privileged fields

through POST/PUT/PATCH.

These fields must be backend-controlled where appropriate.

Pay special attention to mass-assignment vulnerabilities.


==================================================
5. OBJECT-LEVEL AUTHORIZATION / IDOR
==================================================

For every Working resource determine whether records are:

- globally shared
- role-scoped
- user-scoped
- production-line scoped
- otherwise restricted

Attempt to:

User A
  ↓
GET/PATCH/DELETE
  ↓
User B's record

Verify the result according to actual business rules.

Do not merely test role-level permission.


==================================================
6. nguoi_nhap SECURITY
==================================================

For:

- CutReport
- ProcessReport
- KcsReport
- FinishingReport

verify:

Client sends:
"nguoi_nhap": another user

Expected:

The server ignores/rejects the spoofed value and uses:

request.user

Test both:

- create
- update

==================================================
7. BUSINESS ACTIONS
==================================================

Audit:

POST /exceptions/defects/<id>/receive/

Verify:

- authentication
- role authorization
- target object authorization
- valid state
- invalid state
- invalid quantities
- repeated receive
- concurrent/repeated requests where practical
- so_luong_treo calculation
- ReceiveLog creation
- no negative/invalid quantities
- transaction atomicity

The endpoint must not create partial database state if an operation fails.


==================================================
8. STATE TRANSITIONS
==================================================

Identify every status/state field used by Working APIs.

For each:

- current state
- allowed transition
- actor/role
- validation
- side effects

Attempt illegal transitions.

Ensure clients cannot bypass business workflow through generic PATCH/PUT.

==================================================
9. PRODUCT / CATALOG ENDPOINTS
==================================================

Verify:

- Product
- ProductColor
- ProductSize

Check:

- permissions
- read/write access
- filtering
- relationships
- pagination
- sensitive fields
- mass assignment
- invalid foreign keys


==================================================
10. SERIALIZATION
==================================================

Inspect every Working serializer.

For every field classify:

- writable
- read-only
- calculated
- server-controlled
- user-controlled

Attempt to submit unauthorized values.

Verify ForeignKey fields cannot be manipulated to create invalid
cross-object relationships.


==================================================
11. DASHBOARD / ANALYTICS
==================================================

Verify every dashboard endpoint.

Check:

- authentication
- role access
- returned data
- calculations
- empty data
- date filters
- query parameters
- unauthorized data exposure

Ensure dashboard calculations remain authoritative in Django.

Do not move calculations to React.


==================================================
12. QUERY PERFORMANCE
==================================================

Inspect:

- N+1 queries
- select_related
- prefetch_related
- aggregate queries
- dashboard queries
- pagination

Use query-count tests where appropriate.

Do not perform speculative optimization.


==================================================
13. VALIDATION
==================================================

Test:

- missing required fields
- invalid data types
- invalid foreign keys
- negative quantities
- invalid dates
- duplicate records
- invalid state transitions
- business-specific constraints

Expected result:

Controlled 400 responses rather than 500 errors.


==================================================
14. PAGINATION & FILTERING
==================================================

Verify all list endpoints.

Check:

- count
- next
- previous
- results

Verify all supported filters.

Test:

- valid filters
- invalid filters
- multiple filters
- empty results


==================================================
15. API CONTRACT
==================================================

Verify:

- URLs
- HTTP methods
- response structures
- status codes
- validation errors
- 401
- 403
- 404
- 409 if applicable

Compare implementation against docs/api.md.


==================================================
16. LEGACY REGRESSION
==================================================

Run:

1. Working API tests
2. Working legacy tests
3. Authentication tests
4. Inventory tests
5. Accounting tests
6. Full project test suite

Report EXACT commands and EXACT numbers.

Example:

Ran X tests in Y seconds
OK

Do not report only "100% passed".


==================================================
17. DATABASE SAFETY
==================================================

Verify:

- no unintended model changes
- no migrations
- no schema changes
- no data migration
- no destructive database operations

Report:

git status
git diff --stat
git diff -- migrations


==================================================
18. FILE AUDIT
==================================================

List every file changed during Working implementation.

Classify each:

NEW
MODIFIED
TEST ONLY
DOCUMENTATION

Pay special attention to:

Working/
ProcessMonitoring/
settings.py
requirements.txt


==================================================
19. TEST QUALITY AUDIT
==================================================

Do not merely run existing tests.

Inspect whether the tests actually test:

- forbidden roles
- object-level authorization
- mass assignment
- spoofed nguoi_nhap
- unauthorized state transitions
- repeated business actions
- sensitive fields
- IDOR

If a security test is missing, add the minimum necessary regression
test.

Do not add features.


==================================================
20. FINAL REPORT
==================================================

Return:

1. Complete endpoint inventory
2. Authentication verification
3. Complete role matrix
4. AppUser security audit
5. Object-level authorization / IDOR
6. nguoi_nhap security
7. Business action verification
8. State transition verification
9. Product/catalog verification
10. Serializer security
11. Dashboard verification
12. Query performance
13. Validation
14. Pagination/filtering
15. API contract
16. Legacy regression results
17. Database/migration status
18. Complete file audit
19. Test-quality audit
20. Remaining technical debt
21. Overall PASS/FAIL assessment


==================================================
IMPORTANT
==================================================

If you discover a real security or correctness defect:

1. Explain the defect.
2. Add the smallest necessary fix.
3. Add a regression test.
4. Re-run the relevant tests.
5. Report exactly what changed.

Do NOT redesign the architecture.


==================================================
STOP
==================================================

After completing verification:

STOP.

Do NOT implement React.

Wait for explicit approval for the next phase.