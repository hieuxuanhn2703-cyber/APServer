# Project Overview

This project is a Process Monitoring application for a manufacturing environment. It tracks product quantities across various production stages, including cutting, general production, KCS (Quality Control), and finishing.

## Technology Stack

- **Python version:** 3.12
- **Django version:** 6.0.6
- **Database:** MySQL
- **Frontend technologies:** Django Templates, Vanilla HTML, Vanilla CSS, Vanilla JavaScript
- **API framework:** Not determined from the existing codebase (Standard Django request-response cycle is used).
- **Deployment technologies:** ASGI / Twisted / Daphne present in requirements, indicating potential async deployment.

## Project Structure

- `ProcessMonitoring/`: The main Django project configuration directory containing `settings.py`, `urls.py`, and `asgi.py`.
- `Working/`: The primary Django application containing the business logic.
  - `models.py`: Defines the database schema.
  - `views.py`: Contains the logic for processing requests and rendering templates.
  - `forms.py`: Django forms for data entry.
  - `urls.py`: App-level routing.
  - `templates/`: Contains all HTML templates.
  - `static/`: Contains all static assets (CSS, JS, images).
  - `templatetags/`: Custom template tags for UI logic.
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
