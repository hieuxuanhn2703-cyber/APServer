# Django to React Migration Roadmap

## Objective
Migrate the existing Django Template-based frontend to a React SPA powered by Django REST Framework (DRF) APIs, without disrupting existing business operations.

## Current Architecture
Django Templates -> Django Views -> MySQL

## Target Architecture
React Frontend -> DRF JSON API -> Django Models -> MySQL

## Migration Strategy: "Strangler Fig" Pattern
We will migrate page by page, leaving the existing Django views intact until the React equivalent is fully tested and verified.

## Recommended Migration Phases (Strangler Fig Strategy)

### Phase 1: Foundation & Auth (Zero Risk)
- Install and configure Django REST Framework (DRF).
- Implement custom JWT Authentication mapped to `AppUser`.
- Scaffold the React application folder.

### Phase 2: Inventory App (Low Complexity Pilot)
- **Why?** The `Inventory` app (`MaterialReceipt`, `MaterialIssue`) is highly standalone and depends only on `AppUser`. Perfect pilot for React table and form components.
- **Action**: Build APIs (`/api/v1/inventory/`). Build React pages.

### Phase 3: Accounting App (Medium Complexity)
- **Why?** Introduces `ProductPrice` and somewhat complex dashboard aggregations.
- **Action**: Build APIs for Prices, Exports, and Payments. Migrate UI.

### Phase 4: Working App (High Complexity)
- **Why?** Contains the core data entry forms and heavy interdependent dropdowns (`cascade_select.js`).
- **Action**: Build APIs for Products, Colors, Sizes, and all production reports.

### Phase 5: Dashboards
- **Why Last?** Dashboards contain massive data aggregations (`accounting_dashboard_view`, `list_view`) and are highly susceptible to N+1 query performance issues when serialized through DRF. Must be carefully engineered last.

### Phase 6: Decommissioning
- Remove all Django Templates, legacy CSS/JS, and old Django Views.

## Risks
1. **Authentication Gap**: Integrating the custom `AppUser` role-based logic into DRF Permissions will require careful testing.
2. **N+1 Queries in APIs**: Serializing nested models (e.g., returning a report with the user's name and product's color) can cause database spikes if `select_related` is forgotten in DRF views.
