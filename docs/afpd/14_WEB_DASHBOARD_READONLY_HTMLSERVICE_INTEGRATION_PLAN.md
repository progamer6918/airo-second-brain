<!-- AFPD_PROVENANCE
source_path: docs/afpd/14_WEB_DASHBOARD_READONLY_HTMLSERVICE_INTEGRATION_PLAN.md
source_lines: 1-220
source_heading: AIRO Finance Web Dashboard Read-Only HtmlService Integration Plan
migration_status: CANONICAL
conflict_id: none
-->

# AIRO Finance Web Dashboard Read-Only HtmlService Integration Plan

- **Gate**: `AIRO_FINANCE_WEB_DASHBOARD_READONLY_HTMLSERVICE_INTEGRATION_PLAN_NO_DEPLOY`
- **Status**: `CANONICAL_PLAN`
- **Mode**: `READ_ONLY`
- **Version**: `1.0`
- **Created**: `2026-07-21`

---

## A. Integration Strategy & Routing Architecture

### 1. Recommended Web App Route
- **Route**: `?view=dashboard` (or secondary alias `?page=dashboard`).
- **Target Handler**: `airoWebDashboardRenderPage_(e)` invoked conditionally within `doGet(e)`.

### 2. Guarding Existing Routes
- **Default `doGet(e)` Behavior**: MUST remain 100% unchanged when no `view=dashboard` parameter is passed. Returns `{"ok": false, "message": "Forbidden or unknown GET request"}`.
- **Existing Probe Route (`airo_probe=task9_access_gate`)**: MUST remain 100% unchanged, returning existing JSON probe status.
- **`doPost(e)` Pipeline**: MUST remain 100% untouched. All Telegram inbound webhooks, admin commands, and confirmation dispatches operate independently without interference.
- **Telegram / Email Engine**: Zero side effects or mutations.

---

## B. Apps Script HtmlService Function & File Structure

### 1. Structure
- **HtmlService File**: `AIRO_Finance_WebDashboard.html` (embedded inline or loaded via `HtmlService.createHtmlOutput`).
- **Server Handler**: `airoWebDashboardRenderPage_(e)`
  - Validates route parameter `e.parameter.view === 'dashboard'`.
  - Serves `HtmlService.createHtmlOutput(htmlContent)` with title `AIRO Finance — Web Dashboard` and viewport meta tag.
- **Public Client RPC Bridge**: `airoWebDashboardGetClientSnapshot(year, month)`
  - Public wrapper function called by client JS via `google.script.run`.
  - Sanitizes year (2000–2100) and month (1–12).
  - Invokes canonical internal calculator `airoWebDashboardGetSnapshot_({ year, month })`.
  - Returns serialized JSON object to client.

---

## C. Read-Only Safety & Static Guard
The future HtmlService integration MUST NOT invoke any spreadsheet mutation functions:
- `setValue`
- `setValues`
- `clear`
- `merge`
- `breakApart`
- `appendRow`
- `delete`
- `copyTo`

Zero write operations allowed inside dashboard renderers, client RPC wrappers, or helper modules.

---

## D. Security & Privacy Plan

### 1. Access Mode
- **Recommended Access**: `PRIVATE_OWNER_ONLY` ("Execute as me", "Only myself").
- **Public Access**: FORBIDDEN. Financial transaction details, category breakdowns, and account names MUST NOT be publicly readable without authentication.
- **URL Secret Tokens**: Forbidden as a sole security mechanism for public access.

---

## E. Performance & Optimization Plan
- **Single Snapshot RPC**: Client fetches complete dataset per period filter change using one `google.script.run` call to `airoWebDashboardGetClientSnapshot`.
- **Zero Per-Card Roundtrips**: Avoid multiple RPC calls per widget card.
- **Recent Activity Limit**: Capped at 10 recent rows.
- **Spending Intelligence Limit**: Basic top categories + subcategories only.

---

## F. Implementation Acceptance Criteria (For Code Gate)
The upcoming local code integration gate (`AIRO_FINANCE_WEB_DASHBOARD_READONLY_HTMLSERVICE_LOCAL_INTEGRATION_NO_DEPLOY`) may pass ONLY if:
1. Source code syntax check passes (`node --check`).
2. Harness syntax check passes.
3. Existing selftest suite remains 80/80 PASS.
4. `doPost(e)` remains unchanged.
5. Default `doGet(e)` and `task9_access_gate` probe remain unchanged.
6. Dashboard route (`?view=dashboard`) renders clean HtmlOutput locally.
7. Zero workbook write methods in dashboard modules.
8. Zero clasp push / deployment performed.

---

## G. Risk Assessment Matrix
- **Route Risk**: `LOW` (gated strictly behind `?view=dashboard`).
- **Privacy Risk**: `LOW` (governed by `PRIVATE_OWNER_ONLY` access policy).
- **Data Correctness Risk**: `LOW` (backed by validated Data Contract & 80/80 selftests).
- **Performance Risk**: `LOW` (single RPC per filter update).
- **Regression Risk to v385**: `LOW` (`doPost` and default `doGet` untouched).
- **Scope Creep Risk**: `LOW` (strictly read-only MVP).

---

## H. Recommendation & Next Gate
- **Recommendation**: **GO** to next gate.
- **Next Safe Gate**: `AIRO_FINANCE_WEB_DASHBOARD_READONLY_HTMLSERVICE_LOCAL_INTEGRATION_NO_DEPLOY`
