# Frontend Documentation

## Current Implementation
- **Templating**: Django Templates (e.g., `list.html`, `dashboard_kcs.html`).
- **Styling**: Vanilla CSS stored in `Working/static/working/css/` (e.g., `premium.css`, `list.css`).
- **Interactivity**: Vanilla JS (`cascade_select.js` for dynamic dropdowns, `excel_filter.js` for table filtering).

## Target Implementation (React)
**Status**: Phase 4B Implemented (Complete Auth Flow & Production-Ready Application Shell).

- **Location**: `frontend/`
- **Build Tool**: Vite (`vite v5.4.11`)
- **Language**: JavaScript (React 18 + JSX)
- **Styling**: Vanilla CSS (`src/index.css`) directly porting design tokens from `Working/static/working/css/premium.css`.
- **API Client**: Centralized `fetch` wrapper in `src/api/client.js` with auto-JWT injection and 401 refresh mechanism.
- **State Management**: React Context (`AuthContext.jsx`) for authentication and session state.
- **Routing**: `react-router-dom` (`AppRoutes.jsx`) with `ProtectedRoute.jsx` guarding authenticated pages.
- **Development Command**: `npm run dev` (runs at `http://localhost:5173`, proxies `/api` to `http://localhost:8000`)
- **Production Build Command**: `npm run build` (outputs to `frontend/dist/`)
- **Coexistence**: Django Templates remain active and untouched. React communicates exclusively through `/api/v1/` REST APIs.
