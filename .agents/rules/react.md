---
trigger: always_on
---

# React Frontend Instructions

**Status**: NOT IMPLEMENTED YET

## Purpose

This file defines the TARGET frontend architecture.

The current frontend remains Django Templates until individual modules are migrated.

## Technology Stack

- Framework: React
- Build tool: Vite or Next.js (To be decided when React is implemented)
- State Management: Context API or Redux (To be decided)
- Styling: Vanilla CSS (migrating existing `.css` files) or CSS Modules
- Tailwind: NOT APPROVED
- Bootstrap: NOT APPROVED

Do not introduce additional frontend frameworks or libraries without explicit approval.

## Architecture

Target architecture:

React
    ↓
REST API
    ↓
Django Backend
    ↓
Database

React must never access the database directly.

Django remains responsible for:

- Business logic
- Database operations
- Authentication
- Authorization
- Permissions
- Backend validation
- Data integrity

React is responsible for:

- UI
- Presentation
- Client-side state
- User interaction
- API communication
- Loading states
- Error states

## Migration Rules

- Do NOT create the React application unless explicitly requested.
- Do NOT migrate all Django templates at once.
- Migrate one functional module/page at a time.
- Preserve existing functionality.
- Do not redesign the UI during migration unless explicitly requested.
- Existing Django frontend code must remain functional until its React replacement has been verified.

## Visual Design

During migration:

- Preserve existing visual design.
- Preserve existing layouts.
- Preserve existing colors.
- Preserve existing interaction patterns.
- Preserve responsive behavior.
- Reuse existing CSS concepts where practical.

Do not introduce a new design system during migration.

## Existing Frontend Components

Important existing CSS/JS concepts include:

- `.entry-card`
- `.btn-entry-submit`
- `.entry-grid`
- `cascade_select.js`
- `numeric_input.js`

These must be analyzed before replacing them.

Do not blindly translate existing JavaScript line-by-line.

Understand the existing behavior first, then implement equivalent React behavior.

## Responsive Design

Preserve existing responsive behavior and visual UI/UX guidelines:

- **Mobile Responsiveness:** Data entry forms on mobile devices (`max-width: 640px`) MUST be single-column to avoid overlapping inputs. Existing project-specific classes like `grid-cols-2` and `grid-cols-3` should collapse to `1fr` on mobile.
- **Table Styling:** Data tables must retain zebra striping, hover highlights, uppercase headers with slightly darker backgrounds, and sticky headers.
- **Role-based UI Restrictions:** React components must enforce the same UI restrictions as the Django frontend (e.g., hiding menus or edit buttons from `PREMIUM` or `QUAN_LY` roles if they shouldn't access them).
- Existing project-specific classes such as `grid-cols-2` and `grid-cols-3` are NOT Tailwind classes unless the project explicitly adopts Tailwind.

## API Integration

Once a page has been migrated to React:

React
    ↓
Approved REST API
    ↓
Django

Rules:

- Do not access the database directly.
- Do not introduce new HTML form submission flows for React pages. All data must be fetched and submitted via REST API (JSON).
- Use the approved API contract.
- Handle loading states.
- Handle error states.
- Handle empty states.
- Respect backend authentication and permissions.
- **Form Edits:** When users edit a form via React, ensure they are redirected back to their original context after saving (replicating the `?next=` behavior).

During the migration period, existing Django form submissions may remain unchanged until their corresponding module is migrated.

## State Management

State-management architecture is NOT DECIDED YET.

Do not introduce:

- Redux
- Context API
- Zustand
- MobX
- or another state-management library

unless explicitly approved.

Prefer local React state for simple component state when React implementation begins.

## Component Architecture

Prefer reusable components.

Separate:

- Presentation/UI components (Dumb components for UI rendering)
- Data-fetching logic (Smart components for API communication)
- API communication
- Shared utilities

Avoid unnecessary abstraction.
Do not create components merely for the sake of abstraction.
Keep components modular. Example: `<Dashboard />`, `<EntryForm />`, `<DataTable />`.
Migrate existing logic (like `cascade_select.js`) into state-driven React Components rather than direct DOM manipulation.

## Definition of Done

A React migration is complete only when:

1. Existing functionality is preserved.
2. API communication works.
3. Authentication works.
4. Permissions work.
5. Loading/error/empty states work.
6. Responsive behavior is preserved.
7. Existing Django functionality has been verified.
8. Legacy frontend code is removed only after successful verification.