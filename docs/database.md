# Database Documentation

## Engine
- **MySQL** (via `mysqlclient`), using `utf8mb4` charset.

## Schema Overview
The database is highly relational, utilizing ForeignKeys heavily.

### Key Relationships
1. **Cross-App Dependencies**:
   - `Accounting.PaymentReport` -> `Working.ProductColor`
   - `Accounting.ProductPrice` -> `Working.ProductColor`
   - `Accounting.ExportReport` -> `Working.AppUser`
   - `Inventory.MaterialReceipt` -> `Working.AppUser`
   - `Inventory.MaterialIssue` -> `Working.AppUser`
2. **Internal Dependencies**:
   - `Working.ProductSize` -> `Working.ProductColor` -> `Working.Product`
   - All reports (`ProcessReport`, `CutReport`, etc.) belong to a `Working.AppUser` via `nguoi_nhap`.

## Integrity Rules
- The system prevents accidental data loss by using `on_delete=models.PROTECT` on `AppUser` links. Deleting a user who has submitted a report is blocked at the database level.
