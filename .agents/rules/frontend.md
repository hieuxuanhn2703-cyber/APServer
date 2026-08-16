# Frontend Instructions

## Frontend Stack

- **HTML:** Django Templates
- **CSS:** Vanilla CSS (primarily using custom files like `premium.css` located in `Working/static/working/css/`)
- **JavaScript:** Vanilla JS (`cascade_select.js`, `numeric_input.js`)
- **Frameworks:** No modern JS frameworks (React, Vue, Angular) or utility-first CSS frameworks (Tailwind, Bootstrap) are detected in the repository.

## Rules

- **HTML/templates:** Follow the existing structure and use Django template tags (`{% load static %}`, `{% csrf_token %}`) appropriately. Ensure `dashboard_tags` are used when applicable.
- **CSS:** Add styles directly to the existing CSS files or create a new plain CSS file. Do not introduce a CSS framework unless explicitly requested.
- **JavaScript:** Keep JavaScript simple and vanilla.
- **Components:** Reuse existing HTML structures and CSS classes for inputs, buttons, and layouts (e.g., `.entry-card`, `.btn-entry-submit`).
- **Responsive design:** Ensure changes maintain current responsive behavior.
- **Forms:** Match existing form layouts, honoring grid styles (e.g., `.entry-grid`).
- **Navigation & Dashboard UI:** Preserve the sidebar structure and topbar components.
- **Tables:** Use existing table markup conventions in templates like `list.html` or `tracking.html`.
- **Loading/Error states:** Handle gracefully within the template logic.

## General UI Principles

- Preserve existing functionality.
- Maintain visual consistency.
- Reuse existing components/styles.
- Do not introduce a new UI framework unless explicitly requested.
- Do not rewrite unrelated pages.
- Keep responsive behavior intact.
- Prefer reusable components over duplicated markup.
- Maintain accessibility where practical.

## UI/UX Guidelines (Learned from Session)

- **Mobile Responsiveness:** Data entry forms on mobile devices (`max-width: 640px`) MUST be single-column to avoid overlapping inputs (especially date inputs and selects). `.entry-grid` classes like `grid-cols-2` and `grid-cols-3` should collapse to `1fr` on mobile. Small numeric inputs can remain 2 columns (`grid-cols-4` -> `repeat(2, 1fr)`).
- **Table Styling:** Data tables must be clear. Use zebra striping (`tbody tr:nth-child(even)`), hover highlights (`tbody tr:hover`), uppercase headers with slightly darker backgrounds, and sticky headers.
- **Form Edits:** When users edit a form (e.g., from the dashboard or a list page), use the `?next={{ request.path }}` parameter to redirect them back to their original context after saving.
- **Role-based UI Restrictions:**
  - `PREMIUM` role must not see the "Quy trình sản xuất" (Production Process) data entry links in the sidebar.
  - `PREMIUM` and `QUAN_LY` roles must not have "Đổi mật khẩu" (Change Password) and "Đăng xuất" (Logout) buttons exposed on edit pages, as they can access any user's edits.
- **Dynamic Javascript Rendering:** The `cascade_select.js` script depends on a JSON configuration object. Ensure the view always injects `config` into the template context and the template renders `{{ config|json_script:"config-data" }}`.
