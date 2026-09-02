# Phase 4C-1B — Accounting Dashboard Verification & Hardening

## 0. ROLE

You are working as a senior full-stack engineer and QA engineer on the existing `ProcessMonitoring` project.

The project is being migrated incrementally from:

> Django Templates + Vanilla JS/CSS

to:

> React + Django REST API

Phase 4C-1A — Accounting Dashboard Migration has already been implemented.

Your task is now:

> **Phase 4C-1B — Accounting Dashboard Verification & Hardening**

This phase is primarily a:

> **Verification + Functional Audit + Regression Testing + Hardening**

phase.

It is NOT a new feature-development phase.

---

# 1. PRIMARY OBJECTIVE

Verify that the React Accounting Dashboard implemented in Phase 4C-1A is:

* functionally correct
* consistent with the legacy Django Accounting Dashboard
* correctly integrated with the existing REST APIs
* correctly authorized
* resilient to loading/error/empty states
* responsive
* safe with payment mutations
* compatible with the existing legacy system
* free from unintended backend/database regressions

If defects are found:

> Fix only defects directly related to the Accounting Dashboard migration.

Do NOT use this phase as an opportunity for unrelated refactoring.

---

# 2. CURRENT IMPLEMENTATION

Phase 4C-1A reportedly implemented:

```text
/accounting
```

using:

```text
frontend/src/pages/AccountingDashboardPage.jsx
frontend/src/pages/AccountingDashboard.css

frontend/src/components/accounting/AccountingKPICards.jsx
frontend/src/components/accounting/AccountingProductFilter.jsx
frontend/src/components/accounting/AccountingSummaryTable.jsx
frontend/src/components/accounting/PaymentModal.jsx

frontend/src/api/accounting.js
```

The existing report is:

```text
docs/phase4c1a_accounting_dashboard_migration.md
```

Read the actual report and actual repository before beginning verification.

Do not assume that the report is correct simply because it says PASS.

---

# 3. CORE PRINCIPLE

The purpose of this phase is to answer:

> **Does the React Accounting Dashboard actually behave like the legacy Accounting Dashboard while correctly using the REST API architecture?**

The verification hierarchy is:

```text
Actual Backend/API
        ↓
Actual Legacy Django Dashboard
        ↓
Actual React Dashboard
        ↓
Automated Tests
        ↓
Build
```

When documentation conflicts with code:

> **ACTUAL CODE > DOCUMENTATION**

When React behavior conflicts with backend behavior:

> **BACKEND/API is authoritative**

When React behavior conflicts with legacy UI but the backend/API contract is correct:

> Determine whether the difference is an intentional migration adaptation or an actual regression.

Do not blindly force pixel-perfect legacy duplication.

---

# 4. STRICT SCOPE

## IN SCOPE

Verify and, if necessary, harden:

1. Accounting Dashboard route
2. Authentication integration
3. Role authorization UX
4. Accounting dashboard API integration
5. KPI cards
6. Delivery/export progress
7. Accounting summary table
8. Product filter
9. Payment creation
10. Payment history
11. Payment deletion
12. Dashboard refresh after mutations
13. Loading state
14. Empty state
15. Error state
16. 401 handling
17. 403 handling
18. Validation errors
19. Responsive layout
20. Legacy compatibility
21. Excel export
22. Team revenue link
23. API regression
24. Frontend build
25. Existing test suite relevant to this module
26. Documentation/report

---

# 5. STRICTLY OUT OF SCOPE

DO NOT migrate:

```text
Inventory Dashboard
Working Dashboard
Production detailed dashboard
KCS dashboard
Finishing dashboard
Kho dashboard
```

DO NOT implement:

* new Working APIs
* new Accounting business logic
* new database models
* database schema redesign
* migration of `cascade_select.js`
* global UI redesign
* Sidebar redesign
* authentication redesign
* JWT redesign
* new state-management architecture
* Redux
* Zustand
* MobX
* React Query
* SWR
* Tailwind
* Bootstrap
* MUI
* chart libraries

Do not modify unrelated modules.

---

# 6. FIRST STEP — READ THE PHASE 4C-1A REPORT

Read:

```text
docs/phase4c1a_accounting_dashboard_migration.md
```

Extract:

* files changed
* APIs used
* response structure
* payment payload
* role behavior
* verification already performed
* known issues

Then independently verify those claims against actual code.

Do NOT assume:

> "PASS in the report = verified behavior."

---

# 7. INSPECT ACTUAL IMPLEMENTATION

Inspect all relevant React files:

```text
frontend/src/pages/AccountingDashboardPage.jsx
frontend/src/pages/AccountingDashboard.css

frontend/src/components/accounting/AccountingKPICards.jsx
frontend/src/components/accounting/AccountingProductFilter.jsx
frontend/src/components/accounting/AccountingSummaryTable.jsx
frontend/src/components/accounting/PaymentModal.jsx

frontend/src/api/accounting.js
frontend/src/routes/AppRoutes.jsx
frontend/src/api/client.js
```

Also inspect actual equivalent paths if the repository differs.

Determine:

* component data flow
* API calls
* state management
* error handling
* refresh behavior
* role checks
* URL parameter handling
* modal lifecycle
* payment mutation behavior

---

# 8. INSPECT BACKEND SOURCE OF TRUTH

Inspect:

```text
Accounting/services.py
Accounting/views.py
Accounting/api/views.py
Accounting/api/serializers.py
Accounting/api/permissions.py
Accounting/models.py
Accounting/urls.py
Accounting/api/urls.py
```

and relevant tests.

Verify actual:

```text
GET /api/v1/accounting/dashboard/
POST /api/v1/accounting/payments/
DELETE /api/v1/accounting/payments/{id}/
```

Do not assume the report's API mapping is accurate.

Verify:

* request fields
* response fields
* validation rules
* permissions
* error responses
* payment relationships
* calculated fields
* filtering behavior

---

# 9. INSPECT LEGACY DASHBOARD

Inspect:

```text
Accounting/templates/accounting/dashboard.html
```

and every JS/CSS dependency used by the legacy page.

Search the repository for:

```text
accounting_dashboard
payment
payment history
export-excel
team-revenue
ma_hang
```

Determine the actual legacy behavior.

Build a verification matrix:

| Feature         | Legacy | API | React |
| --------------- | ------ | --- | ----- |
| KPI 1           |        |     |       |
| KPI 2           |        |     |       |
| KPI 3           |        |     |       |
| KPI 4           |        |     |       |
| Progress        |        |     |       |
| Product filter  |        |     |       |
| Summary table   |        |     |       |
| Create payment  |        |     |       |
| Payment history |        |     |       |
| Delete payment  |        |     |       |
| Excel export    |        |     |       |
| Team revenue    |        |     |       |

Fill this using actual code.

---

# 10. VERIFICATION CATEGORY A — ROUTING

Verify:

```text
/accounting
```

loads:

```text
AccountingDashboardPage
```

and not:

```text
AccountingPlaceholder
```

Verify the route is protected by the existing authentication architecture.

Verify direct navigation works.

Verify refresh/reload works.

Verify the intended application shell remains intact.

Do not modify global routing unless an actual Accounting migration defect exists.

---

# 11. VERIFICATION CATEGORY B — AUTHENTICATION

Verify:

## Logged out

Opening:

```text
/accounting
```

should follow the existing ProtectedRoute behavior.

Expected behavior:

```text
/accounting
     ↓
not authenticated
     ↓
/login
```

Do not implement custom login logic.

---

## Authenticated

An authenticated authorized user should be able to load the page.

---

## Token expiration

Verify that API requests rely on:

```text
apiClient
```

for:

```text
401
→ refresh
→ retry
```

Do not duplicate refresh logic inside Accounting components.

---

# 12. VERIFICATION CATEGORY C — ROLE AUTHORIZATION

Verify the actual backend permission:

```text
IsAccountingTeam
```

and the frontend role behavior.

Expected permitted roles are currently believed to be:

```text
PREMIUM
QUAN_LY
KE_TOAN
```

But verify the actual backend implementation.

Test at least:

```text
PREMIUM
QUAN_LY
KE_TOAN
KHO
BASIC
NHA_CAT
KCS
HOAN_THIEN
```

where test accounts/data are available.

Expected principle:

```text
Frontend role check = UX
Backend permission = security boundary
```

A forbidden role must NOT be granted data merely because React hides/shows a component.

---

# 13. 403 HARDENING

Simulate or verify an API `403`.

Expected:

```text
403
↓
show permission/access denied message
↓
user remains logged in
```

Must NOT:

```text
403
↓
logout
```

This distinction is mandatory.

---

# 14. VERIFICATION CATEGORY D — KPI DATA

Verify all four KPI cards.

Expected concepts from Phase 4C-1A:

```text
Tổng Giá Trị Đơn Hàng
Tổng Tiền Đã Xuất
Tiền Đã Thanh Toán
Tiền Chưa Thanh Toán
```

But verify actual backend field names and formulas.

For representative data:

```text
React KPI
    ==
API KPI
    ==
Legacy KPI
```

Do not accept visually plausible values.

Verify actual numerical equality.

Check:

* zero
* positive values
* debt
* no debt
* filtered product
* empty dataset

---

# 15. VERIFICATION CATEGORY E — PROGRESS

Verify:

* exported quantity
* ordered quantity
* percentage
* progress bar

For representative records:

```text
React progress
==
API result
```

Do not recalculate business logic independently in React.

Verify edge cases:

```text
0 ordered
0 exported
exported = ordered
exported < ordered
```

Ensure there is no:

```text
NaN
Infinity
undefined
```

in the UI.

---

# 16. VERIFICATION CATEGORY F — SUMMARY TABLE

Verify the actual table.

Expected Phase 4C-1A implementation contains 13 columns.

Verify against legacy:

* column names
* order
* data
* totals
* number formatting
* currency formatting
* percentage
* status/badge
* payment action

Verify representative rows.

For each important numeric field:

```text
API
==
React
==
Legacy
```

Do not merely compare screenshots.

---

# 17. VERIFICATION CATEGORY G — PRODUCT FILTER

Verify:

```text
?ma_hang=<value>
```

behavior.

Test:

1. no filter
2. select a product
3. refresh page
4. open copied URL
5. clear filter
6. select another product
7. invalid/nonexistent product if applicable

Verify:

```text
URL
↕
React state
↕
API query
↕
displayed data
```

Ensure clearing the filter restores the full dataset.

Verify there is no stale data displayed while a new filtered request is loading.

---

# 18. VERIFICATION CATEGORY H — PAYMENT CREATION

This is a critical mutation workflow.

Verify:

```text
Open payment modal
        ↓
Select/verify product
        ↓
Date
        ↓
Amount
        ↓
Optional note
        ↓
Submit
        ↓
POST API
        ↓
Success
        ↓
Refresh
```

Verify the actual serializer fields.

Do NOT assume the Phase 4C-1A report is correct without inspecting the serializer.

---

# 19. PAYMENT VALIDATION

Test:

* missing required field
* invalid amount
* zero amount if prohibited
* negative amount if prohibited
* invalid date
* excessive amount if backend prohibits it
* invalid product/color relationship if applicable

Backend validation remains authoritative.

Expected behavior:

```text
Backend validation error
        ↓
React displays useful field/form error
```

Do not swallow validation errors.

Do not display a generic "Something went wrong" when the backend has a useful validation message.

---

# 20. PAYMENT SUCCESS

After successful creation:

Verify:

```text
POST 201
        ↓
modal closes/resets appropriately
        ↓
dashboard refetch
        ↓
KPI updated
        ↓
table updated
        ↓
payment history updated
```

The frontend must not manually reconstruct accounting totals.

The backend remains the source of truth.

---

# 21. PAYMENT HISTORY

Verify:

* modal opens
* correct product/payment context
* payment date
* amount
* note
* creator/user
* ordering
* empty state

Compare with the actual backend response.

Do not invent missing fields.

If the backend is paginated, verify the UI handles pagination correctly rather than assuming all records are returned.

---

# 22. PAYMENT DELETE

Verify:

```text
Delete
↓
confirmation
↓
cancel
```

Cancel must NOT delete.

Then:

```text
Delete
↓
confirm
↓
DELETE API
↓
success
↓
refetch
```

Verify:

* table updates
* KPI updates
* debt updates
* payment history updates

Verify unauthorized deletion is rejected by backend.

Do not trust frontend-only hiding of the delete button.

---

# 23. DOUBLE-SUBMISSION / RACE CONDITIONS

Harden payment creation against accidental duplicate submission.

While POST is in progress:

* disable submit button
* prevent duplicate requests
* show submitting state

Similarly, during delete:

* prevent repeated delete requests
* show pending state

Do not introduce complicated state-management infrastructure.

Use local component state.

---

# 24. LOADING STATES

Verify:

## Initial load

Page should clearly communicate loading.

## Filter change

Avoid confusing stale results.

## Payment modal

Show loading when fetching relevant payment information if applicable.

## Create

Show submitting state.

## Delete

Show deleting state.

Do not freeze the entire application unnecessarily.

---

# 25. EMPTY STATES

Verify the following:

```text
No dashboard rows
No payment history
No product options
No matching filter result
```

Each must have a meaningful message.

Empty data must NOT be treated as:

```text
500
```

or a broken UI.

---

# 26. ERROR STATES

Verify:

### Network error

Display:

```text
error message
+
retry
```

### Server error

Display useful error state.

### 401

Use existing API client.

### 403

Permission message, no logout.

### Validation error

Show backend validation details.

### Unexpected response

Do not crash the entire React application.

---

# 27. ERROR RECOVERY

The "Thử lại" / retry action must actually retry the failed operation.

Verify:

```text
failure
↓
retry
↓
new API request
```

Do not simply hide the error banner without refetching.

---

# 28. RESPONSIVE VERIFICATION

Verify at:

```text
Desktop
Tablet
Mobile
```

At minimum inspect:

```text
>= 1024px
768–1023px
<= 640px
```

Verify:

* KPI cards
* filter toolbar
* table
* mobile cards
* modal
* buttons
* form fields
* horizontal overflow

No:

```text
horizontal page overflow
clipped modal
unreachable buttons
overlapping text
```

unless unavoidable and documented.

---

# 29. MOBILE PAYMENT MODAL

Pay particular attention to the payment modal on mobile.

Verify:

* modal fits viewport
* form fields remain usable
* buttons remain accessible
* payment history is readable
* scrolling works
* close button remains accessible

Do not allow the modal to create unusable page-level overflow.

---

# 30. EXCEL EXPORT

Verify:

```text
/accounting/export-excel/
```

still works from the React page.

Do NOT rewrite backend export functionality.

The React button/link should preserve existing behavior.

If the endpoint requires authentication, verify that the current application architecture handles it correctly.

If browser navigation to the legacy export endpoint is intentionally used, document the behavior.

---

# 31. TEAM REVENUE LINK

Verify:

```text
/accounting/team-revenue/
```

still works.

Do not migrate the Team Revenue page in this phase.

The Accounting Dashboard only needs to preserve the existing navigation/link behavior.

---

# 32. LEGACY REGRESSION

Verify that:

```text
/accounting/
```

still works independently.

Check:

* page loads
* legacy data renders
* payment functionality remains intact
* Excel export remains intact
* team revenue remains accessible

Do NOT delete or disable legacy functionality.

---

# 33. API CONTRACT REGRESSION

Run the actual Accounting API tests.

At minimum:

```text
python manage.py test Accounting.api.tests
```

Also run:

```text
python manage.py test Working.api.tests
```

because Phase 4C-1A uses:

```text
/api/v1/working/config/products/
```

for product options.

If the repository has broader relevant API tests, run them too.

---

# 34. FULL RELEVANT BACKEND VERIFICATION

Run:

```text
python manage.py check
```

Then:

```text
python manage.py makemigrations --check
```

There must be no unintended model changes.

If migrations are detected:

> STOP and investigate.

Do not create migrations merely to make the check pass.

---

# 35. FRONTEND BUILD

Run:

```text
npm run build
```

inside:

```text
frontend/
```

The build must succeed.

---

# 36. FRONTEND LINT / TESTS

Inspect the existing frontend tooling first.

If the project already has:

* test runner
* React Testing Library
* Vitest
* ESLint

use the existing setup.

If no frontend test framework exists:

> Do NOT install a new test framework solely for this phase without explicit approval.

At minimum:

```text
npm run build
```

must pass.

Do not modify package dependencies unnecessarily.

---

# 37. AUTOMATED TESTING REQUIREMENTS

If an existing frontend test framework is already available, add focused tests for:

### KPI

* renders API values
* formats values

### Filter

* updates URL
* triggers API reload

### Payment

* opens modal
* validates required fields
* submits once
* handles validation error
* refreshes after success

### Delete

* confirmation appears
* cancel does not delete
* confirm calls DELETE

### Authorization

* forbidden role does not expose Accounting functionality

### Error handling

* 403 does not logout
* network error shows retry

Do not create an elaborate test framework.

---

# 38. MANUAL BROWSER VERIFICATION

This phase MUST prioritize actual browser verification if the development environment permits it.

Perform a real manual test of:

```text
/accounting
```

Use realistic development/test accounts and existing test data.

Record observations.

If browser automation is unavailable:

> Do not falsely claim manual verification was completed.

Instead document:

```text
MANUAL VERIFICATION:
NOT AVAILABLE IN CURRENT ENVIRONMENT
```

and distinguish that from automated verification.

---

# 39. DATA CONSISTENCY TEST

Choose at least one representative dataset where values are known.

Record:

```text
Legacy value
API value
React value
```

for:

* total order value
* total exported value
* total paid
* outstanding amount
* export percentage
* at least one table row

Expected:

```text
Legacy == API == React
```

Any discrepancy must be investigated.

Do not simply mark it as "visual difference."

---

# 40. PAYMENT END-TO-END TEST

If safe test data/environment is available, perform:

```text
Initial state
↓
Create payment
↓
Verify API success
↓
Verify dashboard refresh
↓
Verify KPI change
↓
Verify table change
↓
Verify payment history
↓
Delete payment
↓
Verify dashboard returns to previous state
```

This is the most important end-to-end workflow in this phase.

Do not use destructive production data.

Only perform mutation testing against an explicitly safe development/test environment.

---

# 41. KNOWN LEGACY TEST ISSUE

Previously identified unrelated issue:

```text
Accounting.tests.AccountingTests.test_team_revenue_pagination_5_per_page
```

This test previously expected:

```text
5
```

but received:

```text
2
```

due to legacy fixture/date filtering behavior.

If encountered:

> DO NOT modify the test merely to make it pass.

Document it as:

```text
PRE-EXISTING / UNRELATED
```

unless you can prove Phase 4C-1A caused the regression.

---

# 42. BUG CLASSIFICATION

When a problem is found, classify it.

## P0 — Critical

Examples:

* unauthorized user receives accounting data
* payment can be duplicated due to frontend race
* payment deletion affects wrong record
* accounting totals are materially incorrect
* backend security boundary broken

Action:

> Fix before PASS.

---

## P1 — Major

Examples:

* payment creation does not refresh dashboard
* filter returns incorrect data
* payment history incorrect
* important KPI mismatch
* legacy Accounting dashboard broken

Action:

> Fix before PASS.

---

## P2 — Moderate

Examples:

* responsive issue
* incomplete error message
* modal usability issue
* formatting inconsistency

Action:

> Fix if directly related and low-risk.

---

## P3 — Minor

Examples:

* tiny spacing mismatch
* non-critical cosmetic issue

Action:

> May be documented and deferred if it does not affect functionality.

---

# 43. HARDENING RULE

Only fix issues that are:

```text
directly related to Phase 4C-1A
```

Examples of valid hardening:

* disable duplicate payment submit
* fix stale filter state
* fix payment refresh
* improve 403 handling
* fix mobile modal overflow
* correct API field mapping
* fix KPI display mismatch
* improve validation error mapping

Examples of invalid scope expansion:

* redesign Sidebar
* refactor all API services
* rewrite authentication
* redesign global CSS
* migrate Inventory
* migrate Working
* fix unrelated Accounting legacy tests
* rewrite Django architecture

---

# 44. NO BUSINESS LOGIC MIGRATION

If you discover:

```text
React calculation != Django calculation
```

do NOT automatically move or rewrite the business logic.

First determine whether:

1. React is incorrectly displaying backend data
2. React is incorrectly recalculating a value
3. Backend/API is incorrect
4. Legacy UI used a different presentation rule

Business calculations should remain in Django.

---

# 45. API SOURCE OF TRUTH

The dashboard API should remain the source for:

* KPI
* accounting totals
* progress
* summary rows

React should not recreate these from individual records unless the API contract explicitly requires it.

If React currently contains duplicated business calculations:

> Identify them and simplify/remove them if safe.

---

# 46. PAYMENT SOURCE OF TRUTH

Payment persistence must remain:

```text
React
  ↓
POST/DELETE
  ↓
Django
  ↓
Database
```

Do not directly manipulate database state from frontend.

Do not add alternative payment endpoints.

---

# 47. URL / ROUTING SAFETY

Do not change the meaning of:

```text
/accounting/
```

or other legacy routes.

The new React route:

```text
/accounting
```

must coexist according to the existing project routing design.

If both routes are intentionally present:

```text
/accounting
/accounting/
```

verify that both behave correctly.

Do not remove one merely because the other works.

---

# 48. SECURITY AUDIT

Verify:

* no password logging
* no JWT logging
* no refresh token logging
* no sensitive payment information unnecessarily logged
* no bypass of DRF permissions
* no hard-coded credentials
* no hard-coded authorization tokens

Inspect browser console/network logging introduced by the new components.

Remove accidental debug logs.

---

# 49. PERFORMANCE / REQUEST AUDIT

Inspect API request behavior.

Verify there is no accidental:

```text
infinite useEffect loop
```

or repeated dashboard fetching.

Expected behavior should be approximately:

```text
Initial page load → dashboard request
Filter change → dashboard request
Payment create → mutation + intentional refetch
Payment delete → mutation + intentional refetch
Retry → intentional refetch
```

Avoid unnecessary duplicate requests.

---

# 50. STALE STATE AUDIT

Check scenarios:

```text
Filter A
↓
Filter B
```

and:

```text
Open payment modal for Row A
↓
Change dashboard/filter
```

Ensure the modal does not accidentally display stale information from another row.

After mutation:

```text
dashboard
payment history
KPIs
table
```

must represent the same current backend state.

---

# 51. REPORTING REQUIREMENTS

Update or create:

```text
docs/phase4c1b_accounting_dashboard_verification.md
```

The report MUST include:

## 1. Phase

```text
Phase 4C-1B — Accounting Dashboard Verification & Hardening
```

## 2. Verification objective

Explain what was audited.

## 3. Files inspected

List relevant backend, legacy, and React files.

## 4. Files changed

List every file modified during hardening.

If no files were changed:

```text
No code changes required.
```

## 5. Verification matrix

Include:

| Area                 | Result    | Evidence |
| -------------------- | --------- | -------- |
| Routing              | PASS/FAIL |          |
| Authentication       | PASS/FAIL |          |
| Authorization        | PASS/FAIL |          |
| KPI                  | PASS/FAIL |          |
| Progress             | PASS/FAIL |          |
| Table                | PASS/FAIL |          |
| Filter               | PASS/FAIL |          |
| Payment create       | PASS/FAIL |          |
| Payment history      | PASS/FAIL |          |
| Payment delete       | PASS/FAIL |          |
| Loading              | PASS/FAIL |          |
| Empty state          | PASS/FAIL |          |
| Error handling       | PASS/FAIL |          |
| Responsive           | PASS/FAIL |          |
| Excel export         | PASS/FAIL |          |
| Team revenue         | PASS/FAIL |          |
| Legacy compatibility | PASS/FAIL |          |
| API regression       | PASS/FAIL |          |
| Build                | PASS/FAIL |          |

## 6. Data consistency

Document actual:

```text
Legacy
API
React
```

comparisons.

## 7. Payment E2E verification

Document the result.

## 8. Automated tests

Document exact commands and results.

## 9. Manual browser verification

Clearly state:

```text
PASS
```

or:

```text
NOT AVAILABLE
```

Do NOT claim manual testing if it was not actually performed.

## 10. Bugs found

For each:

```text
ID
Severity
Description
Root cause
Fix
Verification
```

## 11. Known unrelated issues

Keep pre-existing issues separate.

## 12. Scope compliance

Explicitly state:

* backend changed or not
* models changed or not
* migrations changed or not
* API contract changed or not
* new dependencies added or not

## 13. Final verdict

Use exactly one:

```text
PASS
```

```text
PASS WITH CONDITIONS
```

or:

```text
NOT READY
```

---

# 52. PASS CRITERIA

You may declare:

```text
PASS
```

only when all critical conditions are satisfied:

### Functional

* React Accounting Dashboard works.
* KPI values are correct.
* Progress is correct.
* Table data is correct.
* Filter works.
* Payment creation works.
* Payment history works.
* Payment deletion works.
* Dashboard refresh works after mutations.

### Security

* Correct roles have access.
* Unauthorized roles are denied.
* Backend permission remains authoritative.
* 403 does not logout.

### Reliability

* Loading works.
* Empty state works.
* Network/server errors work.
* Validation errors work.
* Retry works.
* Duplicate payment submission is prevented.

### Compatibility

* `/accounting/` legacy remains functional.
* Excel export remains functional.
* Team revenue remains functional.

### Technical

```text
python manage.py check
```

PASS.

```text
python manage.py makemigrations --check
```

PASS with no unintended changes.

Relevant backend API tests PASS.

```text
npm run build
```

PASS.

---

# 53. PASS WITH CONDITIONS

Use:

```text
PASS WITH CONDITIONS
```

when:

* core functionality is correct
* no security issue exists
* no data correctness issue exists
* only minor/non-blocking issues remain
* or manual browser verification is genuinely unavailable but automated/API verification is strong

Clearly document the conditions.

Do NOT use PASS WITH CONDITIONS to hide a P0/P1 defect.

---

# 54. NOT READY

Use:

```text
NOT READY
```

if any of the following remain:

* incorrect accounting values
* broken payment creation
* broken payment deletion
* unauthorized data access
* wrong API mapping
* broken legacy dashboard
* serious mutation/race issue
* database regression
* build failure
* critical API regression

---

# 55. FINAL RESPONSE FORMAT

At the end of execution, report:

```text
PHASE 4C-1B RESULT

Status:
PASS / PASS WITH CONDITIONS / NOT READY

Files changed:
...

Tests:
...

Manual verification:
...

Bugs fixed:
...

Known issues:
...

Next recommended phase:
...
```

Then:

> STOP.

Do NOT automatically begin:

```text
Phase 4C-2
Phase 4C-3
Phase 4C-4
Inventory migration
Working migration
```

Wait for further instructions.

---

# 56. FINAL ENGINEERING PRINCIPLE

The target architecture remains:

```text
React Accounting Dashboard
          │
          │ REST API
          ▼
Django REST Framework
          │
          ▼
Accounting Services
          │
          ▼
MySQL
```

The purpose of Phase 4C-1B is NOT to make React smarter.

The purpose is to prove that:

> **React is now a reliable presentation/client layer on top of the existing Django Accounting business logic and REST API.**

Preserve:

```text
Django = source of truth
React  = presentation + interaction
API    = contract
DRF    = security boundary
Legacy = fallback during migration
```

Do not break this architecture.

---

# 57. STOP CONDITION

After:

1. verification
2. necessary hardening
3. regression testing
4. documentation
5. final verdict

STOP.

Do not proceed to another phase without explicit instruction.
