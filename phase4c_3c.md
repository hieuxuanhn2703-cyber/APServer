# Phase 4C-3C: Production Dashboard Comprehensive Verification & Hardening

## ROLE

You are a Senior Full-Stack Engineer specializing in:

* Django REST Framework
* React 18 + Vite
* API integration
* Frontend migration verification
* Security / authorization
* Regression testing
* Browser-based verification
* Production hardening

You are working on the existing `ProcessMonitoring` project.

Your task is to execute **Phase 4C-3C: Production Dashboard Comprehensive Verification & Hardening**.

---

# 1. PRIMARY OBJECTIVE

Verify that the newly migrated React Production Dashboard from:

> Phase 4C-3B

is functionally equivalent to the intended legacy Production Dashboard behavior, correctly consumes the Phase 4C-3A APIs, respects authorization, preserves filtering/pagination/state behavior, and does not introduce regressions.

This phase is primarily:

> **VERIFY → IDENTIFY → FIX → RE-VERIFY**

It is NOT a new feature-development phase.

Do not expand the dashboard's functionality beyond what already exists in Phase 4C-3B unless a verification finding demonstrates that something required by the existing specification was accidentally omitted or incorrectly implemented.

---

# 2. IMPORTANT SCOPE BOUNDARY

## This phase MUST NOT automatically decommission legacy functionality.

Do NOT:

* delete legacy Django templates
* delete legacy views
* delete legacy URLs
* delete legacy JavaScript
* delete legacy CSS
* remove legacy dashboard endpoints
* remove legacy Excel export
* remove legacy production routes
* remove fallback functionality

The legacy implementation remains an important reference and regression oracle during this phase.

Any actual legacy decommissioning must be handled in a **separate explicitly authorized phase/gate**.

Therefore:

> "Legacy Decommissioning" is NOT part of Phase 4C-3C.

---

# 3. AUTHORITATIVE SOURCES

Before making any changes, inspect the actual repository.

Read:

### Project rules

* `.agents/rules/project.md`
* `.agents/rules/frontend.md`
* `.agents/rules/react.md`
* `.agents/rules/api.md`
* `.agents/rules/django.md`
* `.agents/rules/migration.md`
* `.agents/rules/database.md`
* `.agents/rules/git.md`

### Relevant skills

Read the applicable skills under:

* `.agents/skills/react-frontend-dev`
* `.agents/skills/django-to-react-migration`
* `.agents/skills/code-review-and-debugging`
* `.agents/skills/django-rest-api-dev`

### Phase documentation

Read:

* Phase 4C-3-0 assessment
* Phase 4C-3A report
* Phase 4C-3B report

Use the actual repository code as the final authority if documentation and implementation disagree.

---

# 4. EXISTING PHASE CONTEXT

Phase 4C-3A established:

### Tracking API

```text
GET /api/v1/working/dashboards/tracking/
```

Supports:

```text
ma_hang
mau
```

### Production report APIs

```text
GET /api/v1/working/reports/cut/
GET /api/v1/working/reports/process/
GET /api/v1/working/reports/kcs/
GET /api/v1/working/reports/finishing/
```

With:

```text
with_totals=true
```

for cumulative totals.

### Production dashboard roles

Allowed:

```text
PREMIUM
QUAN_LY
KE_TOAN
```

Workers such as:

```text
BASIC
NHA_CAT
KCS
HOAN_THIEN
KHO
```

must not have production dashboard access.

Backend authorization remains authoritative.

---

# 5. PHASE 4C-3B EXPECTED FRONTEND

The migrated React dashboard should contain:

```text
/dashboard
```

with five tabs:

```text
Tracking
Cut
Process
KCS
Finishing
```

Expected components include the equivalent of:

```text
ProductionDashboardPage
ProductionDashboardHeader
ProductionDashboardNav
ProductionFilterBar
OrderTrackingTable
StageSummaryCards
ProductionActivityTable
```

Do not assume these files still have exactly the same implementation. Inspect the actual code.

---

# 6. VERIFICATION STRATEGY

Perform verification at multiple levels:

```text
Legacy data
     ↓
Django service/business logic
     ↓
REST API
     ↓
React API client
     ↓
React state
     ↓
React components
     ↓
DOM
```

The goal is to verify the complete chain:

> **Legacy → Backend/API → React → DOM**

Do not treat a backend 887/887 consistency result as proof that the React UI is correct.

The UI itself must be verified.

---

# 7. STEP 1 — STATIC CODE AUDIT

Inspect the Phase 4C-3B implementation.

Verify:

## API layer

Check:

```text
frontend/src/api/client.js
frontend/src/api/working.js
```

Verify that:

* the centralized API client is used
* authentication headers/tokens are handled consistently
* endpoints are correct
* query parameters are encoded correctly
* no unnecessary duplicate API abstraction exists
* no direct `fetch()` calls bypass the existing API layer unless justified

---

## Routing

Inspect:

```text
frontend/src/routes/AppRoutes.jsx
```

Verify:

* `/dashboard` exists
* authorization is role-aware
* allowed roles are:

```text
PREMIUM
QUAN_LY
KE_TOAN
```

* unauthorized users are handled correctly
* React authorization is not being treated as the actual security boundary

---

# 8. STEP 2 — AUTHENTICATION & AUTHORIZATION MATRIX

Verify all relevant roles.

Create a test matrix similar to:

| Role            | Dashboard UI | Tracking API | Report APIs |
| --------------- | -----------: | -----------: | ----------: |
| PREMIUM         |        ALLOW |        ALLOW |       ALLOW |
| QUAN_LY         |        ALLOW |        ALLOW |       ALLOW |
| KE_TOAN         |        ALLOW |        ALLOW |       ALLOW |
| BASIC           |        BLOCK |        BLOCK |       BLOCK |
| NHA_CAT         |        BLOCK |        BLOCK |       BLOCK |
| KCS             |        BLOCK |        BLOCK |       BLOCK |
| HOAN_THIEN      |        BLOCK |        BLOCK |       BLOCK |
| KHO             |        BLOCK |        BLOCK |       BLOCK |
| Unauthenticated |        BLOCK |          401 |         401 |

Verify:

* UI route guard
* API authorization
* direct URL access
* direct API access
* expired/invalid authentication behavior where practical
* HTTP 401 vs 403 semantics
* a 403 must NOT incorrectly log the user out
* unauthorized users must not see production data

Do not weaken backend permissions to make frontend tests pass.

---

# 9. STEP 3 — TRACKING DASHBOARD VERIFICATION

Verify:

```text
/dashboard?tab=tracking
```

Check:

### Table structure

Expected:

* order/product information
* 17 tracking rows or current equivalent real dataset
* seven production stages
* correct `lam`
* correct `con`
* negative remaining values represented correctly
* totals row

Seven stages:

```text
nhan_btp
vao_chuyen
giua_chuyen
ra_chuyen
thu_hoa
la_thanh_pham
nhap_hoan_thien
```

---

# 10. TRACKING DATA RECONCILIATION

Select representative rows.

For each selected row compare:

```text
Backend API JSON
        ↓
React state
        ↓
Rendered DOM
```

Verify values exactly.

Where practical, verify all currently returned tracking rows.

Do not merely verify that the table has the correct number of rows.

Check actual numeric values.

Verify:

```text
lam
con
```

and relevant order quantity / totals.

Pay special attention to negative `con` values.

---

# 11. STEP 4 — TRACKING FILTER VERIFICATION

Test:

### Product filter

```text
ma_hang
```

Verify:

* filtered API request
* filtered UI
* clearing restores full dataset
* URL query updates correctly

### Color filter

```text
mau
```

Verify:

* color options depend on selected product where applicable
* selecting a color filters correctly
* clearing restores expected state

### Combined filter

Test:

```text
ma_hang + mau
```

Verify both are applied together.

### URL state

Verify:

```text
/dashboard?tab=tracking&ma_hang=...&mau=...
```

works correctly.

Test:

* refresh
* browser back
* browser forward
* direct URL navigation

---

# 12. STEP 5 — ACTIVITY DASHBOARDS

Verify all four:

```text
Cut
Process
KCS
Finishing
```

Each must consume the appropriate backend API.

Verify:

```text
with_totals=true
```

is used where required.

Check:

* table data
* KPI/summary cards
* cumulative values
* filters
* pagination
* loading state
* empty state
* error state

---

# 13. CUMULATIVE TOTAL VERIFICATION

This is a critical test.

The backend calculates cumulative totals chronologically.

Verify that React displays backend-provided cumulative values rather than recalculating them independently.

For each activity dashboard:

1. Open page 1.
2. Record cumulative values for the final row.
3. Navigate to page 2.
4. Verify the first row on page 2 continues the cumulative sequence from page 1.
5. Compare the values directly against API JSON.

Repeat for:

```text
Cut
Process
KCS
Finishing
```

Do not accept an implementation that resets cumulative totals at every page.

---

# 14. ACTIVITY FILTER MATRIX

Test each activity dashboard with:

### Product

```text
ma_hang
```

### Color

```text
mau
```

### Combined

```text
ma_hang + mau
```

### Date range

```text
start_date
end_date
```

Test:

* start only
* end only
* both
* clearing filters
* changing filters
* invalid/empty filter state where applicable

Verify:

> Filter change resets pagination to page 1.

---

# 15. PAGINATION VERIFICATION

Verify:

* page 1
* page 2
* last page
* next/previous controls
* disabled states
* empty final page behavior if applicable

Important:

> Pagination must not change cumulative semantics.

Also verify:

> Filter changes reset the page to 1.

---

# 16. URL STATE VERIFICATION

Verify that relevant state is represented consistently in URL query parameters.

Expected parameters may include:

```text
tab
ma_hang
mau
start_date
end_date
page
```

Verify:

1. Select filters.
2. URL changes.
3. Refresh browser.
4. State is restored.
5. Navigate Back.
6. Previous state is restored.
7. Navigate Forward.
8. Next state is restored.

Do not introduce unnecessary URL parameters that are not part of the existing design.

---

# 17. FILTER RESET VERIFICATION

For every applicable dashboard:

1. Apply filters.
2. Confirm filtered data.
3. Click Reset/Clear.
4. Verify UI controls reset.
5. Verify URL resets.
6. Verify page returns to 1.
7. Verify unfiltered data returns.

---

# 18. API REQUEST AUDIT

Use browser network inspection where available.

Verify:

* expected endpoints only
* correct HTTP methods
* correct query parameters
* authentication headers
* no accidental legacy dashboard data requests
* no duplicate requests caused by React effects
* no request loops
* no unnecessary requests when switching unrelated UI state

Pay particular attention to React `useEffect` dependencies.

---

# 19. CONSOLE AUDIT

Verify:

```text
Console errors = 0
Unexpected warnings = 0
```

Investigate:

* React warnings
* key warnings
* failed API requests
* undefined values
* unhandled promise rejections
* hydration-like issues if any
* routing errors

Do not simply hide warnings.

Fix their underlying cause when they are introduced by Phase 4C-3B.

---

# 20. RESPONSIVE VERIFICATION

Verify at least:

### Desktop

Approximately:

```text
1440px
```

### Tablet

Approximately:

```text
768px
```

### Mobile

Approximately:

```text
390px
```

Check:

* navigation
* filter controls
* tables
* horizontal overflow
* cards
* buttons
* text wrapping
* page usability

Do not redesign the UI.

Only fix clear layout defects.

---

# 21. LEGACY ↔ API ↔ REACT VERIFICATION

Build a small representative reconciliation matrix.

Example:

| Dataset            | Legacy | API | React DOM |
| ------------------ | -----: | --: | --------: |
| Tracking row A     |      X |   X |         X |
| Tracking row B     |      X |   X |         X |
| Cut activity       |      X |   X |         X |
| Process activity   |      X |   X |         X |
| KCS activity       |      X |   X |         X |
| Finishing activity |      X |   X |         X |

The exact values must come from actual project data.

Where practical, verify:

* order quantities
* stage quantities
* remaining quantities
* daily activity values
* cumulative values
* filtered results

Any mismatch must be investigated.

---

# 22. REGRESSION TESTING

Verify that previous migrated dashboards still work.

## Authentication

Verify:

```text
/login
```

Login/logout must remain functional.

---

## Accounting

Verify:

```text
/accounting
```

Check that the Phase 4C Accounting migration still works.

---

## Inventory

Verify:

```text
/inventory
```

Check that the Phase 4C Inventory migration still works.

---

## App shell

Verify:

* sidebar
* navigation
* role-aware menu behavior
* logout
* routing
* token/session handling

Do not introduce regressions in unrelated React pages.

---

# 23. BACKEND REGRESSION CHECKS

Run:

```bash
python manage.py check
```

Then:

```bash
python manage.py makemigrations --check
```

Then:

```bash
python manage.py test Working.api.tests
```

Then:

```bash
python manage.py test Working.tests
```

Do not modify tests merely to make them pass.

If an existing test fails because of a genuine regression, investigate and fix the implementation.

---

# 24. FRONTEND BUILD

Run:

```bash
npm run build
```

Verify:

* build succeeds
* no compilation errors
* no unexpected warnings
* no broken imports
* no missing assets

---

# 25. SECURITY AUDIT

Verify that React does NOT expose sensitive information.

Especially check:

* passwords
* password hashes
* authentication secrets
* unnecessary user fields
* internal security fields

Verify that:

> React role checks are UX behavior only.

Never rely on frontend authorization to protect API data.

---

# 26. SCOPE-CONTROLLED FIX POLICY

If you discover a defect:

### Allowed to fix

Clearly frontend-related defects introduced by Phase 4C-3B, such as:

* incorrect API parameter
* wrong rendering
* incorrect state synchronization
* pagination bug
* URL-state bug
* filter bug
* responsive layout defect
* incorrect role guard
* React runtime error
* duplicate request
* incorrect cumulative value rendering
* broken loading/error/empty state

### Avoid changing

* Django models
* database schema
* migrations
* production business calculations
* legacy production algorithms
* Phase 4C-3A API behavior
* backend authorization semantics

If you discover a genuine Phase 4C-3A backend defect:

> Document it as a blocker/finding.

Do NOT silently rewrite backend business logic during this frontend verification phase.

Only make backend changes if absolutely necessary for verification infrastructure, and document the reason explicitly.

---

# 27. DO NOT CHEAT THE VERIFICATION

Do NOT:

* change expected values to match incorrect UI
* modify tests simply to pass
* disable authorization
* mock production data when real data is available
* remove failing test cases
* suppress console warnings
* hide network errors
* claim browser verification without actually running it
* claim DOM/API reconciliation without comparing actual values
* claim full filter verification after testing only one filter
* claim cumulative pagination verification without testing page boundaries

Evidence must support every PASS claim.

---

# 28. BROWSER VERIFICATION

If browser/CDP infrastructure is available:

Create or update a verification script under:

```text
scratch/
```

for example:

```text
scratch/verify_production_dashboard_4c3c.mjs
```

It should cover as much of the following as practical:

1. Login
2. Dashboard navigation
3. Tracking tab
4. Cut tab
5. Process tab
6. KCS tab
7. Finishing tab
8. Tracking row count
9. Seven-stage structure
10. Tracking numeric values
11. Product filter
12. Color filter
13. Combined filter
14. Reset
15. URL state
16. Back/forward
17. Activity filters
18. Date filters
19. Pagination
20. cumulative continuation across pages
21. role access
22. unauthorized access
23. console errors
24. network errors
25. responsive layout

Do not claim tests that were not actually executed.

---

# 29. DOCUMENTATION

Create:

```text
docs/phase4c_3c_production_dashboard_verification.md
```

The document must contain:

## 1. Executive Summary

What was verified.

## 2. Scope

What was and was not included.

Explicitly state:

> Legacy decommissioning is NOT part of Phase 4C-3C.

## 3. Implementation Under Test

Relevant React components and API endpoints.

## 4. Verification Matrix

Include:

* authentication
* authorization
* tracking
* filters
* pagination
* cumulative totals
* URL state
* responsive
* console/network
* regression

## 5. Legacy ↔ API ↔ React Results

Show representative reconciliation results.

## 6. Automated Test Results

Record exact commands and results.

## 7. Browser Verification Results

Only record tests actually executed.

## 8. Findings

Classify each as:

```text
PASS
FIXED
BLOCKER
KNOWN LIMITATION
```

## 9. Changes Made

List every file modified during Phase 4C-3C and explain why.

## 10. Remaining Risks

Clearly identify anything not fully verified.

## 11. Final Verdict

Use exactly one:

```text
PASS
PASS WITH CONDITIONS
FAIL
```

---

# 30. FINAL VERDICT RULES

## PASS

Use only if:

* required functionality works
* authorization is correct
* API ↔ React data is correct
* critical filters work
* pagination works
* cumulative pagination works
* URL state works
* no meaningful console/network errors
* regression tests pass
* build passes
* no unresolved blocker exists

---

## PASS WITH CONDITIONS

Use if:

* core functionality is correct
* no critical security issue exists
* but a non-critical limitation remains

Document the limitation clearly.

---

## FAIL

Use if:

* production data is incorrect
* authorization is broken
* critical filters fail
* pagination/cumulative semantics are incorrect
* React cannot reliably consume the production APIs
* regression is introduced
* critical runtime errors remain

---

# 31. FINAL RESPONSE FORMAT

At the end, provide:

```text
PHASE 4C-3C RESULT

Status:
PASS / PASS WITH CONDITIONS / FAIL

Tests:
- manage.py check: ...
- makemigrations --check: ...
- Working.api.tests: ...
- Working.tests: ...
- npm run build: ...

Browser:
- Executed: YES/NO
- Result: ...

Data reconciliation:
- Legacy ↔ API: ...
- API ↔ React DOM: ...

Authorization:
- PREMIUM: ...
- QUAN_LY: ...
- KE_TOAN: ...
- Unauthorized roles: ...

Filters:
- Product: ...
- Color: ...
- Combined: ...
- Date: ...
- Reset: ...

Pagination:
- Basic pagination: ...
- Cumulative continuation: ...

URL state:
- Refresh: ...
- Back/Forward: ...

Responsive:
- Desktop: ...
- Tablet: ...
- Mobile: ...

Console/Network:
- Console errors: ...
- Network errors: ...

Regression:
- Login: ...
- Accounting: ...
- Inventory: ...
- App shell: ...

Files changed:
...

Documentation:
docs/phase4c_3c_production_dashboard_verification.md

Final Verdict:
PASS / PASS WITH CONDITIONS / FAIL
```

---

# 32. MOST IMPORTANT RULE

Do not confuse:

> "The backend API is correct"

with:

> "The React dashboard is correct."

This phase exists specifically to prove the complete chain:

```text
Legacy behavior
      ↓
Django service
      ↓
REST API
      ↓
React API client
      ↓
React state
      ↓
React component
      ↓
DOM
```

The final verdict must be based on actual evidence from this complete chain.

And again:

> **Do NOT delete or decommission the legacy dashboard during Phase 4C-3C.**
