from pathlib import Path
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


class AsetSavingsGoldContractTest(unittest.TestCase):
    def setUp(self):
        self.source = read_source()

    def test_aset_top_level_routes_gold_savings_and_review_fallbacks(self):
        body = extract_function(self.source, "writeAssetSafely_")

        for expected in [
            "AIRO_CONFIG.tabs.aset",
            "AIRO_CONFIG.tabs.review",
            "appendGoldAssetRow_",
            "appendToAssetSection_",
            "mirrorAssetPurchaseToAccountLedger_",
            "parsed.assetSection === 'gold'",
            "parsed.assetSection === 'savings'",
            "asset_tab_missing",
            "asset_section_unclear_or_header_not_found",
            "asset_write_error",
        ]:
            self.assertIn(expected, body)

    def test_asset_purchase_mirror_preserves_account_ledger_contract(self):
        body = extract_function(self.source, "mirrorAssetPurchaseToAccountLedger_")

        for expected in [
            "writeAccountLedgerMirror_",
            "type: 'asset_purchase'",
            "category: parsed.category || 'Aset'",
            "linked_txn_id: common.linked_txn_id || makeTxnId_({}, rawText)",
            "account_ledger_result",
            "AIRO_CONFIG.tabs.aset",
            "Object.assign",
        ]:
            self.assertIn(expected, body)

    def test_savings_asset_writer_preserves_linked_id_section_and_amount(self):
        body = extract_function(self.source, "appendToAssetSection_")

        for expected in [
            "section === 'gold'",
            "asset_section_header_not_found",
            "savingsEventType_(data)",
            "amount: data.amount",
            "linked_txn_id: data.linked_txn_id",
            "asset_section: section",
            "findNextSectionRow_",
            "setValues",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("writeAccountLedgerMirror_", body)

    def test_gold_asset_writer_preserves_gold_event_id_linked_id_and_gram_fields(self):
        body = extract_function(self.source, "appendGoldAssetRow_")

        for expected in [
            "gold_event_id",
            "common.linked_txn_id || makeTxnId_({}, rawText)",
            "goldWeightGram",
            "goldKarat",
            "goldPurchasePrice",
            "gramsIn",
            "gramsOut",
            "pricePerGram",
            "totalAmount",
            "gold_weight_missing",
            "gold_ledger_header_not_found",
        ]:
            self.assertIn(expected, body)

        self.assertNotIn("writeAccountLedgerMirror_", body)

    def test_gold_parser_extracts_action_weight_karat_price_and_dates(self):
        body = extract_function(self.source, "parseGoldAsset_")

        for expected in [
            "isGoldAsset",
            "parseGoldAction_",
            "weightGram",
            "karat",
            "pureGram",
            "purchasePrice",
            "purchaseDate",
            "marketPrice24k",
            "estimatedValue",
        ]:
            self.assertIn(expected, body)

    def test_asset_section_parser_distinguishes_gold_and_savings(self):
        body = extract_function(self.source, "parseAssetSection_")

        for expected in [
            "emas",
            "gold",
            "nabung",
            "tabung",
            "saving",
            "savings",
        ]:
            self.assertIn(expected, body)

    def test_review_queue_asset_reprocess_preserves_asset_section_inference(self):
        body = extract_function(self.source, "processReviewQueueApproved")

        for expected in [
            "assetSection: parseAssetSection_(rawText || '')",
            "routeReviewApprovedTab_(parsed, rawText)",
            "writeRouted_(ss, plannedTab, parsed, rawText, stagingResult)",
            "issue_reason",
        ]:
            self.assertIn(expected, body)

    def test_review_queue_approved_tab_router_preserves_aset_routing(self):
        body = extract_function(self.source, "routeReviewApprovedTab_")

        for expected in [
            "AIRO_CONFIG.tabs.aset",
            "nabung",
            "tabung",
            "saving",
            "savings",
            "emas",
            "gold",
            "parsed.category === 'Aset'",
        ]:
            self.assertIn(expected, body)


if __name__ == "__main__":
    unittest.main()
