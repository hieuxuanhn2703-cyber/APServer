# Debugging Workflow

Use this workflow to isolate and fix bugs.

## Analyze -> Plan -> Implement -> Test -> Review

1. **Analyze**: Reproduce the error. Check Django tracebacks. Is it a database `ProtectedError`? Is it an N+1 query timeout? Is it a permission denial?
2. **Plan**: Formulate a hypothesis and a fix.
3. **Implement**: Apply the fix (e.g., adding `transaction.atomic()`, or handling exception).
4. **Test**: Rerun the failure scenario.
5. **Review**: Ensure the fix didn't break related modules (e.g., fixing `Working` didn't break `Accounting`).
