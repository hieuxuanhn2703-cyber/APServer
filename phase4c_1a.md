# Phase 4C-1A — Accounting Dashboard Migration

## 0. ROLE

You are working as a senior full-stack engineer on the existing `ProcessMonitoring` project.

Your task is to implement:

> **Phase 4C-1A — Accounting Dashboard Migration**

The project is currently undergoing an incremental migration from:

> Django Templates + Vanilla JS/CSS

to:

> React + Django REST API

This is a **migration task**, not a redesign task.

You MUST inspect the actual repository before modifying code.

---

# 1. PRIMARY OBJECTIVE

Migrate the existing **Accounting Dashboard** from the legacy Django Template UI to the existing React frontend.

The target React page must reproduce the existing Accounting Dashboard's functionality and UI intent while consuming the already implemented REST APIs.

The main target route is:

```text
/accounting
```

The existing React route/placeholder must be inspected and replaced with the real Accounting Dashboard implementation.

The legacy Django Accounting Dashboard must remain functional as a fallback.

---

# 2. IMPORTANT PROJECT RULES

Follow these rules strictly.

## 2.1 ACTUAL CODE > DOCUMENTATION

If documentation conflicts with the actual repository:

> **Trust the actual code.**

Inspect:

* existing Django views
* services
* serializers
* API views/viewsets
* URLs
* templates
* JavaScript
* CSS
* React code
* tests

Do not assume field names, response structures, permissions, or business logic from documentation alone.

---

## 2.2 DO NOT REDESIGN THE UI

This is a migration.

Preserve the existing Accounting Dashboard's:

* information hierarchy
* labels
* terminology
* layout intent
* table structure
* KPI presentation
* filters
* modal behavior
* payment workflow
* visual meaning

You may adapt the layout to React when technically necessary, but do NOT introduce an unrelated new design.

Do not add unnecessary animations or visual effects.

---

## 2.3 FRONTEND / BACKEND RESPONSIBILITIES

### Django / API remains responsible for:

* database access
* business logic
* calculations
* aggregations
* validation
* authorization
* payment persistence
* payment deletion
* accounting KPI calculations

### React is responsible for:

* rendering UI
* component structure
* local UI state
* API calls through the existing API client
* loading states
* error states
* empty states
* modal state
* filter state
* URL state where appropriate
* formatting values for presentation

DO NOT duplicate Django business logic in React.

---

# 3. SCOPE

## IN SCOPE

Implement only the Accounting Dashboard migration.

Expected scope:

1. Accounting Dashboard React page
2. Accounting dashboard API service/client integration
3. KPI cards
4. Delivery/progress section
5. Accounting summary table
6. Product/code filter
7. Payment creation modal/form
8. Payment history modal
9. Payment deletion
10. Loading states
11. Empty states
12. Error states
13. Role-aware UI
14. Responsive layout
15. Existing React route integration
16. Verification/build
17. Phase report

---

## OUT OF SCOPE

DO NOT implement:

* Inventory Dashboard migration
* Working Dashboard migration
* Production detailed matrix migration
* new Working APIs
* new Accounting APIs
* API contract redesign
* database schema changes
* model changes
* migrations
* JWT redesign
* authentication redesign
* Sidebar redesign
* AppLayout redesign
* global navigation redesign
* `cascade_select.js` migration
* unrelated bug fixes
* unrelated test modifications
* UI framework installation
* chart library installation
* Redux/MobX/Zustand
* Tailwind
* Bootstrap
* Material UI

Do not silently expand the scope.

---

# 4. REQUIRED PRE-IMPLEMENTATION AUDIT

Before writing code, inspect the repository.

At minimum inspect:

## Backend

```text
Accounting/views.py
Accounting/services.py
Accounting/models.py
Accounting/urls.py
Accounting/api/
Accounting/templates/
```

Also inspect relevant:

```text
Accounting/tests/
Working/models.py
Working/views.py
```

and the actual API routing configuration.

---

## Legacy frontend

Find the actual Accounting Dashboard implementation.

Inspect:

```text
Accounting/templates/accounting/dashboard.html
```

and every JavaScript/CSS file used by that page.

Do not assume the exact filename/location.

Search for:

```text
/accounting/
dashboard
payment
payment history
export
product filter
ma_hang
```

Determine:

* which elements are rendered by Django
* which data comes from Django context
* which data is fetched asynchronously
* which JavaScript controls filters
* which JavaScript controls modals
* how payments are created
* how payment history is displayed
* how payments are deleted
* whether Excel export exists
* what roles can access each operation

---

# 5. INSPECT EXISTING REACT FOUNDATION

Before implementing, inspect:

```text
frontend/
frontend/src/
frontend/src/api/
frontend/src/auth/
frontend/src/components/
frontend/src/pages/
frontend/src/AppRoutes.*
```

Use the existing architecture from Phase 4A / 4B.

Especially inspect:

```text
frontend/src/api/client.js
frontend/src/auth/AuthContext.jsx
frontend/src/auth/useAuth.js
frontend/src/auth/useRoles.js
```

or their actual repository locations.

Do NOT create another authentication mechanism.

Do NOT manually implement JWT refresh in the Accounting page.

All authenticated API requests MUST go through the existing API client.

---

# 6. EXISTING API CONTRACTS

The Phase 4C-0 assessment established that Accounting APIs are READY.

Use the actual implementation as the source of truth.

Expected endpoints:

```text
GET  /api/v1/accounting/dashboard/
POST /api/v1/accounting/payments/
DELETE /api/v1/accounting/payments/{id}/
```

The dashboard endpoint may support filtering such as:

```text
?ma_hang=...
```

BUT:

> Inspect the actual API implementation and serializer before using any parameter.

Do NOT invent fields.

Do NOT assume response JSON structure.

Read the actual:

* API view
* serializer
* service
* URL configuration
* tests

and map the real response structure into React.

---

# 7. API SERVICE LAYER

Create or extend an Accounting-specific API service according to the existing React project conventions.

For example, if the existing architecture supports it, use something similar to:

```text
frontend/src/api/accounting.js
```

or an appropriate existing API module.

Do not create duplicate generic API infrastructure.

The service layer should encapsulate calls such as:

```text
getAccountingDashboard(...)
createPayment(...)
deletePayment(...)
```

Use the existing `apiClient`.

Do not call `fetch()` directly from multiple React components if the existing project architecture already provides a central API client.

---

# 8. AUTHENTICATION BEHAVIOR

Reuse the authentication system implemented in Phase 4B.

Do NOT:

* read JWT manually inside components
* duplicate token refresh logic
* store tokens in new locations
* implement another login mechanism
* log access tokens
* log refresh tokens
* log passwords

The existing API client already handles:

```text
401 → refresh → retry
```

including concurrent refresh protection.

The Accounting Dashboard should simply use that API client.

---

# 9. ROLE / AUTHORIZATION REQUIREMENTS

The Accounting Dashboard is intended for:

```text
PREMIUM
QUAN_LY
KE_TOAN
```

The exact permissions MUST be verified against the actual backend permission classes and API tests.

Important:

> React role checking is UX only.

Backend DRF authorization remains the actual security boundary.

The frontend should:

* show Accounting navigation/page only to permitted roles
* redirect unauthorized users according to existing application behavior
* display a meaningful permission error for a direct API `403`

Do NOT log the user out on `403`.

A `403` means:

> authenticated but not authorized.

Only authentication failure / refresh failure should trigger the existing logout behavior.

---

# 10. ACCOUNTING DASHBOARD FEATURES

Reproduce the existing dashboard functionality.

## 10.1 KPI CARDS

The legacy Accounting Dashboard contains four main KPI areas.

Inspect the actual legacy template/API response and reproduce all four.

Examples may include concepts such as:

* revenue
* delivery progress
* outstanding/debt
* payment-related values

BUT:

> Do NOT invent KPI names or calculations.

Use the actual existing backend response and legacy UI.

KPI values MUST come from Django/API business logic.

React should only format and display them.

---

# 11. DELIVERY / PROGRESS SECTION

Reproduce the existing delivery/progress visualization.

The Phase 4C-0 assessment indicates that the Accounting Dashboard contains a delivery progress section.

Use:

* actual API data
* existing business calculations
* existing labels

Do not create new business formulas in React.

CSS-based progress visualization is sufficient.

Do NOT install a charting library.

---

# 12. ACCOUNTING SUMMARY TABLE

Implement the Accounting summary table visible in the legacy dashboard.

Inspect the actual legacy implementation for:

* columns
* ordering
* number/date/currency formatting
* empty behavior
* totals
* product/code filtering

Preserve the existing meaning.

Do not arbitrarily rename columns.

---

# 13. PRODUCT / MA_HANG FILTER

Implement the existing Accounting product filter.

Determine from the backend/API:

```text
ma_hang
```

or the actual field name.

The filter must use real values returned by the API or otherwise available through the existing API contract.

Do NOT hard-code product codes.

If the dashboard endpoint supports:

```text
?ma_hang=...
```

use server-side filtering.

Prefer server-side filtering when the API explicitly supports it.

Do not assume client-side filtering is safe if the server response is aggregated or incomplete.

---

# 14. PAYMENT CREATION

Implement the payment creation workflow from the legacy dashboard.

Expected flow:

```text
User opens payment modal
        ↓
User enters required fields
        ↓
React performs basic UI validation
        ↓
POST /api/v1/accounting/payments/
        ↓
Django validates and persists
        ↓
Success
        ↓
Close/reset modal
        ↓
Refresh Accounting Dashboard data
```

Important:

> Django serializer/backend validation remains authoritative.

React must NOT duplicate complex business validation.

Inspect the actual serializer to determine:

* required fields
* field names
* allowed values
* number/date constraints
* related-object requirements
* error response format

Do not invent request payloads.

---

# 15. PAYMENT HISTORY

Implement the payment history modal according to the legacy UI.

The modal should display the actual payment records available through the existing Accounting API.

Inspect the API/viewset to determine the correct endpoint and response.

Do not assume that:

```text
GET /api/v1/accounting/payments/
```

has a specific pagination or field structure until you inspect it.

Handle:

* loading
* empty history
* API error
* normal data

---

# 16. PAYMENT DELETE

Implement payment deletion if the legacy UI supports it.

Expected endpoint:

```text
DELETE /api/v1/accounting/payments/{id}/
```

Flow:

```text
User chooses delete
        ↓
Show confirmation
        ↓
User confirms
        ↓
DELETE API request
        ↓
Success
        ↓
Refresh payment/dashboard data
```

Do not delete records optimistically unless the existing architecture clearly requires it.

Prefer server confirmation followed by refresh.

If deletion is not available for a role according to backend permission rules, the UI must respect that.

---

# 17. ERROR HANDLING

Implement clear states for:

## Loading

Show a spinner/skeleton/appropriate loading UI consistent with existing React foundation.

Do not display broken or half-rendered dashboard values.

---

## Empty

If the API returns no accounting data:

Display a clear empty state.

Do not treat an empty dataset as an error.

---

## 401

Do not implement custom refresh behavior in the page.

Allow the existing `apiClient` to handle:

```text
401 → refresh → retry
```

If refresh fails, existing authentication flow should lead to login.

---

## 403

Show a permission message.

Do NOT logout.

---

## 500 / Network error

Show a user-friendly error state.

Provide a retry action where appropriate.

Do not expose raw stack traces.

---

## Validation errors

When payment creation fails due to serializer validation:

Map backend validation errors into the form where practical.

Do not hide the actual useful validation message.

---

# 18. DATA REFRESH STRATEGY

After successful:

```text
POST payment
```

or:

```text
DELETE payment
```

refresh the relevant accounting data from the backend.

Preferred strategy:

```text
mutation
   ↓
successful response
   ↓
refetch
```

Do not duplicate accounting calculations in React.

The backend remains the source of truth.

---

# 19. STATE MANAGEMENT

Use the existing React architecture.

Preferred:

```text
useState
useEffect
useMemo
useCallback
URLSearchParams
existing AuthContext
```

Do NOT introduce:

```text
Redux
MobX
Zustand
React Query
SWR
```

unless the project already uses one of them.

Do not add a new state-management dependency merely for this page.

---

# 20. URL STATE

If practical and consistent with the existing project, preserve useful Accounting Dashboard state in URL parameters.

For example:

```text
/accounting?ma_hang=...
```

Only use parameters supported by the actual API.

Do not invent URL parameters without a reason.

The page should remain usable if opened directly at:

```text
/accounting
```

---

# 21. COMPONENT ARCHITECTURE

Use reusable React components where appropriate.

A possible structure is:

```text
frontend/src/pages/
    AccountingDashboardPage.jsx

frontend/src/components/accounting/
    AccountingKPICards.jsx
    AccountingProgress.jsx
    AccountingSummaryTable.jsx
    AccountingProductFilter.jsx
    PaymentCreateModal.jsx
    PaymentHistoryModal.jsx
```

However:

> Do not blindly create this exact structure.

First inspect the existing project conventions and follow them.

Avoid creating tiny components that provide no real value.

---

# 22. CSS

Use:

> Vanilla CSS only.

Reuse existing global styles/components where appropriate.

Do not install:

* Tailwind
* Bootstrap
* Material UI
* Ant Design
* Chakra
* other UI libraries

Do not redesign the entire application.

Accounting-specific styles should be scoped appropriately.

Avoid unnecessary global CSS changes.

---

# 23. RESPONSIVE BEHAVIOR

The migrated page must work on:

* desktop
* tablet
* mobile

Preserve the legacy responsive intent.

For tables:

### Desktop

Use the normal table layout.

### Tablet

Allow horizontal scrolling where necessary.

### Mobile

If the legacy design already provides a mobile card representation, preserve that behavior.

Do not force a huge desktop table into a tiny mobile viewport.

Do not redesign unrelated application pages.

---

# 24. ACCESSIBILITY

Maintain basic accessibility:

* semantic buttons
* labels for form controls
* modal close controls
* keyboard-accessible interactions
* visible focus states
* appropriate `aria` attributes where necessary

Do not sacrifice accessibility merely to copy legacy markup.

---

# 25. EXCEL EXPORT

Inspect whether the Accounting Dashboard contains an existing Excel export function.

If it exists:

> Preserve it.

Do NOT create a new export backend.

Do NOT rewrite the existing export logic unless absolutely necessary.

If the existing export is a legacy Django endpoint, React may navigate/open the existing endpoint rather than duplicating the functionality.

Do not change backend export behavior in this phase.

---

# 26. LEGACY PRESERVATION

This is critical.

The following legacy functionality MUST remain intact:

```text
/accounting/
```

and all existing Django Accounting routes/templates used by it.

Do NOT:

* delete the legacy template
* delete legacy JavaScript
* delete legacy CSS
* delete Django Accounting views
* remove old URLs
* replace `/accounting/` with React globally
* break the legacy dashboard

The new React page should coexist with the legacy system.

If the existing application currently routes:

```text
/accounting
```

to React while legacy Django uses:

```text
/accounting/
```

or vice versa, inspect the actual routing and preserve both paths according to the current architecture.

Do not change routing assumptions blindly.

---

# 27. BACKEND MODIFICATION POLICY

Ideally this phase requires:

> NO BACKEND CHANGES.

Before changing backend code, verify whether the existing API already provides everything required.

If a backend change appears necessary:

1. Stop and inspect the exact limitation.
2. Determine whether the requirement can be fulfilled using the existing API.
3. Do NOT modify models or database.
4. Do NOT create migrations.
5. Do NOT change API contracts casually.
6. If a backend change is genuinely unavoidable, document it clearly in the phase report.

Do not silently expand Phase 4C-1A.

---

# 28. TESTING

Before declaring completion, inspect the existing test infrastructure.

## Backend

Run relevant tests.

At minimum verify:

```text
python manage.py check
python manage.py makemigrations --check
```

Run the relevant Accounting API tests.

Do not modify unrelated tests merely to make the suite pass.

---

# 29. KNOWN UNRELATED ACCOUNTING TEST ISSUE

There is a previously known Accounting test issue:

```text
Accounting.tests.AccountingTests.test_team_revenue_pagination_5_per_page
```

The test has previously expected:

```text
5
```

but received:

```text
2
```

This appears to be a fixture/mock/data issue rather than a migration requirement.

If you encounter this test:

> DO NOT silently modify the test just to make it pass.

Report it as an existing/unrelated issue unless your Accounting Dashboard migration genuinely caused it.

---

# 30. FRONTEND BUILD

Run:

```text
npm run build
```

from:

```text
frontend/
```

The build must complete successfully.

Fix errors caused by your migration.

Do not introduce unrelated changes solely to silence warnings.

---

# 31. MANUAL VERIFICATION

If the environment allows it, manually verify:

## Authentication

* logged-out user cannot access Accounting Dashboard
* allowed user can access it
* unauthorized role does not receive inappropriate UI access

## Dashboard

* KPI values load
* progress section loads
* table loads
* product filter works
* empty state works

## Payments

* create payment
* validation errors display correctly
* successful creation refreshes data
* payment history opens
* delete confirmation works
* successful deletion refreshes data

## Error handling

* 401 behavior follows existing API client
* 403 does not logout
* network/server errors show meaningful UI

## Responsive

Verify desktop/tablet/mobile layouts.

## Legacy

Verify the legacy:

```text
/accounting/
```

still works.

---

# 32. COMPARISON AGAINST LEGACY

For the migrated Accounting Dashboard compare React against the legacy implementation.

Verify at minimum:

| Area                | React         | Legacy    |
| ------------------- | ------------- | --------- |
| KPI cards           | Match         | Reference |
| Progress            | Match         | Reference |
| Table columns       | Match         | Reference |
| Product filter      | Match         | Reference |
| Payment modal       | Match         | Reference |
| Payment history     | Match         | Reference |
| Delete payment      | Match         | Reference |
| Formatting          | Match intent  | Reference |
| Permissions         | Match backend | Reference |
| Responsive behavior | Equivalent    | Reference |

The goal is functional equivalence and preservation of UI intent, not pixel-perfect duplication.

---

# 33. DO NOT INVENT DATA

This rule is especially important.

Do NOT invent:

* KPI values
* API fields
* payment fields
* product fields
* permissions
* status values
* calculations
* endpoints
* URL parameters

If something is unclear:

> Inspect the actual backend implementation and legacy frontend first.

---

# 34. DO NOT HIDE PROBLEMS

If an API limitation prevents full migration:

Do not fake the data.

Do not implement a misleading approximation.

Document:

```text
LIMITATION
IMPACT
WHY IT EXISTS
RECOMMENDED FOLLOW-UP PHASE
```

and stop rather than silently changing scope.

---

# 35. IMPLEMENTATION SEQUENCE

Follow this sequence.

## Step 1 — Audit

Inspect:

* legacy Accounting dashboard
* backend service
* API
* serializers
* permissions
* existing React foundation
* existing route

Do not code yet.

---

## Step 2 — API mapping

Create a clear internal mapping:

```text
API response field
        ↓
React data model
        ↓
UI component
```

Use only actual fields.

---

## Step 3 — API service

Implement Accounting API calls using existing `apiClient`.

---

## Step 4 — Page shell

Replace the existing Accounting React placeholder with the actual page.

---

## Step 5 — KPI + progress

Implement the top-level Accounting dashboard sections.

---

## Step 6 — Summary table + filter

Implement the accounting table and product filtering.

---

## Step 7 — Payment creation

Implement modal/form + POST.

---

## Step 8 — Payment history

Implement history modal.

---

## Step 9 — Payment deletion

Implement confirmation + DELETE.

---

## Step 10 — States

Implement:

* loading
* empty
* error
* permission denied

---

## Step 11 — Responsive CSS

Ensure desktop/tablet/mobile behavior.

---

## Step 12 — Verification

Run:

```text
python manage.py check
python manage.py makemigrations --check
```

relevant backend tests, and:

```text
npm run build
```

Then manually compare React vs legacy.

---

# 36. ACCEPTANCE CRITERIA

Phase 4C-1A is considered successful only if:

### A. React Accounting Dashboard

```text
/accounting
```

loads the real React Accounting Dashboard instead of the placeholder.

---

### B. API integration

Dashboard data comes from:

```text
GET /api/v1/accounting/dashboard/
```

using the existing API client.

---

### C. KPI

All existing Accounting KPI information is reproduced correctly.

---

### D. Progress

Existing delivery/progress information is reproduced correctly.

---

### E. Table

Accounting summary table is reproduced with correct data and columns.

---

### F. Filter

Existing product/code filtering works using the actual API contract.

---

### G. Payment creation

Payment creation works through the existing API.

---

### H. Payment history

Payment history is displayed correctly.

---

### I. Payment deletion

Supported payment deletion works with confirmation and backend authorization.

---

### J. Authentication

Existing JWT/session architecture remains untouched.

---

### K. Authorization

Only appropriate roles can access Accounting functionality.

Backend remains the true security boundary.

---

### L. Error handling

Loading, empty, 401, 403, validation, and server/network errors are handled appropriately.

---

### M. Responsive

Desktop/tablet/mobile layouts are usable.

---

### N. Legacy compatibility

Legacy:

```text
/accounting/
```

continues to work.

---

### O. No database changes

```text
makemigrations --check
```

must show no unintended model changes.

---

### P. Build

```text
npm run build
```

must succeed.

---

# 37. DOCUMENTATION / PHASE REPORT

After implementation, create:

```text
docs/phase4c1a_accounting_dashboard_migration.md
```

The report MUST include:

## 1. Phase

```text
Phase 4C-1A — Accounting Dashboard Migration
```

## 2. Objective

What was migrated.

## 3. Files inspected

List important legacy/backend/frontend files inspected.

## 4. Files changed

List every changed file.

## 5. API mapping

Document the actual endpoints and response/request fields used.

## 6. React architecture

Document:

* page
* components
* API service
* state management
* routing

## 7. Features implemented

List:

* KPI
* progress
* table
* filter
* payment creation
* payment history
* deletion
* error states
* responsive behavior

## 8. Authorization

Document the actual role behavior.

## 9. Legacy compatibility

Confirm:

```text
/accounting/
```

remains functional.

## 10. Verification

Record results for:

```text
python manage.py check
python manage.py makemigrations --check
relevant backend tests
npm run build
manual verification
```

## 11. Known issues

Clearly separate:

```text
Phase-related issues
```

from:

```text
Pre-existing/unrelated issues
```

Include the known pagination test issue if encountered.

## 12. Scope compliance

Explicitly confirm whether any backend/model/database/API changes occurred.

## 13. Final verdict

Use exactly one:

```text
PASS
```

or:

```text
PASS WITH CONDITIONS
```

or:

```text
NOT READY
```

Explain the reason.

---

# 38. FINAL STOP CONDITION

After completing the implementation and report:

> STOP.

Do not automatically start:

* Phase 4C-1B
* Inventory migration
* Working migration
* Production detailed dashboard migration
* unrelated refactoring

Wait for further instructions.

---

# 39. IMPORTANT ENGINEERING PRINCIPLE

The migration must preserve this architecture:

```text
                    ┌──────────────────────┐
                    │    React Frontend    │
                    │                      │
                    │ AccountingDashboard  │
                    │ KPI / Table / Modal  │
                    └──────────┬───────────┘
                               │
                               │ REST API
                               ▼
                    ┌──────────────────────┐
                    │     Django DRF       │
                    │                      │
                    │ Auth / Permissions   │
                    │ Serializers          │
                    │ API Views             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Accounting Services  │
                    │                      │
                    │ Business Logic       │
                    │ Aggregations         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       MySQL          │
                    └──────────────────────┘
```

The most important rule is:

> **Do not move Accounting business logic into React.**

React replaces the presentation layer.

Django remains the source of truth for accounting calculations, authorization, validation, and persistence.

---

# 40. EXECUTION STYLE

Work carefully and incrementally.

Before every significant change:

1. inspect existing implementation
2. understand current behavior
3. make the smallest necessary change
4. verify
5. continue

Do not perform a large blind rewrite.

At the end, provide the Phase 4C-1A report and stop.
