---
name: django-to-react-migration
description: Specific steps to take an existing Django Template view and convert it to a DRF API endpoint + React View.
---

# Django to React Migration Execution

## Overview
This skill acts as a checklist for executing a page-by-page migration from Django Templates to React.

## Migration Steps
1. **Analyze the Current Page**:
   - Identify the Django View (e.g., `inventory_summary_view`).
   - Identify the Context variables passed to the Template.
   - Identify the HTML form structure and existing CSS/JS.
2. **Build the API**:
   - Create a DRF Serializer for the relevant models.
   - Create a DRF View/ViewSet returning the exact data the template used.
   - Configure DRF URLs.
3. **Build the React Component**:
   - Scaffold a new React component matching the HTML layout.
   - Implement data fetching from the new API.
   - Map existing CSS classes to the component.
4. **Test in Parallel**:
   - Verify the React component works by running it alongside the existing Django view. Do NOT delete the Django view yet.
5. **Switch and Cleanup**:
   - Only after approval, point the URL router to the React app and remove the old Django View/Template.
