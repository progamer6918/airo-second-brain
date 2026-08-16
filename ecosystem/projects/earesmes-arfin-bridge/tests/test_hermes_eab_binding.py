# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path
from importlib.machinery import SourceFileLoader
import importlib.util

repo_root = Path("/home/egitaristorandas/AI_WORKSPACES/airo-second-brain")
sys.path.insert(0, str(repo_root / "scripts"))
sys.path.insert(0, str(repo_root / "ecosystem/projects/earesmes-arfin-bridge"))

loader = SourceFileLoader("airo_hermes_worker", str(repo_root / "scripts/airo-hermes-worker"))
spec = importlib.util.spec_from_loader("airo_hermes_worker", loader)
worker_mod = importlib.util.module_from_spec(spec)
loader.exec_module(worker_mod)

class TestHermesEabBinding(unittest.TestCase):
    @patch("src.adapter.eab_live_client.EABLiveSignedClient")
    def test_exact_phrase_triggers_eab_list_pending(self, mock_client_cls):
        mock_instance = MagicMock()
        mock_instance.list_pending.return_value = {
            "status": "ok",
            "pending_items": []
        }
        mock_client_cls.return_value = mock_instance

        res = worker_mod.try_handle_eab_intent("cek transaksi Arfin yang pending", "7113110978")
        self.assertIsNotNone(res)
        self.assertIn("Tidak ada transaksi Arfin", res)

    def test_unrelated_message_returns_none(self):
        res = worker_mod.try_handle_eab_intent("halo Earesmes selamat malam", "7113110978")
        self.assertIsNone(res)

    def test_eab_prerouter_no_unbound_session_id(self):
        """Regression test: ensure try_handle_eab_intent does not raise UnboundLocalError."""
        res = worker_mod.try_handle_eab_intent("cek transaksi Arfin yang pending", "7113110978")
        self.assertIsNotNone(res)


    def test_eab_client_endpoint_is_public_canonical(self):
        """Regression test: ensure eab_live_client APPS_SCRIPT_URL points to public deployment ID."""
        import src.adapter.eab_live_client as client_mod
        self.assertIn("AKfycbxzalMbtiHNHUFaWhZcaEBupMfxfXzqlTwrjhDmovUayZnSv-Z-kRmN6MPjq1ncv7nq0g", client_mod.APPS_SCRIPT_URL)
        self.assertNotIn("AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA", client_mod.APPS_SCRIPT_URL)


if __name__ == "__main__":
    unittest.main()
