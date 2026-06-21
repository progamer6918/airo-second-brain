from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
ACTIVE_APPS_SCRIPT = REPO_ROOT / "scripts" / "personal-workflow" / "apps-script" / "airo_finance_multitab_final_v1.gs"


def read_source() -> str:
    return ACTIVE_APPS_SCRIPT.read_text(encoding="utf-8", errors="replace")


def extract_function(source: str, function_name: str) -> str:
    marker = f"function {function_name}("
    start = source.find(marker)
    if start < 0:
        raise AssertionError(f"Missing function: {function_name}")

    brace_start = source.find("{", start)
    if brace_start < 0:
        raise AssertionError(f"Missing opening brace for function: {function_name}")

    depth = 0
    for index in range(brace_start, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]

    raise AssertionError(f"Could not extract function body: {function_name}")


class ReviewQueueStatusReasonContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_review_queue_processor_exists_and_reads_review_status(self):
        body = extract_function(self.source, "processReviewQueueApproved")

        self.assertIn("AIRO_CONFIG.tabs.review", body)
        self.assertIn("reviewHeaderMap_", body)
        self.assertIn("getReviewValue_", body)
        self.assertIn("setReviewValue_", body)
        self.assertIn("['review_status', 'status']", body)
        self.assertRegex(body, r"toLowerCase\(\)")

    def test_review_queue_only_processes_approved_or_edited_rows(self):
        body = extract_function(self.source, "processReviewQueueApproved")

        self.assertIn("approved", body)
        self.assertIn("edited", body)
        self.assertIn("!['approved', 'edited'].includes(status)", body)
        self.assertIn("skipped++", body)

    def test_review_queue_writes_explicit_issue_reason_outcomes(self):
        body = extract_function(self.source, "processReviewQueueApproved")

        for expected_reason in [
            "approved_but_amount_missing",
            "approved_but_account_missing",
            "processed_to_",
            "process_failed_",
            "process_error_",
        ]:
            self.assertIn(expected_reason, body)

        self.assertIn("issue_reason", body)

    def test_review_queue_header_map_canonicalizes_headers(self):
        body = extract_function(self.source, "reviewHeaderMap_")

        self.assertIn("canonicalKey_", body)
        self.assertIn("headers.forEach", body)
        self.assertIn("map[key] = idx", body)
        self.assertIn("return map", body)

    def test_review_queue_value_helpers_preserve_key_based_access(self):
        getter = extract_function(self.source, "getReviewValue_")
        setter = extract_function(self.source, "setReviewValue_")

        for expected in ["keys", "canonicalKey_", "map"]:
            self.assertIn(expected, getter)
            self.assertIn(expected, setter)

        self.assertIn("Object.prototype.hasOwnProperty.call(map, c)", getter)
        self.assertIn("setValue", setter)


if __name__ == "__main__":
    unittest.main()
