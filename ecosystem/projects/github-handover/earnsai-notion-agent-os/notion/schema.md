# EarnsAI Notion Workspace Schema Blueprint

Mode: **SCHEMA_BLUEPRINT_ONLY**

Boundary:

- Dedicated EarnsAI Notion account/workspace only
- No personal Notion workspace
- No external user/workspace access
- No destructive actions
- No real API call until guarded adapter is approved

## Databases

1. EarnsAI Command Center
2. Research Journal
3. Strategy Registry
4. Backtest Logs
5. Decision Journal
6. Risk Flags
7. Agent Activity Log

## Permission Model

Allowed:

- Create page
- Append block
- Update status
- Create database item
- Append research log

Blocked:

- Delete page
- Bulk delete
- Share externally
- Invite users
- Change workspace settings
- Read personal workspace
- Live trading
- Private exchange API

## Integration Order

1. Dry-run payload review
2. Guarded official Notion API adapter
3. Allowlist root page/database IDs
4. Audit every write
5. Human approval for destructive/bulk actions
