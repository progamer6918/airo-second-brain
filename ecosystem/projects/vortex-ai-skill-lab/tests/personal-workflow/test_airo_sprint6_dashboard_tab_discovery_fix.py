from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"
V2_SRC = ROOT / "apps-script-prod-v2" / "AIRO_Finance_Multitab_Final_v1.js"
DOC = ROOT / "docs" / "AIRO_FINANCE_SPRINT_6_DASHBOARD_TAB_DISCOVERY_FIX.md"
CURRENT = ROOT / "docs" / "AIRO_FINANCE_CURRENT_STATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def function_body(text: str, name: str) -> str:
    start = text.index(f"function {name}")
    brace = text.index("{", start)
    depth = 0
    for i in range(brace, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise AssertionError(f"function body not found: {name}")


class TestSprint6DashboardTabDiscoveryFix:
    def test_doc_exists(self):
        assert DOC.exists()

    def test_source_has_discovery_marker(self):
        text = read(SRC)
        assert "AIRO_SPRINT6_DASHBOARD_TAB_DISCOVERY_FIX_V1" in text
        assert "airoSprint6NormalizeTabName_" in text
        assert "airoSprint6FindSheetLoose_" in text

    def test_normalizer_strips_non_alphanumeric(self):
        body = function_body(read(SRC), "airoSprint6NormalizeTabName_")
        assert "toLowerCase()" in body
        assert "replace(/[^a-z0-9]+/g, '')" in body

    def test_get_sheet_stats_returns_actual_match_metadata(self):
        body = function_body(read(SRC), "airoSprint6GetSheetStats_")
        assert "requested_name" in body
        assert "actual_name" in body
        assert "match_type" in body
        assert "normalized_exact" in read(SRC)
        assert "normalized_partial" in read(SRC)

    def test_fix_is_not_dashboard_writer(self):
        text = read(SRC)
        stats_body = function_body(text, "airoSprint6GetSheetStats_")
        find_body = function_body(text, "airoSprint6FindSheetLoose_")
        normalize_body = function_body(text, "airoSprint6NormalizeTabName_")
        combined = stats_body + find_body + normalize_body
        forbidden = [
            ".clear(",
            ".clearContent(",
            ".deleteRow(",
            ".deleteRows(",
            ".deleteSheet(",
            ".appendRow(",
            ".setValue(",
            ".setValues(",
            ".insertSheet(",
        ]
        for item in forbidden:
            assert item not in combined

    def test_v2_source_is_patched_when_present(self):
        if not V2_SRC.exists():
            return
        text = read(V2_SRC)
        assert "AIRO_SPRINT6_DASHBOARD_TAB_DISCOVERY_FIX_V1" in text
        assert "airoSprint6FindSheetLoose_" in text

    def test_current_state_records_fix(self):
        text = read(CURRENT)
        assert "Sprint 6 Dashboard tab discovery fix" in text
        assert "Do not build Dashboard yet" in text
        assert "Run `admin dashboard sprint6 plan` again" in text
