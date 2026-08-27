---
name: react-frontend-dev
description: Instructions for scaffolding and building React components for this project.
---

# React Frontend Development (Migration Target)

## Overview
This skill outlines how to build React components that match the existing Django UI.

## Guidelines
1. **Status**: React is CURRENTLY NOT IMPLEMENTED.
2. **Styling Consistency**: You must inspect the existing Django `.html` templates and `.css` files (in `Working/static/working/css/`) to copy the exact class names (like `.entry-card`, `.entry-grid`) to your React components. Do NOT redesign the app.
3. **State Management**: Existing JS logic (like `cascade_select.js` which filters colors/sizes based on product) must be rewritten using React state (`useState`, `useEffect`) and API calls.
4. **API Integration**: All form submissions must use `fetch` or `axios` to POST to the new DRF endpoints, rather than standard HTML form submissions.
5. **Component Structure**: Keep components modular. Example: `<Dashboard />`, `<EntryForm />`, `<DataTable />`.
