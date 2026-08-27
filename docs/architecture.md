# System Architecture

## Current Architecture
The ProcessMonitoring project is a monolithic web application built on **Django 6.0.6**. 
It utilizes the Model-Template-View (MTV) pattern.

### Components
1. **Database**: MySQL.
2. **Backend**: Python/Django.
3. **Frontend**: Server-Side Rendered (SSR) HTML via Django Templates, styled with custom CSS and vanilla JavaScript.
4. **Apps**:
   - `ProcessMonitoring`: Core settings and routing.
   - `Working`: Core module for user management, product configuration, and production stages (Cut, KCS, Finishing).
   - `Accounting`: Financial module (Prices, Exports, Payments).
   - `Inventory`: Warehouse module (Receipts, Issues).

## Target Architecture (React Migration)
**Status**: NOT IMPLEMENTED YET.

In the future, the architecture will migrate to a decoupled SPA (Single Page Application):
1. **Database**: MySQL (Unchanged).
2. **Backend API**: Django + Django REST Framework providing JSON endpoints.
3. **Frontend**: React application communicating with the backend via REST API.
