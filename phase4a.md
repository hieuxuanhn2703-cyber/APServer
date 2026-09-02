# PHASE 4A — REACT FOUNDATION
## React Frontend Architecture & Project Initialization

You are working on the existing ProcessMonitoring project.

The backend migration to REST API has completed through Phase 3.

Completed backend domains:

- Authentication & Authorization
- Inventory REST API
- Accounting REST API
- Working REST API
- Dashboard API endpoints

Phase 3D-3 Working API Verification & Hardening has been completed and approved.

Your task is now ONLY:

> Build the React frontend foundation for the existing Django REST API architecture.

==================================================
0. ABSOLUTE SCOPE BOUNDARY
==================================================

This is PHASE 4A ONLY.

DO NOT migrate existing Django Template pages.

DO NOT rewrite existing Django frontend templates.

DO NOT remove Django templates.

DO NOT remove existing CSS.

DO NOT modify existing business logic.

DO NOT modify Django models.

DO NOT modify database schema.

DO NOT modify existing REST API behavior.

DO NOT create new API endpoints unless absolutely required for the React foundation.

DO NOT migrate Inventory screens.

DO NOT migrate Accounting screens.

DO NOT migrate Working screens.

DO NOT migrate Dashboard screens.

DO NOT redesign the existing UI.

DO NOT introduce Tailwind CSS.

DO NOT introduce a UI component framework such as:

- Material UI
- Ant Design
- Chakra UI
- Bootstrap React
- shadcn/ui

unless an existing project dependency already requires it.

The goal is to establish a clean, maintainable React foundation that can later receive migrated screens incrementally.

==================================================
1. FIRST: ANALYZE THE EXISTING PROJECT
==================================================

Before modifying anything, inspect the existing repository.

Read and respect:

.agents/rules/project.md
.agents/rules/frontend.md
.agents/rules/react.md
.agents/rules/api.md
.agents/rules/migration.md

Read relevant documentation:

docs/architecture.md
docs/frontend.md
docs/api.md
docs/migration.md
docs/backend.md

Inspect:

- Django project structure
- existing templates
- static files
- existing CSS
- existing JavaScript
- existing authentication flow
- existing navigation/sidebar
- existing URL structure
- REST API URL structure
- current role definitions
- existing frontend conventions
- existing cascade_select.js
- current package/environment configuration

Do NOT assume the project structure.

Use the actual repository structure as the source of truth.

Before implementation, determine:

1. Where the React application should live.
2. Whether a frontend directory already exists.
3. Whether package.json already exists.
4. Whether Node/npm configuration already exists.
5. Whether there are existing frontend build tools.
6. Whether the project already contains React dependencies.
7. Whether Django is currently serving static frontend assets.
8. How the eventual React build is expected to integrate with Django.

If there is an existing frontend structure, preserve it unless there is a strong architectural reason to change it.

==================================================
2. ARCHITECTURAL GOAL
==================================================

The target architecture is:

Browser
   |
   v
React Frontend
   |
   | HTTP/JSON + JWT
   v
Django REST API
   |
   v
Business Logic
   |
   v
MySQL Database

React is responsible for:

- UI
- components
- client-side routing
- client-side state
- API communication
- authentication state
- displaying validation errors
- displaying loading/error states
- role-based UI visibility

Django remains responsible for:

- database
- models
- business logic
- validation
- authorization
- JWT authentication
- API responses
- financial calculations
- inventory calculations
- production calculations
- dashboard aggregation

Never move business logic from Django into React.

==================================================
3. REACT APPLICATION INITIALIZATION
==================================================

Create the React application using the project's currently appropriate modern tooling.

Preferred:

- React
- Vite
- JavaScript or JSX unless the repository already uses TypeScript

Do NOT introduce TypeScript simply for preference if the existing project is JavaScript-based.

The application should have a clear development command, for example:

npm run dev

and a production build command:

npm run build

Do not unnecessarily add dependencies.

Keep package.json minimal.

==================================================
4. TARGET DIRECTORY STRUCTURE
==================================================

Use this architecture as the target direction:

frontend/
├── package.json
├── vite.config.js
├── index.html
│
└── src/
    ├── api/
    │   ├── client.js
    │   ├── auth.js
    │   ├── inventory.js
    │   ├── accounting.js
    │   └── working.js
    │
    ├── components/
    │   ├── common/
    │   ├── layout/
    │   └── auth/
    │
    ├── context/
    │   └── AuthContext.jsx
    │
    ├── hooks/
    │
    ├── layouts/
    │   └── AppLayout.jsx
    │
    ├── pages/
    │
    ├── routes/
    │   └── AppRoutes.jsx
    │
    ├── utils/
    │
    ├── App.jsx
    ├── main.jsx
    └── index.css

This is a target architecture, NOT a command to blindly create every file.

Only create files that are actually required for Phase 4A.

Keep empty directories out of git if they contain no meaningful files.

==================================================
5. API CLIENT FOUNDATION
==================================================

Create a centralized API client.

Do NOT allow components to directly use fetch() everywhere.

There should be one centralized mechanism responsible for:

- base API URL
- JSON headers
- Authorization header
- request handling
- response parsing
- common error handling

The API base should target:

/api/v1/

Do NOT hardcode localhost URLs into application code.

Use environment configuration where appropriate.

For example:

VITE_API_BASE_URL

with a sensible development default if necessary.

The API client should make it easy to later call:

/api/v1/auth/token/
/api/v1/auth/me/

/api/v1/inventory/...
/api/v1/accounting/...
/api/v1/working/...

Do NOT implement every endpoint yet.

Only establish the infrastructure.

==================================================
6. JWT AUTHENTICATION FOUNDATION
==================================================

The existing backend authentication contract is:

POST /api/v1/auth/token/

with:

{
    "account": "...",
    "password": "..."
}

The backend returns JWT credentials.

There is also:

GET /api/v1/auth/me/

The React foundation must be designed around this contract.

Implement the authentication infrastructure only.

Requirements:

- AuthContext
- login()
- logout()
- current user state
- authentication loading state
- authentication error state
- token storage abstraction
- authenticated API requests
- handling expired access tokens
- refresh-token mechanism if supported by the existing backend contract

Do NOT change the backend authentication implementation.

Do NOT change the AppUser password system.

Do NOT implement a new authentication system.

==================================================
7. TOKEN STORAGE
==================================================

Create a small abstraction for token storage rather than scattering:

localStorage.getItem(...)
sessionStorage.getItem(...)

throughout the application.

For example:

utils/tokenStorage.js

or another appropriate structure.

The rest of the application should not care where tokens are stored.

The implementation should make it possible to change storage strategy later without rewriting API calls.

Do not store passwords.

Do not log tokens.

Do not log authentication credentials.

==================================================
8. AUTH CONTEXT
==================================================

Create:

AuthContext

It should provide a clean interface similar to:

{
    user,
    isAuthenticated,
    isLoading,
    login,
    logout,
    refreshUser
}

The exact implementation may differ if the project architecture suggests something better.

After successful login:

1. receive JWT
2. store tokens through token storage abstraction
3. request /api/v1/auth/me/
4. populate current user
5. expose authentication state to the application

On logout:

1. clear stored tokens
2. clear user state
3. return application to unauthenticated state

Do not expose passwords or sensitive credentials through React state.

==================================================
9. ROLE FOUNDATION
==================================================

The existing system contains role-based authorization.

Do NOT redefine backend authorization rules in React.

Backend authorization remains authoritative.

React only uses the user's role for:

- navigation visibility
- route visibility
- UI convenience
- preventing users from seeing irrelevant controls

A malicious client must never be trusted merely because React hides a button.

The backend must continue enforcing permissions.

Create a clean mechanism for checking roles, for example:

hasRole(...)
hasAnyRole(...)

or an equivalent utility/hook.

Do not duplicate complicated permission logic from Django.

==================================================
10. ROUTING FOUNDATION
==================================================

Set up client-side routing.

The routing architecture should support:

- public routes
- authenticated routes
- role-aware routes

At minimum establish conceptual routes for:

/login

/

and placeholders for future application areas.

Do NOT implement actual business screens.

For example, placeholders may be simple:

Dashboard
Inventory
Accounting
Working

but they must NOT contain migrated business functionality.

Create a ProtectedRoute mechanism.

Unauthenticated users should not be able to access protected React routes.

Again:

React route protection is only UX protection.

Django API permissions remain the real security boundary.

==================================================
11. APPLICATION LAYOUT FOUNDATION
==================================================

Create the reusable application shell.

Expected conceptual structure:

App
 └── AuthProvider
      └── Router
           ├── Public routes
           └── Protected routes
                └── AppLayout
                     ├── Sidebar
                     ├── Topbar
                     └── Main content

Do NOT migrate the complete existing sidebar yet.

Do NOT migrate every menu item yet.

Create only the structural components needed to establish the layout architecture.

==================================================
12. EXISTING UI DESIGN MUST BE PRESERVED
==================================================

The current Django frontend already has an established design.

Do NOT redesign it.

Before creating CSS, inspect:

- existing sidebar CSS
- topbar CSS
- layout CSS
- typography
- spacing
- responsive behavior
- existing CSS naming conventions

When future screens are migrated, React should reproduce the existing visual design rather than inventing a new one.

For Phase 4A:

Create only the minimal CSS required for the foundation.

Do not create an entirely new design system.

Do not introduce Tailwind.

Prefer existing CSS conventions.

==================================================
13. RESPONSIVE FOUNDATION
==================================================

The current application supports responsive behavior.

The React layout foundation must not break this.

Establish structural support for:

- desktop
- tablet
- mobile

Do not spend Phase 4A implementing every responsive detail of every existing page.

That belongs to individual screen migration phases.

==================================================
14. ERROR / LOADING FOUNDATION
==================================================

Create reusable mechanisms/components for:

- loading state
- API error state
- unauthorized state
- forbidden state
- generic error state

Keep these components simple.

Do not build a complicated global design system.

==================================================
15. ENVIRONMENT CONFIGURATION
==================================================

Create appropriate environment configuration.

For example:

.env.development

and:

.env.production

only if actually necessary.

Do not commit secrets.

Do not put JWT tokens into .env files.

Do not put passwords or credentials into source code.

Document required environment variables.

==================================================
16. DJANGO INTEGRATION
==================================================

Do NOT immediately replace Django's existing frontend.

During Phase 4A:

Django Templates remain the existing production frontend.

React is established alongside the existing frontend.

The architecture should allow gradual migration.

The intended future transition is:

CURRENT:

Browser
   ↓
Django Templates
   ↓
Django

TARGET:

Browser
   ↓
React
   ↓
REST API
   ↓
Django

During migration, both systems may temporarily coexist.

Do not delete the existing templates.

==================================================
17. LEGACY JAVASCRIPT
==================================================

Do not migrate:

cascade_select.js

or other business-specific JavaScript yet.

Only inspect them to understand existing frontend behavior.

Their migration belongs to the appropriate screen migration phase.

Do not delete them.

==================================================
18. API DOMAIN MODULES
==================================================

Create API module boundaries for:

api/auth.js
api/inventory.js
api/accounting.js
api/working.js

However:

Do NOT implement every API function yet.

Create only the structure and, where useful, minimal health/auth functions required to verify the foundation.

The goal is separation:

components/pages
        ↓
domain API module
        ↓
central API client
        ↓
Django REST API

Avoid:

component
   ↓
fetch(...)
   ↓
hardcoded URL

==================================================
19. DO NOT OVER-ENGINEER STATE MANAGEMENT
==================================================

Do not introduce Redux unless the existing project clearly requires it.

For Phase 4A:

React Context is sufficient for authentication state.

Do not build a global state architecture for Inventory, Accounting, Working, etc. yet.

Those decisions should be made when the corresponding domain is migrated.

==================================================
20. TESTING / VERIFICATION
==================================================

After implementation, verify:

1. React development server starts.
2. React production build succeeds.
3. No ESLint/build errors if linting is configured.
4. Django backend still starts.
5. Existing Django templates still work.
6. Existing REST API tests still pass.
7. No database migrations were introduced.
8. No Django models were modified.
9. No existing API behavior was changed.
10. Login foundation can communicate with:
   POST /api/v1/auth/token/
11. Authenticated user can be retrieved through:
   GET /api/v1/auth/me/
12. Invalid credentials are handled correctly.
13. Unauthenticated protected React routes are blocked.
14. Logout clears authentication state.
15. Role information is available to React.
16. No password/token is printed to console.
17. React build does not modify legacy frontend behavior.

==================================================
21. BACKEND REGRESSION
==================================================

Run the existing relevant backend tests.

At minimum verify the API test suites that were already passing before Phase 4.

Do NOT modify backend tests simply to make Phase 4 pass.

If a pre-existing test fails, report it separately.

Remember the known existing issue:

Accounting.tests
test_team_revenue_pagination_5_per_page

This was already identified during Phase 3D-3.

Do NOT silently fix or rewrite that test as part of Phase 4A.

==================================================
22. GIT SAFETY
==================================================

Before implementation:

Run:

git status

Do not overwrite unrelated user changes.

Do not reset the repository.

Do not use:

git reset --hard

Do not delete untracked files.

Do not rewrite existing commits.

After implementation:

Run:

git status

and:

git diff --stat

Clearly identify:

NEW FILES
MODIFIED FILES
DELETED FILES

There should be NO intentional database schema changes.

==================================================
23. DOCUMENTATION
==================================================

Update documentation only where necessary.

If appropriate, add/update:

docs/frontend.md
docs/migration.md

Document:

- React application location
- development command
- production build command
- environment variables
- API base configuration
- authentication architecture
- token handling abstraction
- routing foundation
- relationship between React and Django

Do not create unnecessary documentation.

==================================================
24. REQUIRED FINAL REPORT
==================================================

When implementation is complete, DO NOT immediately proceed to Phase 4B.

Stop and produce a detailed report.

The report must contain:

## 1. Implementation Summary

What was created.

## 2. Project Structure

Show the final React directory tree.

## 3. Dependencies

List newly added npm packages and why they were needed.

## 4. API Architecture

Explain:

React
→ API modules
→ API client
→ Django REST API

## 5. Authentication Architecture

Explain:

Login
→ JWT
→ token storage
→ /auth/me/
→ AuthContext

## 6. Routing Architecture

Explain public/protected/role-aware routing.

## 7. State Management

Explain what uses Context and what intentionally does not exist yet.

## 8. Layout Foundation

Explain AppLayout / Sidebar / Topbar / Main content structure.

## 9. Django Compatibility

Confirm that existing Django Templates remain intact.

## 10. Legacy Frontend Compatibility

Confirm existing CSS/JS/templates were not unnecessarily modified.

## 11. Security Review

Explicitly confirm:

- no passwords stored
- no passwords logged
- no tokens logged
- backend remains authorization authority
- React role checks are UX-only
- JWT authentication uses existing backend contract

## 12. Database Safety

Confirm whether migrations/schema changes occurred.

Expected:

NONE.

## 13. Backend Regression

Report relevant test results.

## 14. React Verification

Report:

- npm install
- npm run build
- npm run dev
- authentication verification
- routing verification

## 15. Files Changed

Categorize:

NEW
MODIFIED
DELETED

## 16. Known Issues

Include the existing Accounting pagination test issue if it remains.

## 17. Phase 4A Verdict

Use exactly one:

PASS

PASS WITH CONDITIONS

NOT READY

==================================================
25. STOP CONDITION
==================================================

After completing Phase 4A:

STOP.

Do NOT:

- migrate Inventory
- migrate Accounting
- migrate Working
- migrate Dashboard
- migrate Django templates
- remove legacy frontend
- redesign the UI
- start Phase 4B automatically

Wait for explicit approval before proceeding.

The next phase will be separately reviewed and authorized.

==================================================
FINAL PRINCIPLE
==================================================

This phase is about building a stable foundation, not about migrating functionality.

Prefer:

SMALL
SAFE
REVERSIBLE
TESTABLE
DOCUMENTED

over:

FAST
LARGE
AUTOMATIC
DESTRUCTIVE

Preserve the existing application while creating the React architecture beside it.

Do not change working backend behavior merely to make the React architecture easier.

The existing Django REST API is the contract.

React must adapt to the API, not redefine the API.