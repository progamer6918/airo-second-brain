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
    "backend_rpc_absent": "google.script.run" not in text,
    "fetch_absent": "fetch(" not in text,
    "write_method_absent": not re.search(
        r"\b(setValue|setValues|appendRow|insertRow|deleteRow)\b", text
    ),
    "public_safe_fixture": "PUBLIC_SAFE_SAMPLE_DATA" in text,
    "production_replacement_false": "productionReplacement: false" in text,
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
