import unittest
import os
import sys
import json
import time
import subprocess
import hashlib
import re

bridge_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if bridge_root not in sys.path:
    sys.path.insert(0, bridge_root)

repo_root = os.path.abspath(os.path.join(bridge_root, "../../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.adapter.eab_live_client import EABLiveSignedClient

class TestEABV3CorrectedProductionSourceSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.as_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../vortex-ai-skill-lab/apps-script-live/AIRO_Finance_Multitab_Final_v1.js"))
        cls.worker_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../vortex-ai-skill-lab/workers/airo-finance-telegram-proxy/src/index.js"))
        
        with open(cls.as_file, "r", encoding="utf-8") as f:
            cls.as_text = f.read()
        with open(cls.worker_file, "r", encoding="utf-8") as f:
            cls.worker_text = f.read()

    def test_001_actual_worker_has_all_four_operations(self):
        self.assertIn("EAB_GET_PENDING", self.worker_text)
        self.assertIn("EAB_LIST_PENDING", self.worker_text)
        self.assertIn("EAB_SUBMIT_BATCH_CLARIFICATION", self.worker_text)
        self.assertIn("EAB_CREATE_MANUAL_TRANSACTION", self.worker_text)

    def test_002_actual_apps_script_has_all_four_operations(self):
        self.assertIn("EAB_GET_PENDING", self.as_text)
        self.assertIn("EAB_LIST_PENDING", self.as_text)
        self.assertIn("EAB_SUBMIT_BATCH_CLARIFICATION", self.as_text)
        self.assertIn("EAB_CREATE_MANUAL_TRANSACTION", self.as_text)

    def test_003_actual_apps_script_node_harness_execution(self):
        harness_js = f"""
        const fs = require('fs');
        const content = fs.readFileSync('{self.as_file}', 'utf-8');
        global.Utilities = {{
          computeHmacSha256Signature: function(text, secret) {{
            const crypto = require('crypto');
            return crypto.createHmac('sha256', secret).update(text).digest();
          }},
          computeDigest: function(alg, text) {{
            const crypto = require('crypto');
            return crypto.createHash('sha256').update(text).digest();
          }},
          DigestAlgorithm: {{ SHA_256: 'SHA_256' }},
          Charset: {{ UTF_8: 'UTF_8' }}
        }};
        global.ContentService = {{
          MimeType: {{ JSON: 'application/json' }},
          createTextOutput: function(text) {{
            return {{
              setMimeType: function(m) {{ return {{ content: text, mime: m }}; }}
            }};
          }}
        }};
        global.LockService = {{
          getScriptLock: function() {{
            return {{ tryLock: function(ms) {{ return true; }}, releaseLock: function() {{}} }};
          }}
        }};
        let store = new Map();
        store.set('EAB_INTERNAL_AUTH_TOKEN', 'eab_internal_secret_default');
        store.set('EAB_OWNER_CHAT_ID_ALLOWLIST', '7113110978');
        global.PropertiesService = {{
          getScriptProperties: function() {{
            return {{
              getProperty: function(k) {{ return store.get(k) || null; }},
              setProperty: function(k, v) {{ store.set(String(k), String(v)); }},
              getProperties: function() {{ return Object.fromEntries(store.entries()); }}
            }};
          }}
        }};
        eval(content);

        const crypto = require('crypto');
        const ts = Math.floor(Date.now() / 1000);
        const reqId = 'req_123';
        const keyId = 'key_1';
        const nonce = '0123456789abcdef';
        const bodySha256 = crypto.createHash('sha256').update('{{}}').digest('hex');

        const canonical = 'v=1.0&op=EAB_LIST_PENDING&req_id=' + reqId + '&owner_chat_id=7113110978&key_id=' + keyId + '&nonce=' + nonce + '&ts=' + ts + '&body_sha256=' + bodySha256;
        const mac = crypto.createHmac('sha256', 'eab_internal_secret_default').update(canonical).digest('hex');

        const req = {{
          postData: {{
            contents: JSON.stringify({{
              _eab_internal: {{
                marker: 'AIRO_EAB_INTERNAL_V1',
                schema_version: '1.0',
                operation_id: 'EAB_LIST_PENDING',
                request_id: reqId,
                owner_chat_id: '7113110978',
                key_id: keyId,
                nonce: nonce,
                issued_at: ts,
                body_sha256: bodySha256,
                mac: mac
              }}
            }})
          }}
        }};
        const res = airoEabMaybeHandleInternalRequest_(req);
        if (!res || !res.content) throw new Error('Harness failed: ' + JSON.stringify(res));
        """
        r = subprocess.run(["node", "-e", harness_js], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, msg=f"Node harness error: {r.stderr}")

    def test_004_zero_direct_ledger_write_in_eab_block(self):
        m = re.search(r"/\* EAB_M12_READ_ONLY_RECEIVER_START \*/.*?/\* EAB_M12_READ_ONLY_RECEIVER_END \*/", self.as_text, re.DOTALL)
        self.assertIsNotNone(m)
        eab_code = m.group(0)
        self.assertNotIn("writeInternalTransferToAccountLedger_(", eab_code)

    def test_005_live_signed_client_interface(self):
        client = EABLiveSignedClient(service_secret="test_secret_12345678901234567890123456789012")
        self.assertIsNotNone(client)

    def test_006_hermes_script_no_fake_short_ref(self):
        hermes_p = os.path.join(os.path.dirname(__file__), "../../../../scripts/airo-hermes-worker")
        with open(hermes_p, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn("AF-FAKE", content)

    def test_007_node_syntax_check_worker(self):
        r = subprocess.run(["node", "--check", self.worker_file], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, msg=r.stderr)
