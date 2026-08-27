# Project Overview

This project is a Process Monitoring application for a manufacturing environment. It tracks product quantities across various production stages, including cutting, general production, KCS (Quality Control), and finishing.

## Technology Stack

- **Python version:** 3.12
- **Django version:** 6.0.6
- **Database:** MySQL
- **Frontend technologies:** Django Templates, Vanilla HTML, Vanilla CSS, Vanilla JavaScript (Targeting React migration in the future).
- **API framework:** Not determined from the existing codebase (Standard Django request-response cycle is used). Target: Django REST Framework (NOT IMPLEMENTED YET).
- **Deployment technologies:** ASGI / Twisted / Daphne present in requirements, indicating potential async deployment.

## Project Structure

- `ProcessMonitoring/`: The main Django project configuration directory containing `settings.py`, `urls.py`, and `asgi.py`.
- `Working/`: The primary Django application handling users, products, and core production tracking (Cut, KCS, Finishing).
- `Accounting/`: The financial application handling pricing, exports, and payments.
- `Inventory/`: The warehouse application handling material receipts and issues.
- `.agents/`: Agent instruction system directory.

## General Coding Rules

- Understand existing code before changing it.
- Reuse existing functionality whenever possible.
- Follow existing architecture and naming conventions.
- Avoid unnecessary refactoring.
- Make the smallest reasonable change.
- Do not duplicate existing business logic.
- Do not introduce unnecessary dependencies.
- Do not remove existing functionality without explicit approval.

## Change Philosophy

Agents should prefer:

1. Minimal changes.
2. Existing project patterns.
3. Reusable code.
4. Backward compatibility.
5. Clear and maintainable implementations.
