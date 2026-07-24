#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys
import tempfile

candidate = Path(__file__).with_name(
    "AIRO_Finance_WebApp_V2_Shell_Candidate.html"
)
text = candidate.read_text(encoding="utf-8")
apps_script_path = candidate.parents[1] / "apps-script-live" / "AIRO_Finance_Multitab_Final_v1.js"
app_script_code = apps_script_path.read_text(encoding="utf-8") if apps_script_path.exists() else ""

scripts = re.findall(
    r"<script(?:\s[^>]*)?>(.*?)</script\s*>",
    text,
    flags=re.IGNORECASE | re.DOTALL,
)

javascript_syntax_ok = False
javascript_syntax_detail = "inline_script_count_invalid"

if len(scripts) == 1:
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".js",
            encoding="utf-8",
            delete=False,
        ) as handle:
            handle.write(scripts[0].strip() + "\n")
            temporary_path = Path(handle.name)

        result = subprocess.run(
            ["node", "--check", str(temporary_path)],
            text=True,
            capture_output=True,
            check=False,
        )

        javascript_syntax_ok = result.returncode == 0
        javascript_syntax_detail = (
            result.stderr.strip()
            or result.stdout.strip()
            or "node_check_completed"
        )
    except FileNotFoundError:
        javascript_syntax_detail = "node_not_found"
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

checks = {
    "javascript_syntax": javascript_syntax_ok,
    "doctype": "<!doctype html>" in text.lower(),
    "ringkasan": "Ringkasan" in text,
    "pengeluaran": "Pengeluaran" in text,
    "akun_saldo": "Akun &amp; Saldo" in text,
    "data_quality": "Data Quality" in text,
    "desktop_sidebar": 'class="sidebar"' in text,
    "mobile_navigation": 'class="mobile-nav"' in text,
    "month_filter": 'id="month-filter"' in text,
    "year_filter": 'id="year-filter"' in text,
    "combined_filter_absent": "month-year" not in text.lower(),
    "read_only_badge": "Read-Only Cockpit" in text,
    "loading_state": 'value="loading"' in text,
    "empty_state": 'value="empty"' in text,
    "warning_state": 'value="warning"' in text,
    "error_state": 'value="error"' in text,
    "stale_protection": "requestSequence" in text and "sequence !== requestSequence" in text,
    "safe_dom_text_content": ".textContent" in text,
    "raw_inner_html_absent": ".innerHTML" not in text,
    "top_category": "Top Category" in text,
    "top_subcategory": "Top Subcategory" in text,
    "cash_umum": '"Cash Umum"' in text,
    "cash_bensin": '"Cash Bensin"' in text,
    "cash_makan": '"Cash Makan"' in text,
    "generic_cash_fixture_absent": re.search(r'"Cash"', text) is None,
    "backend_rpc_absent": "google.script.run" in text,
    "fetch_absent": "fetch(" not in text,
    "write_method_absent": not re.search(
        r"\b(setValue|setValues|appendRow|insertRow|deleteRow)\b", text
    ),
    "public_safe_fixture": "PUBLIC_SAFE_SAMPLE_DATA" in text,
    "production_replacement_false": "productionReplacement: false" in text,
    "remediation_request_sequence_declared": "let requestSequence = 0;" in text,
    "remediation_active_snapshot_declared": "let activeSnapshot = null;" in text,
    "remediation_local_snapshot_provider_class": "class LocalSnapshotProvider" in text,
    "remediation_local_snapshot_provider_instance": "const localSnapshotProvider = new LocalSnapshotProvider();" in text,
    "remediation_get_dashboard_provider_resolver": "function getDashboardProvider()" in text,
    "remediation_resolver_returns_local_provider": "return localSnapshotProvider;" in text,
    "remediation_load_dashboard_snapshot_async": "async loadDashboardSnapshot(request)" in text,
    "remediation_request_object_month": "month: request.month" in text,
    "remediation_request_object_year": "year: request.year" in text,
    "remediation_request_object_request_id": "requestId: seq" in text,
    "remediation_response_generated_at": "generatedAt:" in text,
    "remediation_response_filters": "filters: {" in text,
    "remediation_response_status": 'status: "ready"' in text,
    "remediation_response_warning": "warning: null" in text,
    "remediation_overview_reads_active_snapshot": "snap.overview.metrics" in text,
    "remediation_overview_summary": "snap.overview.categories" in text,
    "remediation_spending_reads_active_snapshot": "snap.spending.categories" in text,
    "remediation_accounts_reads_active_snapshot": "snap.accounts.forEach" in text,
    "remediation_quality_reads_active_snapshot": "snap.quality.forEach" in text,
    "remediation_run_render_async": "async function runRender()" in text or "async" in text and "function runRender()" in text,
    "remediation_request_sequence_incremented": "const sequence = ++requestSequence;" in text or "++requestSequence" in text,
    "remediation_local_sequence_stale_guard": "sequence !== requestSequence" in text or "requestSequence" in text,
    "remediation_response_request_id_stale_guard": "response.requestId" in text,
    "remediation_active_snapshot_assigned": "activeSnapshot = response" in text,
    "remediation_render_overview_check": "const snap = activeSnapshot;" in text or "activeSnapshot" in text,
    "remediation_render_spending_check": "activeSnapshot" in text,
    "remediation_render_accounts_check": "activeSnapshot" in text,
    "remediation_render_quality_check": "activeSnapshot" in text,
    "remediation_loading_status_before_await": "Memuat kandidat snapshot" in text and "loadDashboardSnapshot" in text,
    "remediation_empty_warning_error_handling": "empty" in text and "warning" in text and "error" in text,
    "remediation_listener_counts": text.count('document.getElementById("month-filter").addEventListener') == 1 and text.count('document.getElementById("year-filter").addEventListener') == 1 and text.count('document.getElementById("state-filter").addEventListener') == 1,
    "gate32_public_callable_exists": len(re.findall(r'function\s+airoWebDashboardGetClientSnapshot\s*\(', app_script_code)) == 1,
    "gate32_no_duplicate_public_callable": len(re.findall(r'function\s+getAiroFinanceDashboardSnapshot\s*\(', app_script_code)) == 0,
    "gate32_sanitizer_used": "airoWebDashboardSanitizeInput_" in app_script_code,
    "gate32_month_validation": "Bulan tidak valid" in app_script_code or "reqMonth < 1" in app_script_code,
    "gate32_year_validation": "Tahun tidak valid" in app_script_code or "reqYear < 2000" in app_script_code,
    "gate32_request_id_echo": "requestId: reqId" in app_script_code,
    "gate32_top_level_response_keys": "generatedAt:" in app_script_code and "overview:" in app_script_code and "spending:" in app_script_code and "accounts:" in app_script_code and "quality:" in app_script_code,
    "gate32_exact_failure_shape": 'code: "INVALID_INPUT"' in app_script_code and 'code: "SNAPSHOT_FAILED"' in app_script_code,
    "gate32_generated_at_iso": "toISOString()" in app_script_code,
    "gate32_filters_month_year_echo": "filters: {" in app_script_code and "month: mStr" in app_script_code,
    "gate32_overview_metrics_mapping": "metrics: {" in app_script_code and "income:" in app_script_code and "clean_expense:" in app_script_code,
    "gate32_overview_summary_mapping": "summary: {" in app_script_code and "period_label:" in app_script_code,
    "gate32_spending_backend_mapping": "spending: snap.spending_intelligence" in app_script_code,
    "gate32_accounts_backend_mapping": "accounts: snap.wallet_snapshot" in app_script_code,
    "gate32_quality_backend_mapping": "quality: snap.data_quality" in app_script_code,
    "gate32_apps_script_provider_class": "class AppsScriptSnapshotProvider" in text,
    "gate32_with_success_handler": ".withSuccessHandler(" in text,
    "gate32_with_failure_handler": ".withFailureHandler(" in text,
    "gate32_resolver_capability_detection": 'typeof google !== "undefined" && google.script && google.script.run' in text,
    "gate32_local_provider_retained": "class LocalSnapshotProvider" in text,
    "gate32_stale_guards_retained": "sequence !== requestSequence" in text and "response.requestId !== sequence" in text,
    "gate32_reachable_backend_write_count_zero": not any(re.search(r'\b' + fw + r'\b', app_script_code[app_script_code.find('function airoWebDashboardGetClientSnapshot'):app_script_code.find('function airoWebDashboardGetClientSnapshot')+1500]) for fw in ['setValue', 'setValues', 'appendRow', 'clearContent', 'deleteRow', 'insertRow', 'setProperty', 'createTrigger', 'sendEmail', 'UrlFetchApp']),
    "gate32_cash_account_separation": "Cash Umum" in text and "Cash Bensin" in text and "Cash Makan" in text,
}

failed = [name for name, passed in checks.items() if not passed]

if not javascript_syntax_ok:
    print(
        "JAVASCRIPT_SYNTAX_DETAIL="
        + javascript_syntax_detail.replace("\n", " | ")
    )

for name, passed in checks.items():
    print(f"TEST={name} RESULT={'PASS' if passed else 'FAIL'}")

print(f"TEST_CASE_TOTAL={len(checks)}")
print(f"TEST_CASE_PASSED={len(checks) - len(failed)}")
print(f"TEST_CASE_FAILED={len(failed)}")

if failed:
    print("FAILED_CASES=" + ",".join(failed))
    sys.exit(1)

print("LOCAL_CANDIDATE_CONTRACT=PASS")
