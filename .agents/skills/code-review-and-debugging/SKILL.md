---
name: code-review-and-debugging
description: Checklist for reviewing PRs in this project (checking N+1 queries, permission bugs).
---

# Code Review and Debugging Checklist

## For Backend (Django)
1. **N+1 Query Check**: Are there loops over querysets in templates or API serializers without a `.select_related` or `.prefetch_related` in the view?
2. **Transaction Check**: If multiple records are created/updated across `Working`, `Accounting`, or `Inventory`, is `transaction.atomic()` used?
3. **Role Validation**: Does the view check `request.user.role` appropriately before saving data?
4. **Foreign Key Deletions**: Is it possible for a user to delete a record that might throw a `ProtectedError`? Ensure error handling exists.

## For Frontend (Django Templates)
1. **Mobile Responsiveness**: Do `.entry-grid` layouts collapse to 1 column on small screens (`max-width: 640px`)?
2. **Static Files**: Are new JS/CSS files correctly loaded using `{% load static %}`?

## For React/API (When Implemented)
1. **CORS/Auth**: Is the API properly validating the token or session?
2. **Data Consistency**: Does the React UI reflect the exact same table structure as the old Django UI?
