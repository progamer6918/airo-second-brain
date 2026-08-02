import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

WORKER = ROOT / (
    "ecosystem/projects/vortex-ai-skill-lab/"
    "workers/airo-finance-telegram-proxy/src/index.js"
)

ACTIVE_JS = ROOT / (
    "ecosystem/projects/vortex-ai-skill-lab/"
    "apps-script-live/AIRO_Finance_Multitab_Final_v1.js"
)

MIRROR_GS = ROOT / (
    "ecosystem/projects/vortex-ai-skill-lab/"
    "scripts/personal-workflow/apps-script/"
    "airo_finance_multitab_final_v1.gs"
)


class TestEabRealRuntimeReceiver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="eab_runtime_receiver_"))

        cls.worker_mjs = cls.tmp / "worker.mjs"
        cls.worker_mjs.write_text(
            WORKER.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

        cls.worker_runner = cls.tmp / "worker_runner.mjs"
        worker_uri = cls.worker_mjs.as_uri()

        cls.worker_runner.write_text(
            textwrap.dedent(
                f"""
                import workerModule from {json.dumps(worker_uri)};
                import {{ createHash, createHmac }} from "node:crypto";

                const scenario = process.argv[2];

                const env = {{
                  APPS_SCRIPT_URL: "https://apps.example.test/exec",
                  EAB_SERVICE_AUTH_KEY_ID: "key_current",
                  EAB_SERVICE_SECRET: "test_service_secret",
                  EAB_INTERNAL_AUTH_TOKEN: "test_internal_secret",
                  EAB_OWNER_CHAT_ID_ALLOWLIST: "111"
                }};

                const calls = [];
                const waiters = [];

                globalThis.fetch = async (url, opts = {{}}) => {{
                  calls.push({{
                    url: String(url),
                    body: String(opts.body || ""),
                    headers: opts.headers || {{}}
                  }});

                  return new Response(
                    JSON.stringify({{
                      schema_version: "1.0",
                      application_status: "SUCCESS",
                      payload: {{ items: [] }}
                    }}),
                    {{
                      status: 200,
                      headers: {{ "content-type": "application/json" }}
                    }}
                  );
                }};

                function sign(bodyObj, rawBody, ts, nonce) {{
                  const bodySha = createHash("sha256")
                    .update(rawBody)
                    .digest("hex");

                  const canonical =
                    "v=1.0" +
                    "&op=" + bodyObj.operation_id +
                    "&req_id=" + bodyObj.request_id +
                    "&ts=" + ts +
                    "&nonce=" + nonce +
                    "&body_sha256=" + bodySha;

                  return createHmac("sha256", env.EAB_SERVICE_SECRET)
                    .update(canonical)
                    .digest("hex");
                }}

                async function eabRequest({{
                  bodyObj,
                  badSignature = false,
                  omitHeaders = false
                }}) {{
                  const rawBody = JSON.stringify(bodyObj);
                  const ts = Math.floor(Date.now() / 1000);
                  const nonce = "0123456789abcdef";

                  const headers = {{
                    "content-type": "application/json"
                  }};

                  if (!omitHeaders) {{
                    headers["X-EAB-Key-ID"] = "key_current";
                    headers["X-EAB-Timestamp"] = String(ts);
                    headers["X-EAB-Nonce"] = nonce;
                    headers["X-EAB-Signature"] =
                      badSignature
                        ? "00".repeat(32)
                        : sign(bodyObj, rawBody, ts, nonce);
                  }}

                  return workerModule.fetch(
                    new Request("https://worker.example.test/eab", {{
                      method: "POST",
                      headers,
                      body: rawBody
                    }}),
                    env,
                    {{
                      waitUntil(p) {{
                        waiters.push(p);
                      }}
                    }}
                  );
                }}

                let out = {{}};

                if (scenario === "normal_telegram") {{
                  const raw = JSON.stringify({{
                    update_id: 7,
                    message: {{ text: "halo" }}
                  }});

                  const res = await workerModule.fetch(
                    new Request("https://worker.example.test/", {{
                      method: "POST",
                      headers: {{ "content-type": "application/json" }},
                      body: raw
                    }}),
                    {{ APPS_SCRIPT_URL: env.APPS_SCRIPT_URL }},
                    {{
                      waitUntil(p) {{
                        waiters.push(p);
                      }}
                    }}
                  );

                  await Promise.all(waiters);
                  out = {{
                    status: res.status,
                    response: JSON.parse(await res.text()),
                    calls,
                    originalBody: raw
                  }};
                }}

                if (scenario === "missing_auth") {{
                  const res = await eabRequest({{
                    bodyObj: {{
                      schema_version: "1.0",
                      request_id: "req_1",
                      operation_id: "EAB_LIST_PENDING",
                      owner_chat_id: 111
                    }},
                    omitHeaders: true
                  }});

                  out = {{
                    status: res.status,
                    response: JSON.parse(await res.text()),
                    calls
                  }};
                }}

                if (scenario === "bad_signature") {{
                  const res = await eabRequest({{
                    bodyObj: {{
                      schema_version: "1.0",
                      request_id: "req_2",
                      operation_id: "EAB_LIST_PENDING",
                      owner_chat_id: 111
                    }},
                    badSignature: true
                  }});

                  out = {{
                    status: res.status,
                    response: JSON.parse(await res.text()),
                    calls
                  }};
                }}

                if (scenario === "bad_owner") {{
                  const res = await eabRequest({{
                    bodyObj: {{
                      schema_version: "1.0",
                      request_id: "req_3",
                      operation_id: "EAB_LIST_PENDING",
                      owner_chat_id: 222
                    }}
                  }});

                  out = {{
                    status: res.status,
                    response: JSON.parse(await res.text()),
                    calls
                  }};
                }}

                if (scenario === "unknown_operation") {{
                  const res = await eabRequest({{
                    bodyObj: {{
                      schema_version: "1.0",
                      request_id: "req_4",
                      operation_id: "EAB_CREATE_MANUAL_TRANSACTION",
                      owner_chat_id: 111
                    }}
                  }});

                  out = {{
                    status: res.status,
                    response: JSON.parse(await res.text()),
                    calls
                  }};
                }}

                if (scenario === "valid_eab") {{
                  const res = await eabRequest({{
                    bodyObj: {{
                      schema_version: "1.0",
                      request_id: "req_5",
                      operation_id: "EAB_LIST_PENDING",
                      owner_chat_id: 111
                    }}
                  }});

                  out = {{
                    status: res.status,
                    response: JSON.parse(await res.text()),
                    calls
                  }};
                }}

                console.log(JSON.stringify(out));
                """
            ),
            encoding="utf-8",
        )

        active = ACTIVE_JS.read_text(encoding="utf-8")
        match = re.search(
            r"/\* EAB_M12_READ_ONLY_RECEIVER_START \*/"
            r"(.*?)"
            r"/\* EAB_M12_READ_ONLY_RECEIVER_END \*/",
            active,
            re.S,
        )
        if not match:
            raise RuntimeError("EAB Apps Script block not found")

        block = match.group(1)

        cls.apps_runner = cls.tmp / "apps_runner.mjs"
        cls.apps_runner.write_text(
            textwrap.dedent(
                """
                import { createHash, createHmac } from "node:crypto";

                const scenario = process.argv[2];
                const store = new Map();

                const scriptProps = {
                  getProperty(k) {
                    return store.has(k) ? store.get(k) : null;
                  },
                  setProperty(k, v) {
                    store.set(String(k), String(v));
                  },
                  deleteProperty(k) {
                    store.delete(String(k));
                  },
                  getProperties() {
                    return Object.fromEntries(store.entries());
                  }
                };

                globalThis.PropertiesService = {
                  getScriptProperties() {
                    return scriptProps;
                  }
                };

                globalThis.LockService = {
                  getScriptLock() {
                    return {
                      tryLock() { return true; },
                      releaseLock() {}
                    };
                  }
                };

                function signedBytes(buffer) {
                  return Array.from(buffer, (b) => b > 127 ? b - 256 : b);
                }

                globalThis.Utilities = {
                  Charset: { UTF_8: "UTF_8" },
                  DigestAlgorithm: { SHA_256: "SHA_256" },

                  computeHmacSha256Signature(value, key) {
                    return signedBytes(
                      createHmac("sha256", String(key))
                        .update(String(value))
                        .digest()
                    );
                  },

                  computeDigest(_algo, value) {
                    return signedBytes(
                      createHash("sha256")
                        .update(String(value))
                        .digest()
                    );
                  }
                };

                globalThis.ContentService = {
                  MimeType: { JSON: "application/json" },
                  createTextOutput(text) {
                    return {
                      text: String(text),
                      setMimeType() { return this; }
                    };
                  }
                };

                globalThis.clarificationPropKey_ = function(chatId) {
                  return "AIRO_PENDING_CLARIFICATION_" +
                    String(chatId || "").trim();
                };
                """
            )
            + "\n"
            + block
            + "\n"
            + textwrap.dedent(
                """
                const internalSecret = "test_internal_secret";
                store.set("EAB_INTERNAL_AUTH_TOKEN", internalSecret);
                store.set("EAB_OWNER_CHAT_ID_ALLOWLIST", "111");

                function makeEnvelope(overrides = {}) {
                  const meta = {
                    marker: "AIRO_EAB_INTERNAL_V1",
                    schema_version: "1.0",
                    request_id: "req_runtime_1",
                    operation_id: "EAB_LIST_PENDING",
                    owner_chat_id: 111,
                    key_id: "key_current",
                    nonce: "abcdef0123456789",
                    issued_at: Math.floor(Date.now() / 1000),
                    body_sha256: "a".repeat(64),
                    mac: ""
                  };

                  Object.assign(meta, overrides);

                  const canonical =
                    "v=1.0" +
                    "&op=" + meta.operation_id +
                    "&req_id=" + meta.request_id +
                    "&owner_chat_id=" + String(meta.owner_chat_id) +
                    "&key_id=" + meta.key_id +
                    "&nonce=" + meta.nonce +
                    "&ts=" + meta.issued_at +
                    "&body_sha256=" + meta.body_sha256;

                  meta.mac = createHmac("sha256", internalSecret)
                    .update(canonical)
                    .digest("hex");

                  if (overrides.mac !== undefined) {
                    meta.mac = overrides.mac;
                  }

                  return {
                    postData: {
                      contents: JSON.stringify({
                        _eab_internal: meta
                      })
                    }
                  };
                }

                function parsed(result) {
                  if (result === null) return null;
                  return JSON.parse(result.text);
                }

                let out = {};

                if (scenario === "normal_bypass") {
                  out = {
                    result: airoEabMaybeHandleInternalRequest_({
                      postData: {
                        contents: JSON.stringify({
                          update_id: 1,
                          message: { text: "halo" }
                        })
                      }
                    })
                  };
                }

                if (scenario === "empty_pending") {
                  out = parsed(
                    airoEabMaybeHandleInternalRequest_(makeEnvelope())
                  );
                }

                if (scenario === "one_pending") {
                  store.set(
                    clarificationPropKey_(111),
                    JSON.stringify({
                      pending_id: "pending:1",
                      type: "missing_account",
                      amount: 50000,
                      category: "Food",
                      description: "GrabFood",
                      created_at: "2026-08-02T00:00:00Z"
                    })
                  );

                  out = parsed(
                    airoEabMaybeHandleInternalRequest_(makeEnvelope())
                  );
                }

                if (scenario === "corrupt_pending") {
                  const key = clarificationPropKey_(111);
                  store.set(key, "{broken");

                  out = {
                    response: parsed(
                      airoEabMaybeHandleInternalRequest_(makeEnvelope())
                    ),
                    pendingAfter: store.get(key)
                  };
                }

                if (scenario === "bad_internal_mac") {
                  out = parsed(
                    airoEabMaybeHandleInternalRequest_(
                      makeEnvelope({ mac: "00".repeat(32) })
                    )
                  );
                }

                if (scenario === "bad_owner") {
                  out = parsed(
                    airoEabMaybeHandleInternalRequest_(
                      makeEnvelope({ owner_chat_id: 222 })
                    )
                  );
                }

                if (scenario === "replay") {
                  const envelope = makeEnvelope();
                  const first = parsed(
                    airoEabMaybeHandleInternalRequest_(envelope)
                  );
                  const second = parsed(
                    airoEabMaybeHandleInternalRequest_(envelope)
                  );

                  out = { first, second };
                }

                console.log(JSON.stringify(out));
                """
            ),
            encoding="utf-8",
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run_node(self, script, scenario):
        proc = subprocess.run(
            ["node", str(script), scenario],
            text=True,
            capture_output=True,
            check=False,
        )

        if proc.returncode != 0:
            self.fail(
                "node runtime failed\\nSTDOUT:\\n"
                + proc.stdout
                + "\\nSTDERR:\\n"
                + proc.stderr
            )

        return json.loads(proc.stdout.strip().splitlines()[-1])

    def test_01_worker_node_syntax(self):
        proc = subprocess.run(
            ["node", "--check", str(self.worker_mjs)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_02_normal_telegram_runtime_preserved(self):
        out = self.run_node(self.worker_runner, "normal_telegram")
        self.assertEqual(out["status"], 200)
        self.assertEqual(out["response"]["mode"], "async_ack")
        self.assertEqual(len(out["calls"]), 1)
        self.assertEqual(
            out["calls"][0]["url"],
            "https://apps.example.test/exec",
        )
        self.assertEqual(out["calls"][0]["body"], out["originalBody"])

    def test_03_missing_external_headers_fail_closed(self):
        out = self.run_node(self.worker_runner, "missing_auth")
        self.assertEqual(out["status"], 401)
        self.assertEqual(out["response"]["error"], "ERR_MISSING_AUTH")
        self.assertEqual(out["calls"], [])

    def test_04_bad_external_signature_fail_closed(self):
        out = self.run_node(self.worker_runner, "bad_signature")
        self.assertEqual(out["status"], 401)
        self.assertEqual(
            out["response"]["error"],
            "ERR_INVALID_SIGNATURE",
        )
        self.assertEqual(out["calls"], [])

    def test_05_owner_allowlist_fail_closed(self):
        out = self.run_node(self.worker_runner, "bad_owner")
        self.assertEqual(out["status"], 403)
        self.assertEqual(
            out["response"]["error"],
            "ERR_OWNER_NOT_AUTHORIZED",
        )
        self.assertEqual(out["calls"], [])

    def test_06_only_list_pending_operation_reachable(self):
        out = self.run_node(self.worker_runner, "unknown_operation")
        self.assertEqual(out["status"], 400)
        self.assertEqual(
            out["response"]["error"],
            "ERR_INVALID_REQUEST",
        )
        self.assertEqual(out["calls"], [])

    def test_07_valid_eab_runtime_builds_authenticated_internal_envelope(self):
        out = self.run_node(self.worker_runner, "valid_eab")
        self.assertEqual(out["status"], 200)
        self.assertEqual(len(out["calls"]), 1)

        internal = json.loads(out["calls"][0]["body"])["_eab_internal"]
        self.assertEqual(internal["marker"], "AIRO_EAB_INTERNAL_V1")
        self.assertEqual(internal["operation_id"], "EAB_LIST_PENDING")
        self.assertEqual(internal["owner_chat_id"], 111)
        self.assertRegex(internal["mac"], r"^[0-9a-f]{64}$")

    def test_08_normal_apps_script_request_bypasses_eab(self):
        out = self.run_node(self.apps_runner, "normal_bypass")
        self.assertIsNone(out["result"])

    def test_09_empty_real_pending_runtime_returns_empty_list(self):
        out = self.run_node(self.apps_runner, "empty_pending")
        self.assertEqual(out["application_status"], "SUCCESS")
        self.assertEqual(out["payload"]["items"], [])

    def test_10_one_real_pending_runtime_returns_one_bounded_item(self):
        out = self.run_node(self.apps_runner, "one_pending")
        self.assertEqual(out["application_status"], "SUCCESS")
        self.assertEqual(len(out["payload"]["items"]), 1)
        item = out["payload"]["items"][0]
        self.assertEqual(item["amount"], 50000)
        self.assertEqual(item["description"], "GrabFood")
        self.assertNotIn("rawText", item)
        self.assertNotIn("original_text", item)

    def test_11_corrupt_pending_fails_closed_without_deleting_business_state(self):
        out = self.run_node(self.apps_runner, "corrupt_pending")
        self.assertEqual(
            out["response"]["application_error_code"],
            "ERR_CORRUPT_PENDING_STATE",
        )
        self.assertEqual(out["pendingAfter"], "{broken")

    def test_12_bad_internal_mac_rejected(self):
        out = self.run_node(self.apps_runner, "bad_internal_mac")
        self.assertEqual(out["error"], "ERR_INVALID_INTERNAL_AUTH")

    def test_13_internal_owner_scope_rejected(self):
        out = self.run_node(self.apps_runner, "bad_owner")
        self.assertEqual(out["error"], "ERR_OWNER_NOT_AUTHORIZED")

    def test_14_replay_is_durable_keyed_security_state(self):
        out = self.run_node(self.apps_runner, "replay")
        self.assertEqual(
            out["first"]["application_status"],
            "SUCCESS",
        )
        self.assertEqual(
            out["second"]["error"],
            "ERR_NONCE_REPLAYED",
        )

    def test_15_active_and_mirror_have_same_eab_block(self):
        def block(path):
            text = path.read_text(encoding="utf-8")
            m = re.search(
                r"/\* EAB_M12_READ_ONLY_RECEIVER_START \*/"
                r"(.*?)"
                r"/\* EAB_M12_READ_ONLY_RECEIVER_END \*/",
                text,
                re.S,
            )
            self.assertIsNotNone(m)
            return m.group(1)

        self.assertEqual(block(ACTIVE_JS), block(MIRROR_GS))

    def test_16_eab_block_has_zero_finance_business_side_effect_calls(self):
        text = ACTIVE_JS.read_text(encoding="utf-8")
        m = re.search(
            r"/\* EAB_M12_READ_ONLY_RECEIVER_START \*/"
            r"(.*?)"
            r"/\* EAB_M12_READ_ONLY_RECEIVER_END \*/",
            text,
            re.S,
        )
        self.assertIsNotNone(m)
        eab = m.group(1)

        forbidden = [
            "clearPendingClarification_(",
            "savePendingClarification_(",
            "sendTelegram_(",
            "writeRouted_(",
            "writeInternalTransferToAccountLedger_(",
        ]

        for token in forbidden:
            self.assertNotIn(token, eab)


if __name__ == "__main__":
    unittest.main()
