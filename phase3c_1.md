# PHASE 3C-1 — ACCOUNTING API DISCOVERY & DESIGN

Inventory API has completed:

- API Foundation
- Authentication
- Authorization
- Implementation
- Verification & Hardening

Inventory API is now the REFERENCE ARCHITECTURE.

We are now beginning:

PHASE 3C-1 — ACCOUNTING API DISCOVERY & DESIGN

IMPORTANT:

This is a DISCOVERY AND DESIGN phase only.

DO NOT IMPLEMENT THE ACCOUNTING API YET.


==================================================
REFERENCE ARCHITECTURE
==================================================

Use the verified Inventory API as an architectural reference for:

- DRF project structure
- serializers
- ViewSets/APIViews where appropriate
- permissions
- services
- URL routing
- authentication
- pagination
- validation
- testing conventions

However:

DO NOT blindly copy Inventory implementation.

Accounting must be designed according to its actual models,
business rules, workflows and permissions.


==================================================
STRICTLY FORBIDDEN
==================================================

Do NOT:

- create Accounting API endpoints
- create Accounting serializers
- create Accounting ViewSets
- modify Accounting models
- modify migrations
- modify database schema
- modify existing Accounting views
- modify Accounting forms
- modify Accounting templates
- modify JWT authentication
- modify global permissions
- create React
- install React
- migrate Accounting frontend

This phase produces DESIGN ONLY.


==================================================
1. ACCOUNTING APPLICATION AUDIT
==================================================

Inspect the complete Accounting application.

Identify:

- models.py
- views.py
- urls.py
- forms.py
- templates
- services
- utils
- signals
- admin
- tests

Also inspect dependencies outside Accounting.

Determine whether Accounting depends on:

- Working
- Inventory
- ProcessMonitoring
- AppUser
- other applications


==================================================
2. MODEL ANALYSIS
==================================================

For every Accounting model identify:

- purpose
- primary key
- fields
- field types
- required/optional fields
- default values
- ForeignKeys
- OneToOne relationships
- ManyToMany relationships
- unique constraints
- indexes
- model methods
- properties
- signals

Create an actual relationship diagram based on source code.

Do not invent relationships.


==================================================
3. BUSINESS LOGIC
==================================================

Inspect:

- views.py
- forms.py
- services.py
- utils.py
- model methods
- signals

Identify all important business rules.

For each rule document:

- where it currently lives
- when it executes
- what data it affects
- whether it must remain backend authoritative

Pay special attention to:

- financial calculations
- totals
- status changes
- approval workflows
- date constraints
- duplicate prevention
- validation
- relationships with Inventory or Working


==================================================
4. EXISTING ACCOUNTING WORKFLOWS
==================================================

Trace existing Django Template workflows.

For every major workflow determine:

- URL
- HTTP method
- Django view
- form
- model
- permissions
- success behavior
- failure behavior
- redirect behavior

Do not assume standard CRUD.

Accounting may contain workflows that are NOT simple CRUD.


==================================================
5. ACCOUNTING ROLES
==================================================

Use the existing 8-role system.

Determine exactly which roles can:

- list
- retrieve
- create
- update
- delete
- approve
- perform other Accounting-specific actions

Do not invent permissions.

Compare:

Existing Django permissions

against:

Proposed API permissions.


==================================================
6. CROSS-MODULE DEPENDENCIES
==================================================

Determine whether Accounting interacts with:

- Inventory
- Working
- AppUser
- other modules

Document:

Accounting
    ↓
Inventory

or any other actual dependency.

Identify whether API endpoints should expose these relationships.

Do not create unnecessary nested APIs.


==================================================
7. API RESOURCE DESIGN
==================================================

Determine which Accounting models should become API resources.

Do NOT automatically expose every model.

For each proposed resource document:

- endpoint
- related model
- purpose
- list
- retrieve
- create
- update
- partial update
- delete
- custom actions if necessary
- filtering
- searching
- ordering
- pagination
- permissions


==================================================
8. CRUD VS BUSINESS ACTIONS
==================================================

This is especially important.

Determine whether each operation should be:

CRUD:

POST /resource/

or a business action:

POST /resource/<id>/approve/
POST /resource/<id>/close/

These are examples only.

Do not use custom actions unless the existing business workflow actually
requires them.

Do not model business workflows as generic CRUD merely because DRF
supports CRUD.


==================================================
9. SERIALIZATION DESIGN
==================================================

For each proposed resource determine:

- response fields
- create fields
- update fields
- read-only fields
- computed fields
- related object representation
- IDs vs nested objects

Do NOT create serializers yet.


==================================================
10. BUSINESS LOGIC BOUNDARY
==================================================

Determine which logic belongs in:

Django backend

versus:

React frontend

Default principle:

DJANGO:
- business rules
- financial calculations
- authorization
- validation
- state transitions
- database integrity

REACT:
- presentation
- local UI state
- user interaction
- display validation

React must never become authoritative for Accounting business rules.


==================================================
11. SECURITY
==================================================

Analyze:

- authentication requirements
- role permissions
- object-level authorization
- IDOR
- sensitive financial information
- unauthorized modification
- mass assignment risks
- read-only fields

Identify fields that must never be accepted from the client.

Do not implement fixes yet.


==================================================
12. QUERY PERFORMANCE
==================================================

Identify likely:

- N+1 queries
- select_related requirements
- prefetch_related requirements
- expensive aggregations
- pagination requirements

Do not perform speculative optimization.


==================================================
13. API CONTRACT
==================================================

Follow:

/api/v1/

and the conventions established by:

docs/api.md

Propose:

- endpoints
- HTTP methods
- status codes
- validation errors
- permission errors
- business-rule errors

Mark all proposed endpoints:

PROPOSED — NOT IMPLEMENTED


==================================================
14. PILOT RESOURCE
==================================================

Recommend the safest first Accounting API resource.

Explain:

- complexity
- dependencies
- business risk
- permission coverage
- CRUD complexity
- suitability for React migration

Do not assume the first model in models.py is the best pilot.


==================================================
15. TEST PLAN
==================================================

Design tests covering:

- authentication
- authorization
- roles
- CRUD
- validation
- business rules
- calculations
- relationships
- filtering
- pagination
- IDOR
- unauthorized fields
- state transitions
- custom actions if required

Do NOT write tests yet.


==================================================
16. DOCUMENTATION
==================================================

Update:

docs/api.md
docs/architecture.md
docs/migration.md

Clearly label all Accounting endpoints:

PROPOSED — NOT IMPLEMENTED


==================================================
17. FINAL REPORT
==================================================

Return:

1. Accounting architecture
2. Model relationship diagram
3. Cross-module dependencies
4. Existing workflows
5. Business rules
6. Role/permission matrix
7. Proposed API resources
8. Proposed endpoints
9. CRUD vs business-action analysis
10. Serialization design
11. Security analysis
12. Query/performance considerations
13. Recommended pilot resource
14. Test plan
15. Risks
16. Exact implementation plan for PHASE 3C-2

==================================================
STOP
==================================================

After producing the design report:

STOP.

Do NOT implement Accounting API.

Wait for explicit approval for:

PHASE 3C-2 — ACCOUNTING API IMPLEMENTATION