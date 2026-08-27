# PHASE 3D-1 — WORKING API DISCOVERY & DESIGN

Inventory API and Accounting API have completed:

- Implementation
- Verification
- Regression testing
- Security review

They are now the reference architecture for the REST API layer.

We are now beginning:

PHASE 3D-1 — WORKING API DISCOVERY & DESIGN

IMPORTANT:

THIS IS A DISCOVERY AND DESIGN PHASE ONLY.

DO NOT IMPLEMENT THE WORKING API.


==================================================
REFERENCE ARCHITECTURE
==================================================

Use Inventory and Accounting APIs as architectural references for:

- DRF structure
- serializers
- permissions
- services
- ViewSets/APIViews
- routing
- filtering
- pagination
- testing
- authentication

However:

DO NOT blindly copy them.

Working must be designed according to its actual business logic.


==================================================
STRICTLY FORBIDDEN
==================================================

Do NOT:

- create Working API endpoints
- create serializers
- create ViewSets
- modify Working models
- create migrations
- modify database schema
- modify existing Working views
- modify existing Working forms
- modify templates
- modify authentication
- modify JWT configuration
- modify global permissions
- create React
- install React
- migrate Working frontend

This phase produces DESIGN ONLY.


==================================================
1. COMPLETE WORKING APPLICATION AUDIT
==================================================

Inspect the complete Working application.

Analyze:

- models.py
- views.py
- urls.py
- forms.py
- templates
- services.py
- utils.py
- signals.py
- admin.py
- tests
- template tags
- middleware
- static JavaScript
- static CSS

Do not limit analysis to models.py.


==================================================
2. MODEL INVENTORY
==================================================

For EVERY Working model document:

- purpose
- primary key
- fields
- field types
- defaults
- nullable fields
- ForeignKeys
- OneToOne
- ManyToMany
- unique constraints
- indexes
- model methods
- properties
- signals

Create a real relationship diagram from source code.

Do not invent relationships.


==================================================
3. BUSINESS DOMAIN MAP
==================================================

Identify the major Working domains.

Examples only:

- users
- production
- products
- orders
- processes
- tracking
- reports
- dashboards

Use actual project terminology.

For each domain identify:

- models
- views
- forms
- templates
- business logic
- permissions
- dependencies


==================================================
4. EXISTING USER WORKFLOWS
==================================================

Trace actual Django Template workflows.

For every major workflow document:

User
 ↓
URL
 ↓
View
 ↓
Form
 ↓
Validation
 ↓
Model
 ↓
Business logic
 ↓
Redirect / response

Identify:

- GET flows
- POST flows
- edit flows
- delete flows
- approval flows
- tracking flows
- dashboard flows

Do not assume CRUD.


==================================================
5. BUSINESS LOGIC EXTRACTION ANALYSIS
==================================================

Identify logic currently located in:

- views.py
- forms.py
- models.py
- template tags
- JavaScript
- utils.py
- services.py

Classify every important rule:

A. Backend business logic

B. Presentation/UI logic

C. Validation

D. Authorization

E. Calculation

F. Workflow/state transition

Determine what should eventually move into services.py.

DO NOT move code yet.


==================================================
6. ROLE AND PERMISSION MATRIX
==================================================

The system has 8 roles.

Determine actual access for each Working workflow.

For each role determine:

- view
- create
- edit
- delete
- approve
- tracking
- dashboard
- reports

Compare:

Legacy Django behavior

with:

Phase 3A authorization design.

DO NOT invent new permissions.


==================================================
7. WORKING ↔ OTHER MODULES
==================================================

Analyze dependencies with:

- Inventory
- Accounting
- AppUser
- other applications

Create a dependency graph.

Example only:

Working
 ├── Inventory
 ├── Accounting
 └── AppUser

Use actual dependencies.

Identify whether Working APIs should consume other APIs
or directly use shared backend services/models.

Do NOT create cross-module APIs yet.


==================================================
8. API RESOURCE DESIGN
==================================================

Determine which Working concepts should become API resources.

DO NOT expose every model automatically.

For each proposed resource document:

- endpoint
- model
- purpose
- list
- retrieve
- create
- update
- delete
- custom actions
- filtering
- ordering
- pagination
- permissions


==================================================
9. CRUD VS BUSINESS ACTION
==================================================

For every important workflow determine whether it should be:

CRUD

OR

a domain action.

Examples only:

POST /resource/

versus:

POST /resource/<id>/approve/
POST /resource/<id>/complete/
POST /resource/<id>/cancel/

Do not use custom actions unless existing business workflows require
them.

Avoid converting state-machine workflows into unsafe generic PATCH.


==================================================
10. SERIALIZATION DESIGN
==================================================

For every proposed API resource define:

- response fields
- create fields
- update fields
- read-only fields
- calculated fields
- related objects
- IDs vs nested objects

Identify fields that must NEVER be client-controlled.

Do NOT create serializers.


==================================================
11. STATE TRANSITIONS
==================================================

Identify every important status/state field.

For each state machine document:

Current state
     ↓
Allowed transition
     ↓
Next state

For example only:

DRAFT → APPROVED → COMPLETED

Do not assume this example exists.

Determine:

- who can transition
- what validation occurs
- what side effects occur
- whether transition should become a dedicated API action


==================================================
12. DASHBOARDS AND REPORTING
==================================================

Identify all Working:

- dashboards
- summaries
- statistics
- reports
- aggregations

Determine:

- data source
- calculations
- filters
- date ranges
- role restrictions
- performance concerns

Determine which calculations belong in backend services.


==================================================
13. API SECURITY
==================================================

Analyze:

- authentication
- role authorization
- object-level authorization
- IDOR
- mass assignment
- sensitive fields
- user-controlled IDs
- workflow manipulation
- unauthorized state transitions

Pay special attention to production records.

Do not implement security fixes yet.


==================================================
14. QUERY PERFORMANCE
==================================================

Identify likely:

- N+1 queries
- expensive dashboard queries
- aggregation queries
- select_related opportunities
- prefetch_related opportunities
- pagination requirements

Do not perform speculative optimization.


==================================================
15. REACT MIGRATION BOUNDARY
==================================================

For each major Working screen identify:

Current:

Django Template
     ↓
Django View
     ↓
Model/Form

Future:

React
     ↓
REST API
     ↓
Service
     ↓
Model

Identify screens that are:

- easy migration candidates
- medium complexity
- high-risk migration candidates

Recommend the safest first Working screen.


==================================================
16. API CONTRACT
==================================================

Follow:

/api/v1/

and the established conventions in:

docs/api.md

All proposed endpoints must be marked:

PROPOSED — NOT IMPLEMENTED


==================================================
17. TEST PLAN
==================================================

Design future API tests covering:

- authentication
- all relevant roles
- CRUD
- business actions
- validation
- state transitions
- calculations
- relationships
- filtering
- pagination
- IDOR
- sensitive fields
- unauthorized state transitions
- regression against legacy workflows


==================================================
18. DOCUMENTATION
==================================================

Update:

docs/api.md
docs/architecture.md
docs/migration.md

Document:

- Working domain architecture
- proposed API resources
- proposed endpoints
- dependencies
- migration strategy

Clearly mark APIs as:

PROPOSED — NOT IMPLEMENTED


==================================================
19. FINAL REPORT
==================================================

Return:

1. Working architecture
2. Complete model map
3. Relationship diagram
4. Business domain map
5. Existing workflows
6. Business logic map
7. Role/permission matrix
8. Cross-module dependencies
9. Proposed API resources
10. Proposed endpoints
11. CRUD vs business actions
12. State transition model
13. Serialization design
14. Dashboard/reporting architecture
15. Security analysis
16. Query/performance analysis
17. React migration boundaries
18. Recommended first Working API resource
19. Test plan
20. Risks
21. Exact implementation plan for PHASE 3D-2


==================================================
STOP
==================================================

After producing the design report:

STOP.

DO NOT IMPLEMENT ANYTHING.

Wait for explicit approval for:

PHASE 3D-2 — WORKING API IMPLEMENTATION