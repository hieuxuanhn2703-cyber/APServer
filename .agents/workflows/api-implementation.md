# API Implementation Workflow

Use this workflow to implement new Django REST Framework (DRF) APIs.

## Analyze -> Plan -> Implement -> Test -> Review

1. **Analyze**: Identify the exact Django View and Model the API should replicate. Note the permissions used.
2. **Plan**: Write out the DRF Serializer fields and ViewSet methods. Ask user for approval.
3. **Implement**: 
   - Create Serializer.
   - Create View/ViewSet with custom permissions checking `AppUser.role`.
   - Update `urls.py`.
4. **Test**: Use `curl` or a test script to ensure the API returns correct JSON and blocks unauthorized roles.
5. **Review**: Check for N+1 queries using `select_related`.
