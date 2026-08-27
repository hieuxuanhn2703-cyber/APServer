# Django to React Migration Roadmap

## Objective
Migrate the existing Django Template-based frontend to a React SPA powered by Django REST Framework (DRF) APIs, without disrupting existing business operations.

## Current Architecture
Django Templates -> Django Views -> MySQL

## Target Architecture
React Frontend -> DRF JSON API -> Django Models -> MySQL

## Migration Strategy: "Strangler Fig" Pattern
We will migrate page by page, leaving the existing Django views intact until the React equivalent is fully tested and verified.

## Recommended Migration Phases

### Phase 1: Foundation (Zero Risk)
- Install and configure Django REST Framework.
- Decide and implement the Authentication strategy for the API (e.g., JWT).
- Scaffold the React application folder.

### Phase 2: Inventory App (Low Complexity)
- **Why first?** The `Inventory` app (`MaterialReceipt`, `MaterialIssue`) is relatively standalone. It only depends on `AppUser` and does not have the deep nested relationships of `Working`'s Product structure.
- **Action**: Build APIs for Inventory. Build React pages for Inventory. Switch routing.

### Phase 3: Accounting App (Medium Complexity)
- **Why second?** Slightly more complex due to Excel exports and dependencies on `ProductColor`.
- **Action**: Build APIs for Prices, Exports, and Payments. Migrate UI to React.

### Phase 4: Working App (High Complexity)
- **Why third?** Contains the core complex forms (e.g., `cascade_select.js` logic) and the most critical business data.
- **Action**: Build APIs for Products, Colors, Sizes, and all production reports (Cut, KCS, Finishing, Process). Build React dynamic forms.

### Phase 5: Dashboards & Auth
- Migrate login flows, account management, and analytical dashboards.

### Phase 6: Decommissioning
- Remove all Django Templates, legacy CSS/JS, and old Django Views.

## Risks
1. **Authentication Gap**: Integrating the custom `AppUser` role-based logic into DRF Permissions will require careful testing.
2. **N+1 Queries in APIs**: Serializing nested models (e.g., returning a report with the user's name and product's color) can cause database spikes if `select_related` is forgotten in DRF views.
