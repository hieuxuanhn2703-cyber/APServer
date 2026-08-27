---
name: django-rest-api-dev
description: Instructions for setting up DRF serializers and views that respect the custom AppUser model.
---

# Django REST API Development (Migration Target)

## Overview
This project is planning to migrate from Django Templates to React. As part of this, Django REST Framework (DRF) APIs must be built.

## Guidelines
1. **Status**: APIs are CURRENTLY NOT IMPLEMENTED. Do not build them unless executing the React Migration phase.
2. **Serializers**: 
   - Ensure foreign keys (e.g., `AppUser`, `ProductColor`) are serialized logically. You may need to use nested serializers for GET requests (to show user names) and PrimaryKeyRelatedFields for POST/PUT requests.
3. **Views**: 
   - Prefer `ModelViewSet` or `APIView`.
   - APIs must live under specific URL prefixes, such as `/api/v1/...`.
4. **Permissions**: 
   - You MUST map the existing `LoginRequiredMiddleware` and role-based checks (from `AppUser.role`) into DRF Custom Permission classes (e.g., `IsKCSRole`, `IsPremiumRole`).
5. **Pagination**: Always paginate list views.
