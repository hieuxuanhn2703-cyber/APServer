# PHASE 4B — AUTHENTICATION & APPLICATION SHELL

## Complete React Auth Flow + Production-Ready Application Shell

You are working on the existing `ProcessMonitoring` project.

The project has completed **Phase 4A — React Foundation** and the Phase 4A report has been approved with verdict:

> **PASS**

Your task is now to implement **Phase 4B — Authentication & Application Shell**.

---

# 1. CURRENT PROJECT STATE

The migration is currently at:

```text
Phase 3A              ✅ APPROVED
Phase 3B              ✅ APPROVED
Phase 3C              ✅ APPROVED
Phase 3D              ✅ APPROVED
Phase 4A              ✅ APPROVED
Phase 4B              🚧 CURRENT TASK
```

The backend REST API foundation is already implemented and must be treated as the current API contract.

The React foundation already exists under:

```text
frontend/
```

The current React architecture includes:

```text
frontend/
└── src/
    ├── api/
    │   ├── client.js
    │   ├── auth.js
    │   ├── inventory.js
    │   ├── accounting.js
    │   └── working.js
    ├── components/
    │   ├── common/
    │   └── layout/
    ├── context/
    │   └── AuthContext.jsx
    ├── hooks/
    │   ├── useAuth.js
    │   └── useRoles.js
    ├── layouts/
    │   └── AppLayout.jsx
    ├── pages/
    │   ├── LoginPage.jsx
    │   ├── DashboardPlaceholder.jsx
    │   ├── InventoryPlaceholder.jsx
    │   ├── AccountingPlaceholder.jsx
    │   ├── WorkingPlaceholder.jsx
    │   └── NotFoundPage.jsx
    ├── routes/
    │   ├── AppRoutes.jsx
    │   └── ProtectedRoute.jsx
    └── utils/
        └── tokenStorage.js
```

Phase 4A already established:

* Vite + React
* React Router
* centralized API client
* JWT token storage abstraction
* AuthContext
* authentication foundation
* ProtectedRoute
* role-aware routing foundation
* Sidebar
* Topbar
* AppLayout
* Loading/Error/Unauthorized components
* domain API boundaries

Do NOT recreate these foundations blindly.

First inspect the actual current source code and improve/complete it in place.

---

# 2. PRIMARY OBJECTIVE

Implement Phase 4B as:

> **A complete, reliable authentication experience and a stable application shell for the future React application.**

Phase 4B must make the React application usable as an authenticated SPA while keeping the existing Django application fully operational.

The goal is NOT to migrate business modules yet.

After Phase 4B, the user should be able to:

```text
Open React app
      ↓
Login
      ↓
Receive JWT
      ↓
Restore session
      ↓
Fetch /auth/me/
      ↓
Enter protected application shell
      ↓
See role-appropriate navigation
      ↓
Navigate between placeholder module pages
      ↓
Logout
      ↓
Return to login
```

---

# 3. MANDATORY FIRST STEP — INSPECT BEFORE MODIFYING

Before changing code, inspect:

```text
frontend/package.json
frontend/vite.config.js
frontend/.env.development
frontend/.env.production

frontend/src/api/client.js
frontend/src/api/auth.js
frontend/src/utils/tokenStorage.js

frontend/src/context/AuthContext.jsx
frontend/src/hooks/useAuth.js
frontend/src/hooks/useRoles.js

frontend/src/routes/AppRoutes.jsx
frontend/src/routes/ProtectedRoute.jsx

frontend/src/layouts/AppLayout.jsx
frontend/src/components/layout/Sidebar.jsx
frontend/src/components/layout/Topbar.jsx

frontend/src/components/common/LoadingSpinner.jsx
frontend/src/components/common/ErrorState.jsx
frontend/src/components/common/Unauthorized.jsx

frontend/src/pages/LoginPage.jsx
frontend/src/pages/DashboardPlaceholder.jsx
frontend/src/pages/InventoryPlaceholder.jsx
frontend/src/pages/AccountingPlaceholder.jsx
frontend/src/pages/WorkingPlaceholder.jsx
frontend/src/pages/NotFoundPage.jsx

docs/frontend.md
docs/api.md
docs/architecture.md
docs/migration.md
```

Also inspect the relevant existing Django authentication implementation:

```text
Working.models.AppUser
/api/v1/auth/token/
/api/v1/auth/token/refresh/
/api/v1/auth/me/
```

Do not assume the report is identical to the current code.

The actual repository source code is authoritative for implementation details.

---

# 4. API CONTRACT — DO NOT CHANGE

The existing backend API is the contract.

The React frontend must consume the existing API.

Expected authentication endpoints include:

```text
POST /api/v1/auth/token/
POST /api/v1/auth/token/refresh/
GET  /api/v1/auth/me/
```

Login payload:

```json
{
  "account": "...",
  "password": "..."
}
```

Token response:

```json
{
  "access": "...",
  "refresh": "..."
}
```

User information is obtained from:

```text
GET /api/v1/auth/me/
```

Do NOT change:

* Django authentication logic
* Django models
* serializers
* API endpoint contracts
* JWT configuration
* token lifetime
* existing authorization classes
* existing database schema

unless a genuine blocking bug is discovered.

If a backend issue appears, document it instead of silently redesigning the backend.

---

# 5. PHASE 4B SCOPE

Implement the following areas.

## 5.1 Authentication Flow

Complete and harden:

```text
Login
Session restoration
Token refresh
Authenticated user state
Logout
Session expiration
Authentication errors
```

The AuthContext should provide a stable interface similar to:

```javascript
{
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    refreshUser
}
```

Preserve compatibility with the existing implementation where possible.

---

# 6. LOGIN PAGE

Make `LoginPage.jsx` a complete production-quality login page.

Requirements:

### Fields

```text
Account
Password
```

### Behaviour

Before submission:

* validate required fields
* prevent empty submission
* do not log credentials

During submission:

* disable submit button
* show loading state
* prevent duplicate requests

On successful login:

```text
POST /api/v1/auth/token/
        ↓
save access + refresh
        ↓
GET /api/v1/auth/me/
        ↓
update AuthContext
        ↓
navigate to intended destination
```

If the user originally attempted:

```text
/dashboard
```

then after successful login return to:

```text
/dashboard
```

If there is no previous destination:

```text
/
```

should perform the existing role-aware redirect.

---

# 7. LOGIN ERROR HANDLING

Handle at least:

```text
Invalid credentials
Inactive/unapproved account
Network error
Server error
Malformed response
Unexpected authentication failure
```

The UI must display a human-readable message.

Do NOT expose:

* stack traces
* raw server internals
* JWT tokens
* passwords
* sensitive debugging information

Do not use `alert()` for normal authentication errors.

---

# 8. SESSION RESTORATION

When the React application loads:

```text
AuthProvider
    ↓
check tokenStorage
    ↓
if no access token:
    unauthenticated

if access token exists:
    GET /api/v1/auth/me/
```

If the access token is expired:

```text
GET /auth/me/
    ↓
401
    ↓
refresh access token
    ↓
retry request
```

If refresh succeeds:

```text
store new access token
    ↓
retry original request
    ↓
restore authenticated session
```

If refresh fails:

```text
clear tokens
clear user
set unauthenticated
redirect /login
```

Avoid infinite refresh loops.

---

# 9. TOKEN MANAGEMENT

Continue using:

```text
src/utils/tokenStorage.js
```

All token access must go through this abstraction.

Do not scatter:

```javascript
localStorage.getItem(...)
localStorage.setItem(...)
localStorage.removeItem(...)
```

throughout the application.

No component should directly manipulate JWT storage.

Do not store:

```text
password
```

anywhere after login.

Never log:

```text
access token
refresh token
password
Authorization header
```

---

# 10. API CLIENT HARDENING

Review:

```text
src/api/client.js
```

Ensure there is one central HTTP abstraction.

Expected architecture:

```text
Component
   ↓
Domain API module
   ↓
apiClient
   ↓
HTTP
   ↓
Django REST API
```

Components must NOT independently implement authentication headers.

The client should:

1. attach access token when available
2. parse JSON responses consistently
3. normalize API errors where appropriate
4. detect `401`
5. attempt token refresh when appropriate
6. retry the original request once
7. prevent refresh loops
8. clear session when refresh fails

Be careful with concurrent requests.

If practical within the existing architecture, avoid multiple simultaneous refresh requests when several API calls receive `401` at the same time.

Do not introduce a large HTTP framework merely to solve this.

Use the existing lightweight implementation unless there is a concrete reason to change it.

---

# 11. LOGOUT

Implement reliable logout.

On logout:

```text
clear access token
clear refresh token
clear current user
clear authentication error state
```

Then navigate to:

```text
/login
```

The browser must not remain inside a protected page after logout.

After logout, attempting to open a protected route must return to:

```text
/login
```

Do not send the password anywhere during logout.

If the backend does not provide a logout endpoint, frontend logout is simply local token/session invalidation.

Do NOT invent a backend logout API.

---

# 12. PROTECTED ROUTES

Review:

```text
ProtectedRoute.jsx
AppRoutes.jsx
```

Required behaviour:

```text
Loading auth state
      ↓
LoadingSpinner
```

```text
Not authenticated
      ↓
Navigate /login
      ↓
preserve intended destination
```

```text
Authenticated
      ↓
render application
```

Protected routes currently include:

```text
/
/dashboard
/working
/inventory
/accounting
```

Keep placeholder pages for business modules.

Do NOT implement actual business screens in this phase.

---

# 13. ROLE-AWARE ROUTING

The application currently has role-aware navigation.

Preserve the backend role values exactly.

Do not invent new roles.

React may use role information for:

* navigation visibility
* default landing page
* UX
* route presentation

However:

> React role checks are NOT security controls.

Backend DRF authorization remains authoritative.

Do not remove backend permission enforcement.

---

# 14. ROLE-AWARE DEFAULT LANDING

Preserve the existing role-aware behaviour:

```text
QUAN_LY / KE_TOAN
    → /dashboard

KHO
    → /inventory

Production / worker role
    → /working
```

However, do not blindly assume role names.

Inspect the existing backend role definitions and current `useRoles.js`.

If the existing implementation already handles the exact project roles correctly, preserve it.

If a role is unknown:

```text
fallback → /dashboard
```

or another existing safe fallback consistent with the current application.

Do not invent new business behaviour.

---

# 15. APPLICATION SHELL

Complete and stabilize:

```text
AppLayout.jsx
Sidebar.jsx
Topbar.jsx
```

The shell should provide:

```text
┌─────────────────────────────────────┐
│ Sidebar │ Topbar                    │
│         ├───────────────────────────┤
│         │                            │
│         │ Main Content               │
│         │ <Outlet />                 │
│         │                            │
│         │                            │
└─────────────────────────────────────┘
```

The shell must work for:

* desktop
* tablet
* mobile

---

# 16. SIDEBAR

Sidebar must remain visually consistent with the existing Django application.

Use the existing design as the visual source of truth.

Do NOT redesign the product.

Sidebar should include:

* application branding
* role-aware navigation
* active route state
* user information where already supported
* logout action

Navigation must use React Router navigation.

Do not use full-page reloads for internal navigation.

---

# 17. SIDEBAR RESPONSIVENESS

Preserve the Phase 4A responsive behaviour:

Desktop:

```text
Expanded / collapsed sidebar
```

Tablet/mobile:

```text
Drawer
Backdrop
Open / close interaction
```

Requirements:

* clicking navigation closes mobile drawer
* clicking backdrop closes drawer
* logout closes drawer
* route changes correctly update active item
* no body overflow issues caused by open drawer
* keyboard accessibility where practical

Do not add a UI framework.

---

# 18. TOPBAR

Topbar should provide:

* sidebar toggle
* current page title
* authenticated user information where appropriate

Page title should reflect the current route.

For example:

```text
Dashboard
Working
Inventory
Accounting
```

Do not hardcode one title for the entire application.

Use the existing visual language.

---

# 19. USER INFORMATION

Use the authenticated user returned by:

```text
GET /api/v1/auth/me/
```

Expected information may include:

```text
id
account
name
role
is_approved
```

Do not display sensitive information.

Do not expose:

* password
* JWT
* refresh token
* internal authentication implementation details

---

# 20. COMMON UI STATES

Ensure reusable components exist for:

```text
Loading
Error
Unauthorized / Forbidden
Empty state where appropriate
```

At minimum:

```text
LoadingSpinner.jsx
ErrorState.jsx
Unauthorized.jsx
```

Avoid duplicating identical loading/error markup throughout pages.

Do not over-engineer a global UI state system.

---

# 21. 401 VS 403

Establish clear semantics:

### 401

Means:

```text
Not authenticated / session expired
```

Expected behaviour:

```text
attempt refresh
      ↓
if refresh fails
      ↓
logout
      ↓
login
```

### 403

Means:

```text
Authenticated but not authorized
```

Expected behaviour:

```text
show Unauthorized / Forbidden UI
```

Do NOT automatically logout a valid user because of a 403.

---

# 22. PLACEHOLDER MODULE PAGES

Keep:

```text
DashboardPlaceholder
InventoryPlaceholder
AccountingPlaceholder
WorkingPlaceholder
```

These pages should clearly communicate that the module is prepared for future migration.

Do NOT migrate actual business functionality in Phase 4B.

Do NOT connect unnecessary API calls just to make placeholders appear functional.

---

# 23. 404 PAGE

Ensure:

```text
*
```

continues to render:

```text
NotFoundPage
```

The page should provide a clear way to return to the application home page.

---

# 24. ENVIRONMENT CONFIGURATION

Preserve:

```text
VITE_API_BASE_URL
```

Use environment configuration rather than hardcoded deployment URLs.

Development may use:

```text
http://localhost:8000/api/v1
```

Production must remain configurable.

Do not hardcode:

```text
localhost
127.0.0.1
192.168.x.x
production domain
```

inside application source code.

---

# 25. VISUAL CONSISTENCY

The existing Django frontend remains the visual source of truth.

Inspect:

```text
Working/static/working/css/premium.css
Working/static/working/css/login.css
```

and related templates if needed.

Preserve:

* colour system
* typography
* spacing
* sidebar proportions
* active navigation style
* general visual hierarchy
* responsive behaviour

Known visual references include:

```text
#0f172a
#1e293b
#94a3b8
#f1f5f9
#ffffff
```

and the existing red active-state design.

Do NOT redesign the UI.

Do NOT introduce:

```text
Tailwind
MUI
Ant Design
Bootstrap
Chakra
shadcn
```

unless explicitly requested later.

---

# 26. ACCESSIBILITY

Within reasonable scope, improve basic accessibility:

* semantic buttons
* labels associated with form inputs
* keyboard-accessible controls
* visible focus states
* `aria-label` for icon-only buttons
* meaningful navigation labels
* password field uses correct input type

Do not turn this into a large accessibility rewrite.

---

# 27. PERFORMANCE / CODE QUALITY

Keep the implementation simple.

Avoid:

* unnecessary global state
* Redux
* Zustand
* MobX
* excessive abstraction
* premature optimization
* duplicated API logic
* duplicated authentication logic

React Context is sufficient for authentication state at this stage.

---

# 28. BACKEND PRESERVATION — ABSOLUTE RULE

Do NOT modify:

```text
Django models
Database schema
Migrations
Existing business logic
Existing templates
Existing legacy JavaScript
Existing legacy CSS
REST API contracts
JWT backend configuration
```

unless a concrete blocking defect is discovered.

The React application must coexist with Django.

The existing Django frontend must continue working.

---

# 29. DO NOT MIGRATE BUSINESS MODULES

This is extremely important.

DO NOT implement:

```text
Inventory screens
Accounting screens
Working screens
Dashboard business logic
Production forms
Material receipt forms
Material issue forms
Accounting reports
Production workflows
```

in Phase 4B.

Only the shell and authentication foundation are in scope.

The placeholder pages should remain.

---

# 30. DO NOT MIGRATE CASCADE SELECT

Do NOT migrate:

```text
cascade_select.js
```

yet.

This remains part of a later migration phase.

---

# 31. TESTING REQUIREMENTS

After implementation, perform actual verification.

## React

Run:

```bash
cd frontend
npm install
npm run build
```

Expected:

```text
BUILD SUCCESS
```

No build errors.

---

# 32. FRONTEND TEST MATRIX

Verify at minimum:

### A. Unauthenticated

```text
Open /
→ /login
```

### B. Login success

```text
Valid account/password
→ POST /auth/token/
→ token stored
→ GET /auth/me/
→ authenticated shell
```

### C. Invalid credentials

```text
Invalid account/password
→ error displayed
→ remain on login
→ no token stored
```

### D. Session restoration

```text
Refresh browser while authenticated
→ auth state restored
→ user remains logged in
```

### E. Access token expiration

```text
Protected API request
→ 401
→ refresh
→ retry
```

### F. Refresh failure

```text
refresh fails
→ tokens cleared
→ user cleared
→ /login
```

### G. Logout

```text
authenticated
→ logout
→ /login
→ protected routes blocked
```

### H. 403

```text
authenticated but unauthorized
→ Unauthorized UI
→ user remains authenticated
```

### I. Routing

Verify:

```text
/login
/
/dashboard
/inventory
/accounting
/working
/unknown-route
```

### J. Responsive shell

Verify:

```text
desktop
tablet
mobile
```

Sidebar and drawer must behave correctly.

---

# 33. BACKEND REGRESSION TESTS

After React changes, run the existing relevant backend tests.

At minimum verify the previously approved suites:

```bash
python manage.py test Working.api.tests
python manage.py test Working.tests
python manage.py test Inventory
```

If the project has broader API/auth regression tests, run those too when practical.

Do not modify tests simply to make them pass.

---

# 34. DATABASE SAFETY CHECK

Verify:

```bash
python manage.py makemigrations --check
```

Expected:

```text
No changes detected
```

or equivalent confirmation that no migrations were introduced.

Confirm:

```text
No Django models modified
No migrations created
No database schema changed
```

---

# 35. LEGACY FRONTEND REGRESSION

Confirm that the following remain intact:

```text
Django Templates
legacy CSS
legacy JavaScript
traditional Django routes
```

At minimum confirm the project still starts correctly.

If practical, verify representative legacy routes such as:

```text
/login/
/dashboard/
/working/
```

Do not replace these routes with React during this phase.

---

# 36. SECURITY CHECKLIST

Before declaring PASS, explicitly verify:

```text
[ ] Password is never stored
[ ] Password is never logged
[ ] Access token is not logged
[ ] Refresh token is not logged
[ ] Authorization header is not logged
[ ] No credentials are hardcoded
[ ] No JWT is hardcoded
[ ] Token access goes through tokenStorage
[ ] Backend remains authoritative for authorization
[ ] 401 and 403 are handled differently
[ ] Refresh loop is prevented
[ ] Logout clears tokens
[ ] Protected routes cannot be accessed unauthenticated
```

---

# 37. FILE SCOPE

Prefer modifying only files under:

```text
frontend/
```

and documentation such as:

```text
docs/frontend.md
```

Do not modify backend source unless absolutely necessary to fix a proven blocker.

Do not create unnecessary files.

Do not introduce unnecessary dependencies.

---

# 38. GIT / CHANGE SAFETY

Before modifying:

```bash
git status
```

Inspect the working tree.

Do NOT overwrite unrelated user changes.

Do NOT reset the repository.

Do NOT use destructive Git commands.

Do NOT delete unrelated files.

---

# 39. DOCUMENTATION

Update:

```text
docs/frontend.md
```

only as necessary to reflect the actual Phase 4B architecture and how to run the React application.

Do not create fake documentation describing features that were not implemented.

---

# 40. FINAL VERIFICATION REPORT

At the end, create:

```text
phase4b_report.md
```

The report MUST contain these sections:

```text
# PHASE 4B — AUTHENTICATION & APPLICATION SHELL

## 1. Implementation Summary
## 2. Authentication Flow
## 3. Token Management
## 4. API Client
## 5. Session Restoration
## 6. Logout
## 7. Protected Routes
## 8. Role-aware Navigation
## 9. Application Shell
## 10. Responsive Behaviour
## 11. Error / Loading / 401 / 403 Handling
## 12. Accessibility
## 13. Security Review
## 14. Django Compatibility
## 15. Legacy Frontend Compatibility
## 16. Database Safety
## 17. Backend Regression Tests
## 18. React Verification
## 19. Files Changed
## 20. Dependencies
## 21. Known Issues
## 22. Deferred Work
## 23. Final Verdict
```

---

# 41. FINAL VERDICT RULE

Use exactly one:

```text
PASS
PASS WITH CONDITIONS
NOT READY
```

### PASS

Use only when:

* authentication flow works
* protected routing works
* logout works
* session restoration works
* API client works
* shell works
* responsive behaviour works
* build succeeds
* relevant backend tests pass
* no database/model/migration changes
* legacy Django frontend remains intact
* no critical security issue

### PASS WITH CONDITIONS

Use when:

* Phase 4B is fundamentally complete
* but a minor non-blocking issue remains

Clearly list the issue.

### NOT READY

Use when:

* authentication is broken
* protected routing is broken
* build fails
* critical security problem exists
* backend regression is broken due to Phase 4B
* Django compatibility is broken
* database/model changes were introduced unexpectedly

---

# 42. STOP CONDITION — VERY IMPORTANT

After completing Phase 4B and writing:

```text
phase4b_report.md
```

STOP.

DO NOT automatically begin:

```text
Phase 4C
Inventory migration
Accounting migration
Working migration
Dashboard migration
```

Do not migrate any business screen.

Do not continue to the next phase without explicit approval.

The final response must summarize what was implemented, verification results, known issues, and the final verdict.

Then STOP.

---

# 43. IMPLEMENTATION PRINCIPLES

Throughout the entire task:

1. Inspect before modifying.
2. Preserve the existing architecture.
3. Preserve existing Django behaviour.
4. Treat existing REST APIs as contracts.
5. Keep backend authorization authoritative.
6. Keep React role checks UX-oriented.
7. Keep authentication centralized.
8. Keep token storage centralized.
9. Keep API calls centralized.
10. Avoid unnecessary dependencies.
11. Avoid unnecessary abstractions.
12. Do not redesign the UI.
13. Do not migrate business modules.
14. Do not modify the database.
15. Do not silently change API contracts.
16. Do not hide failing tests.
17. Do not fabricate successful verification.
18. Report actual commands and actual results.
19. Preserve unrelated user changes.
20. STOP after Phase 4B.

---

# 44. DEFINITION OF DONE

Phase 4B is complete when the following architecture is stable:

```text
                    ┌─────────────────────┐
                    │      React SPA      │
                    │                     │
                    │     LoginPage       │
                    │          │          │
                    │     AuthContext     │
                    │          │          │
                    │     tokenStorage    │
                    │          │          │
                    │      API Client     │
                    │          │          │
                    │    React Router     │
                    │          │          │
                    │      AppLayout      │
                    │       /     \        │
                    │   Sidebar  Topbar    │
                    │          │          │
                    │     <Outlet />       │
                    └──────────┬──────────┘
                               │
                         HTTP + JWT
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Django REST API   │
                    │                     │
                    │ /auth/token/        │
                    │ /auth/token/refresh │
                    │ /auth/me/           │
                    │                     │
                    │ Backend Auth        │
                    │ Backend Roles       │
                    │ Backend Permissions │
                    └──────────┬──────────┘
                               │
                               ▼
                         MySQL / Django
```

The React shell should now be ready for the next approved migration phase.

Again:

> **DO NOT migrate Inventory, Accounting, Working, Dashboard, or any other business screen during this task.**

Complete Phase 4B, verify it, write `phase4b_report.md`, provide the report summary, and STOP.
