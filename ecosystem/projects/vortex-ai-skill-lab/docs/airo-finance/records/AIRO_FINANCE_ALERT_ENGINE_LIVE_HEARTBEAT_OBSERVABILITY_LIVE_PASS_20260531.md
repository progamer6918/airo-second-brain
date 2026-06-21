# Live Pass: Phase 5B-2a Live Heartbeat Observability

## 1. Metadata
* **Verification Date**: 2026-05-31
* **Implementation Commit**: `a9b5553 fix(airo-finance): separate live alert heartbeat readback`
* **Apps Script Deployment Version**: `@95`
* **Apps Script Deployment ID**: `AKfycbx4HWJNY9YOPIssAF9tn3Gx36hFkumyH0TfsuWInPr0e8aZTyrbIs4-kn_Fd-Kox_ie`

---

## 2. Implementation Overview
Phase 5B-2a resolves the observability debt noted at Phase 5B-2 closeout. Previously, `admin alerts live status` returned a single generic `Last Heartbeat` field, which could conflate safe heartbeat with live heartbeat and prevent honest verification of live trigger execution state. This patch separates both:
*   **Distinct Live Heartbeat Actions**: `airoSprint6BTriggerHandlerLive_()` now writes two distinct audit actions:
    *   `sprint6b_trigger_live_disabled_heartbeat` — when `AIRO_ALERT_ENGINE_LIVE_ENABLED` is false (fail-closed mode, proactive sends blocked)
    *   `sprint6b_trigger_live_enabled_heartbeat` — when the switch is enabled and the runner is allowed to send
*   **Separate Readback in `airoSprint6BGetLiveStatus_`**: The status function now independently scans the last 100 audit rows for the most recent safe heartbeat and the most recent live heartbeat, without conflation.
*   **Admin Reply Split**: `admin alerts live status` now shows both `Last Safe Heartbeat` and `Last Live Heartbeat` as separate fields.
*   **Backward Compatibility**: Safe trigger handler remains unchanged; all prior safe trigger tests still pass.

---

## 3. Test & Verification Results

### Automated Tests (PASS)
*   **Alert Engine Tests**: `145 passed / 0 failed` (13 new observability contract tests added)
*   **Nearby Regression Tests**: `24 passed / 0 failed`

### Telegram Smoke Verification (PASS)
`admin alerts live status` after deploy to `@95`:
*   `LIVE Enabled: FALSE`
*   `Live Handler: airoSprint6BTriggerHandlerLive_`
*   `Live Trigger Count: 1`
*   `Safe Trigger Count: 1`
*   `Last Safe Heartbeat: Action sprint6b_trigger_safe_heartbeat, Evaluated 4, Would Send 4, Sent 0`
*   `Last Live Heartbeat: no_recent_live_heartbeat_found`
*   Warning: `⚠️ WARNING: Live trigger is installed, but alert engine is soft-disabled (LIVE enabled is false).`

**Interpretation**: `no_recent_live_heartbeat_found` is an honest, correct readback. The system confirms it has no live heartbeat log yet because the live trigger has not fired a scheduled execution since install. This proves the safe and live readback paths are now fully separated and non-conflating. The value will update to the actual live disabled heartbeat on the next 6-hourly trigger execution.

---

## 4. Safety Guardrails & Principles
*   **Fail-Closed Switch Maintained**: `AIRO_ALERT_ENGINE_LIVE_ENABLED` remains `false`. Proactive sends blocked.
*   **No Uncontrolled Proactive Sends**: Disabled live heartbeat path writes `sent_count: 0` and `proactive_send_performed: false`.
*   **No New Trigger Installed/Uninstalled**: Trigger count remains at `Live: 1, Safe: 1`.
*   **No Gmail Trigger / Email Write**: Gmail polling triggers are disabled. Email finance write is off.
*   **No Gmail/Email State Mutation**: No Gmail messages read, labeled, or modified.
*   **No Sheet Deletion/Unhide**: Sheet structure unchanged from Phase 4B baseline.

---

## 5. Known Next Steps
*   **Phase 5B-3 Controlled Live Enable Trial**: A strict OFF→ON→OFF live enable window test:
    *   Enable live switch via `admin alerts live enable`.
    *   Observe live alert sends within the window.
    *   Verify cooldown and duplicate suppression under live conditions.
    *   Confirm kill-switch (`admin alerts live disable`) stops proactive sends immediately.
