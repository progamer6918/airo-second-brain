import os
import sys
import unittest
import tempfile
import time

CORE_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if CORE_SRC not in sys.path:
    sys.path.insert(0, CORE_SRC)

from airo_finance_core import DatabaseManager, FinanceCoreEngine

class TestOwnerAuth(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_auth.db")
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()
        self.engine = FinanceCoreEngine(self.db)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_verify_session(self):
        session, raw_token = self.engine.create_owner_session("Test Browser", expires_in_days=30)
        self.assertIsNotNone(session.id)
        self.assertEqual(session.device_name, "Test Browser")
        self.assertIsNotNone(raw_token)
        self.assertNotEqual(session.token_hash, raw_token)

        # Verify using the raw token
        verified = self.engine.verify_owner_session(raw_token)
        self.assertIsNotNone(verified)
        self.assertEqual(verified.id, session.id)

    def test_verify_invalid_token(self):
        self.assertIsNone(self.engine.verify_owner_session("invalid_token_12345"))
        self.assertIsNone(self.engine.verify_owner_session(""))

    def test_revoke_single_session(self):
        session, raw_token = self.engine.create_owner_session("Test Mobile", expires_in_days=7)
        self.assertIsNotNone(self.engine.verify_owner_session(raw_token))

        revoked = self.engine.revoke_owner_session(raw_token)
        self.assertTrue(revoked)

        # Should no longer verify
        self.assertIsNone(self.engine.verify_owner_session(raw_token))

    def test_revoke_all_sessions(self):
        _, token1 = self.engine.create_owner_session("Device 1", expires_in_days=7)
        _, token2 = self.engine.create_owner_session("Device 2", expires_in_days=7)
        _, token3 = self.engine.create_owner_session("Device 3", expires_in_days=7)

        self.assertIsNotNone(self.engine.verify_owner_session(token1))
        self.assertIsNotNone(self.engine.verify_owner_session(token2))
        self.assertIsNotNone(self.engine.verify_owner_session(token3))

        count = self.engine.revoke_all_owner_sessions()
        self.assertGreaterEqual(count, 3)

        self.assertIsNone(self.engine.verify_owner_session(token1))
        self.assertIsNone(self.engine.verify_owner_session(token2))
        self.assertIsNone(self.engine.verify_owner_session(token3))

    def test_session_expiration(self):
        # Create session that expires in -1 days (already expired)
        session, raw_token = self.engine.create_owner_session("Expired Device", expires_in_days=-1)
        self.assertIsNone(self.engine.verify_owner_session(raw_token))

if __name__ == "__main__":
    unittest.main()
