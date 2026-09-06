# PHASE 4C-2B-FINAL — BROWSER VERIFICATION CLOSURE

## 0. ROLE

You are acting as:

* Senior Full-Stack Engineer
* React Migration Architect
* QA Engineer
* Browser E2E Test Engineer
* Security Reviewer

You are working inside the existing `ProcessMonitoring` repository.

Your task is **ONLY** to perform the final Browser Verification and closure of:

> **Phase 4C-2B — Inventory Summary Verification & Hardening**

Do NOT start Phase 4C-3.

Do NOT redesign the UI.

Do NOT refactor unrelated code.

Do NOT modify backend/database architecture unless a small in-scope fix is absolutely required to make the existing Inventory Dashboard verifiable.

---

# 1. PRIMARY OBJECTIVE

The previous Phase 4C-2B report concluded:

> `PASS WITH CONDITIONS`

The ONLY remaining condition is:

> Browser Verification = `NOT AVAILABLE`

The previous browser verification could not start because the Playwright browser driver could not be downloaded from the upstream CDN.

Your primary objective now is:

1. Start the actual Django backend.
2. Start the actual React/Vite frontend.
3. Open the application using a real browser automation environment if available.
4. Execute the Browser Verification Matrix below.
5. Capture concrete evidence.
6. Fix only small, clearly in-scope issues discovered during verification.
7. Re-run the relevant tests after fixes.
8. Update the Phase 4C-2B verification report.
9. Decide whether the final status can legitimately become `PASS`.

IMPORTANT:

> NEVER claim browser verification was successful unless an actual browser session successfully opened the application and interacted with the UI.

If the browser automation environment is still unavailable, report:

> `Browser Verification = NOT AVAILABLE`

and keep the final verdict:

> `PASS WITH CONDITIONS`

Do NOT fabricate screenshots, DOM evidence, click results, network results, or browser observations.

---

# 2. SOURCE OF TRUTH

Before testing, inspect:

```text
docs/phase4c2_inventory_summary_migration.md
docs/phase4c2b_inventory_summary_verification.md
```

Then inspect the ACTUAL current implementation.

Relevant files include:

```text
Inventory/services.py
Inventory/views.py
Inventory/models.py
Inventory/urls.py
Inventory/api/views.py
Inventory/api/serializers.py
Inventory/api/permissions.py
Inventory/api/tests.py

ProcessMonitoring/urls.py

frontend/src/api/inventory.js
frontend/src/pages/InventoryDashboardPage.jsx
frontend/src/pages/InventoryDashboard.css
frontend/src/components/inventory/InventoryFilterBar.jsx
frontend/src/components/inventory/InventorySummaryTable.jsx
frontend/src/components/inventory/QuickIssueModal.jsx
frontend/src/routes/AppRoutes.jsx
frontend/src/hooks/useAuth.js
frontend/src/hooks/useRoles.js
frontend/src/api/client.js
```

Use:

> ACTUAL CODE > DOCUMENTATION

If documentation and implementation differ, trust the implementation and document the discrepancy.

---

# 3. ENVIRONMENT SETUP

Start the existing application without changing its architecture.

Expected development environment:

Backend:

```text
Django API
127.0.0.1:8000
```

Frontend:

```text
Vite
127.0.0.1:5173
```

Use the project's existing virtual environment and npm configuration.

Do NOT install unnecessary packages.

Do NOT upgrade dependencies merely to make the test environment work.

If Playwright/browser tooling is already available, use it.

If the browser driver is unavailable because of the environment, attempt only reasonable existing project/environment mechanisms.

Do NOT weaken the test by replacing browser verification with API-only tests.

---

# 4. BROWSER VERIFICATION RULE

The following distinction is mandatory:

### VALID Browser Verification

Evidence obtained from an actual browser session, for example:

* URL opened successfully
* visible UI elements
* actual button clicks
* actual form input
* actual dropdown selection
* actual modal interaction
* actual rendered table
* actual responsive viewport
* browser console
* browser network requests
* actual authentication behavior

### NOT Browser Verification

These alone are NOT sufficient:

* Django Test Client
* DRF APIClient
* unit tests
* static code inspection
* Vite build
* curl
* database queries
* source-code assertions

Those are supporting evidence only.

---

# 5. TEST ACCOUNT / ROLE MATRIX

Use safe development/test accounts already present in the project.

At minimum verify:

### Authorized role

Use a role that belongs to:

```text
KHO
PREMIUM
QUAN_LY
KE_TOAN
```

Prefer `KHO` for Quick Issue testing because the previous E2E verification used that role.

### Unauthorized role

Use:

```text
BASIC
```

Do NOT modify production data.

Do NOT create unnecessary persistent test data.

If a write operation is necessary, use a safe development/test transaction and rollback when possible.

---

# 6. TEST CASE A — ROUTING

Open:

```text
http://127.0.0.1:5173/inventory
```

Verify:

* Application loads successfully.
* `/inventory` renders `InventoryDashboardPage`.
* `InventoryPlaceholder` is not rendered.
* Sidebar/navigation remains functional.
* No unexpected redirect occurs for an authenticated authorized user.

Record browser evidence.

---

# 7. TEST CASE B — AUTHENTICATION

### B1 — Unauthenticated

Clear the authentication state.

Navigate to:

```text
/inventory
```

Expected:

```text
redirect → /login
```

Verify no protected Inventory data is displayed.

### B2 — Authenticated

Login with a valid authorized development account.

Navigate to:

```text
/inventory
```

Expected:

* Dashboard renders.
* API request succeeds.
* Inventory data appears.

---

# 8. TEST CASE C — AUTHORIZATION

Login as:

```text
BASIC
```

Navigate to:

```text
/inventory
```

Expected:

* Backend returns HTTP 403.
* React shows an appropriate access-denied message.
* User is NOT logged out.
* Access token remains valid.
* No redirect to `/login` occurs solely because of 403.
* User can still navigate to pages permitted to that role, especially `/working` if applicable.

This test is critical.

Verify using BOTH:

1. Browser-visible behavior.
2. Browser Network/API evidence.

---

# 9. TEST CASE D — INITIAL DATA RENDERING

With an authorized role:

Open:

```text
/inventory
```

Verify:

* Summary table renders.
* Headers are correct.
* Data rows are visible.
* Receipt values render correctly.
* Issue values render correctly.
* Balance values render correctly.
* Number formatting is correct.
* Unit formatting is correct.
* Stock status is visually distinguishable.
* `has_stock` behavior matches backend response.

Do not rely only on source code.

Inspect actual rendered browser content.

---

# 10. TEST CASE E — FILTER: MÃ HÀNG

Use:

```text
AT2
```

Expected:

* Filter is applied.
* URL query parameter contains:

```text
ma_hang=AT2
```

* Table updates.
* Only the expected AT2 records remain.

Clear the filter afterward.

---

# 11. TEST CASE F — FILTER: MÀU

Open the color filter.

Verify:

* Options are populated from actual data.
* Selecting a color changes the table.
* URL state updates appropriately.
* API request reflects the selected filter.
* Results match the selected color.

Clear afterward.

---

# 12. TEST CASE G — FILTER: TÊN VẬT TƯ

Select/type a valid material name.

Verify:

* URL state updates.
* API request contains the expected filter.
* Table results match the selected material.

Clear afterward.

---

# 13. TEST CASE H — FILTER: ĐƠN VỊ

Test at least:

```text
m
chiếc
y
```

Verify:

* Correct filtering.
* Correct URL query parameter.
* Correct table results.
* `chiếc` values display using integer formatting.

Clear afterward.

---

# 14. TEST CASE I — CLEAR ALL FILTERS

Apply multiple filters simultaneously.

Then click:

```text
Xóa tất cả lọc
```

Verify:

* All filters reset.
* URL query parameters are removed/reset.
* Full dataset returns.
* No stale filter remains in React state.

---

# 15. TEST CASE J — QUICK ISSUE MODAL

Using an authorized `KHO` account:

Find a row with valid stock.

Prefer:

```text
AT4
Tím
Khóa
chiếc
```

Click:

```text
Xuất
```

Verify the modal displays the correct contextual information:

* Mã hàng
* Màu
* Tên vật tư
* Đơn vị
* Current stock
* Quantity fields
* Receiver
* Date

Verify the modal is actually visible in the browser.

---

# 16. TEST CASE K — QUICK ISSUE VALIDATION

Test invalid input cases.

At minimum:

### K1

Quantity <= 0

Expected:

* submission blocked.

### K2

Negative quantity

Expected:

* submission blocked.

### K3

Empty receiver

Expected:

* submission blocked.

### K4

Unit = `chiếc`

Enter a fractional quantity.

Expected:

* validation rejects non-integer quantity.

Verify validation messages are visible and understandable.

---

# 17. TEST CASE L — DOUBLE SUBMISSION

Open Quick Issue.

Enter valid data.

Click Submit repeatedly/rapidly.

Expected:

* Only one request is submitted.
* Submit button becomes disabled while submitting.
* Relevant inputs are disabled.
* No duplicate issue record is created.

Verify through browser Network activity where possible.

---

# 18. TEST CASE M — QUICK ISSUE SUCCESS

Perform ONE safe development/test Quick Issue.

Verify:

### Browser

Success feedback appears.

### Network

Request:

```text
POST /api/v1/inventory/issues/
```

returns:

```text
HTTP 201
```

### Data

After refresh/re-fetch:

```text
issue quantity increases
balance decreases
```

### Security

`nguoi_xuat` is assigned by backend.

The frontend must NOT be able to spoof it.

If the application has a safe transactional test mechanism, rollback the test transaction afterward.

Otherwise use explicitly disposable development data.

DO NOT damage production/deployment data.

---

# 19. TEST CASE N — LOADING STATE

Throttle the API or otherwise introduce a controlled delay.

Reload `/inventory`.

Verify:

* Loading indicator appears.
* Loading text is visible.
* No misleading empty-state message appears during loading.
* Layout remains stable.

---

# 20. TEST CASE O — EMPTY STATE

Apply a filter combination that produces no rows.

Verify:

* Friendly empty-state message appears.
* No 500 error.
* No broken table layout.
* Filters remain usable.
* Clearing filters restores data.

---

# 21. TEST CASE P — ERROR + RETRY

Create a controlled API failure if safely possible.

Verify:

* Error banner/message appears.
* Application does not crash.
* Retry button appears.
* Clicking Retry triggers a new request.
* Successful recovery restores the dashboard.

Do NOT introduce destructive backend changes.

---

# 22. TEST CASE Q — JWT 401 REFRESH

If practical and safe within the existing authentication implementation:

Trigger an expired/invalid access token while a valid refresh token remains.

Verify:

* API client attempts refresh.
* Original request is retried once.
* User remains logged in if refresh succeeds.
* No infinite retry loop occurs.

If the environment makes this unsafe or impractical, document it honestly rather than fabricating a result.

---

# 23. TEST CASE R — LEGACY LINKS

From `/inventory`, click/inspect:

```text
/kho/nhap/
/kho/lich-su-nhap/
/kho/lich-su-xuat/
```

Verify:

* Links point to the correct legacy routes.
* Routes load successfully.
* No incorrect `/inventory/...` assumptions remain.

Also verify:

```text
/kho/tong-hop/
```

still loads successfully.

---

# 24. TEST CASE S — RESPONSIVE BROWSER VERIFICATION

Use actual browser viewport changes.

Test at approximately:

```text
1440 × 900
1024 × 768
767 × 900
390 × 844
```

Verify:

### Desktop

* Table visible.
* Header/layout intact.
* Filters usable.

### Tablet

* No horizontal layout break.
* Table remains usable or follows intended responsive behavior.

### Mobile

Expected responsive behavior:

* Desktop table hidden where designed.
* Mobile card view visible.
* Cards contain all important row information.
* Quick Issue remains accessible.
* No text overflow.
* Modal fits viewport.
* No unusable controls.

---

# 25. TEST CASE T — BROWSER CONSOLE

Inspect browser console.

Expected:

* No React runtime errors.
* No uncaught exceptions.
* No repeated warning spam.
* No accidental token/password logging.
* No obvious lifecycle warning.
* No broken asset warnings.

If warnings/errors exist:

1. Determine whether they are caused by Phase 4C-2B.
2. Fix only in-scope issues.
3. Re-run affected tests.

---

# 26. TEST CASE U — NETWORK VERIFICATION

Inspect browser Network requests.

Verify Inventory page uses the intended REST API:

```text
GET /api/v1/inventory/summary/
```

Verify Quick Issue uses:

```text
POST /api/v1/inventory/issues/
```

Verify:

* Authorization header is correctly handled by the existing API client.
* No unexpected legacy AJAX endpoint is used by the React Inventory Dashboard.
* Filters are passed correctly.
* 403 is handled inline.
* 401 follows existing refresh behavior.

Do NOT expose actual JWT values in the report.

---

# 27. TEST CASE V — REACT LIFECYCLE / RACE CONDITIONS

While using the browser:

* Rapidly change filters.
* Change filters several times before responses return if possible.
* Navigate away and back.
* Open/close Quick Issue repeatedly.
* Submit and close/reopen relevant UI.

Verify:

* No stale data remains unexpectedly.
* No duplicate API requests caused by lifecycle bugs.
* No state update errors.
* No React warnings.
* No uncontrolled re-fetch loop.

Pay particular attention to the previously fixed issue:

```text
allOptions.maHangList.length
```

must NOT unnecessarily trigger repeated `fetchSummary()` executions.

---

# 28. TEST CASE W — DATA CONSISTENCY

For at least the known development dataset:

```text
AT2
AT3
AT34
AT4
AT99
```

compare:

```text
Django Service Layer
        ↓
REST API response
        ↓
Actual Browser-rendered React UI
```

Verify these fields:

```text
ma_hang
mau
ten_vat_tu
don_vi

nhap_kien
nhap_so_luong

xuat_kien
xuat_so_luong

con_lai_kien
con_lai_so_luong

has_stock
```

The important requirement is:

> The values actually visible in the browser must match the API response.

Do not claim UI consistency based only on source inspection.

---

# 29. REGRESSION TESTS

After browser verification, run:

```bash
python manage.py check
```

Then:

```bash
python manage.py makemigrations --check
```

Then:

```bash
python manage.py test Inventory.api.tests
```

Then:

```bash
python manage.py test Working.api.tests Accounting.api.tests
```

Then:

```bash
cd frontend
npm run build
```

All must pass.

Expected baseline:

```text
Inventory.api.tests          13/13 PASS
Working + Accounting tests   15/15 PASS
Vite build                   0 errors
```

If existing unrelated test failures occur:

* Do NOT modify unrelated tests merely to make the suite green.
* Document them separately.
* Determine whether they are actually caused by your changes.

---

# 30. HARDENING RULES

If browser verification discovers a defect:

You MAY fix:

* Inventory React state bugs
* incorrect filter synchronization
* incorrect UI rendering
* modal validation
* double-submit issues
* race conditions
* lifecycle dependency problems
* error handling
* responsive CSS issues
* incorrect legacy links
* Inventory API client issues directly related to this dashboard

You MUST NOT:

* redesign the UI
* introduce a new UI framework
* introduce Redux/Zustand/TanStack Query/etc.
* rewrite unrelated components
* change database schema
* create unnecessary migrations
* modify unrelated Accounting/Working/KCS/Finishing functionality
* change backend business rules merely to fit the frontend
* change tests merely to make them pass

---

# 31. SECURITY REQUIREMENTS

Confirm:

* Passwords never appear in DOM.
* Access tokens never appear in rendered UI.
* Refresh tokens never appear in rendered UI.
* Tokens are not logged.
* `nguoi_xuat` cannot be spoofed from frontend.
* Backend remains the actual authorization boundary.
* 403 does NOT cause logout.
* BASIC cannot access Inventory API.
* Authorized roles can access Inventory API.

Never place real secrets/tokens in the final report.

---

# 32. EVIDENCE REQUIREMENTS

For every test, record:

```text
Test ID
Action
Expected Result
Actual Result
Status
Evidence
```

Use evidence such as:

* browser URL
* visible UI result
* browser screenshot if available
* Network request/result
* console result
* API response status
* automated test output

Do NOT manufacture evidence.

Clearly distinguish:

```text
BROWSER VERIFIED
```

from:

```text
AUTOMATED/API VERIFIED
```

---

# 33. REPORT UPDATE

Update:

```text
docs/phase4c2b_inventory_summary_verification.md
```

Do not create a misleading second report unless the existing project convention requires it.

Update the report with:

## Browser Verification

Include:

* browser environment
* browser/tool used
* exact URL
* date/time
* successful test cases
* failed test cases
* blocked test cases
* relevant evidence
* defects found
* fixes made
* regression results

---

# 34. FINAL VERDICT RULE

The final verdict MUST follow this exact rule.

## PASS

Only if:

* Actual browser successfully opened the application.
* Browser Verification completed.
* All critical browser tests passed.
* No blocking UI defect remains.
* Authorization/security behavior passed.
* Quick Issue browser flow passed.
* Data visible in UI matches API.
* Responsive behavior passed.
* Console/network behavior is acceptable.
* Regression tests pass.
* No migration/schema changes were introduced unnecessarily.

Then set:

```text
Current status:
PASS
```

and explicitly state that the previous condition has been closed.

---

## PASS WITH CONDITIONS

Use this if:

* Browser cannot be launched.
* Some browser tests remain unavailable.
* Environment prevents legitimate verification.
* Or a non-critical verification limitation remains.

Then:

```text
Current status:
PASS WITH CONDITIONS
```

Clearly list the remaining condition.

---

## NOT READY

Use this if:

* Browser verification reveals a blocking defect.
* Security behavior fails.
* Data mismatch exists.
* Quick Issue is broken.
* Regression tests fail because of this phase.
* React application crashes.
* Critical authorization behavior is incorrect.

---

# 35. IMPORTANT HONESTY RULE

The following statement MUST NOT be used unless it is actually true:

> "Browser Verification PASS"

Do NOT infer browser success from:

```text
Django tests
APIClient
curl
Vite build
source inspection
database assertions
```

If the browser driver is unavailable again, report exactly that limitation.

A truthful:

```text
PASS WITH CONDITIONS
```

is preferable to a fabricated:

```text
PASS
```

---

# 36. FINAL REPORT FORMAT

At the end of the report include:

```text
PHASE 4C-2B-FINAL — BROWSER VERIFICATION CLOSURE

Previous status:
PASS WITH CONDITIONS

Browser Verification:
[PASS / NOT AVAILABLE / FAILED]

Automated Verification:
PASS / FAIL

Security Verification:
PASS / FAIL

Data Consistency:
PASS / FAIL

Quick Issue E2E:
PASS / FAIL / NOT AVAILABLE

Responsive Verification:
PASS / FAIL / NOT AVAILABLE

Console / Network Verification:
PASS / FAIL / NOT AVAILABLE

Final status:
PASS / PASS WITH CONDITIONS / NOT READY

Remaining conditions:
- ...
```

If everything is genuinely verified, explicitly state:

```text
The Browser Verification condition from Phase 4C-2B has been closed.
Phase 4C-2B is now fully verified and accepted.
```

If browser verification remains unavailable, explicitly state:

```text
The Browser Verification condition could not be closed because the browser automation environment remains unavailable.
No browser result has been fabricated.
Phase 4C-2B remains PASS WITH CONDITIONS.
```

---

# 37. STOP CONDITION

After completing this task:

STOP.

Do NOT:

* begin Phase 4C-3
* migrate Production Dashboard
* modify Working Dashboard
* perform unrelated refactoring
* introduce new architecture

Your task ends with:

> Phase 4C-2B Browser Verification Closure + Updated Verification Report.
