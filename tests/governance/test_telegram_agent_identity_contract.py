from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]


class TelegramAgentIdentityGuardTest(unittest.TestCase):
    def test_validator_passes(self):
        result = subprocess.run(
            [str(ROOT / "scripts/airo-agent-identity-guard")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            result.stdout + result.stderr,
        )
        self.assertIn(
            "AIRO_AGENT_IDENTITY_GUARD=PASS",
            result.stdout,
        )

    def test_distinct_existing_bots(self):
        contract = (
            ROOT / "systems/telegram-agent-identity-contract.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "existing dedicated Earesmes Telegram bot",
            contract,
        )
        self.assertIn(
            "existing dedicated Arfin Telegram bot",
            contract,
        )
        self.assertIn(
            "existing dedicated EarnsAI Telegram bot",
            contract,
        )

    def test_local_absence_not_global_absence(self):
        contract = (
            ROOT / "systems/telegram-agent-identity-contract.md"
        ).read_text(encoding="utf-8")

        self.assertIn("not found in local WSL files", contract)
        self.assertIn("does not exist in the AIRO ecosystem", contract)

    def test_new_chat_guard(self):
        boot = (ROOT / "BOOT.md").read_text(encoding="utf-8")
        self.assertIn(
            "all AI operators and every new chat",
            boot,
        )


    def test_visible_response_receipt_enforced(self):
        contract = (
            ROOT / "systems/telegram-agent-identity-contract.md"
        ).read_text(encoding="utf-8")
        boot = (ROOT / "BOOT.md").read_text(encoding="utf-8")

        self.assertIn(
            "Every substantive Telegram architecture response must emit",
            contract,
        )
        self.assertIn(
            "NEW_BOT_RECOMMENDATION_ALLOWED=NO",
            contract,
        )
        self.assertIn(
            "MUTATION_ALLOWED=ONLY_WITH_SEPARATE_OWNER_APPROVAL",
            contract,
        )
        self.assertIn(
            "must visibly emit the PASS or FAIL",
            boot,
        )

if __name__ == "__main__":
    unittest.main()
