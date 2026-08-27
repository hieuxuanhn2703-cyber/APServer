# Django to React Migration Guidelines

**Status**: Migration Planning Phase. No migrations have been executed.

## Target Architecture

`React Frontend -> HTTP/REST API (JSON) -> Django Backend -> MySQL`

## Migration Rules

- **Parallel Running**: During migration, existing Django views and templates MUST remain functional. Do not delete a Django view or template until the React replacement is fully verified in production.
- **API-First**: Before building a React component for a page, build and verify the DRF API endpoint it will consume.
- **Phased Approach**:
  1. Migrate independent, low-complexity modules first (e.g., `Inventory` app).
  2. Move to medium complexity (e.g., `Accounting` app).
  3. Migrate core data-entry features last (e.g., `Working` app cascade selects).
- **Data Integrity**: Ensure APIs respect the exact same business logic (e.g., `transaction.atomic()`, `on_delete=models.PROTECT`) as the original Django Views.
- **Routing**: API routes should be completely separate from UI routes (e.g., `/api/...` vs UI routes).
