# React Migration Workflow

Use this workflow when migrating a specific Django page to React.

## Analyze -> Plan -> Implement -> Test -> Review

1. **Analyze**: Review the existing Django HTML template and JS logic. Note all context variables.
2. **Plan**: Outline the React Component structure. Map the API endpoint it needs.
3. **Implement**: 
   - Verify the API exists (run API Implementation Workflow if not).
   - Scaffold the React component.
   - Fetch data via API.
   - Replicate the exact CSS styling.
4. **Test**: Run the React page in parallel with the old Django page to compare visual and functional parity.
5. **Review**: Ensure mobile responsiveness and Role-based UI restrictions are maintained in the frontend state.
