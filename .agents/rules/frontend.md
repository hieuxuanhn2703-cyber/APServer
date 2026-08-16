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
