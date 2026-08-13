const JSON_HEADERS = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": "no-store"
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: JSON_HEADERS
  });
}

function bytesToHex(bytes) {
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

async function sha256Hex(text) {
  const digest = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(text)
  );
  return bytesToHex(new Uint8Array(digest));
}

async function hmacSha256Hex(secret, text) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );

  const signature = await crypto.subtle.sign(
    "HMAC",
    key,
    new TextEncoder().encode(text)
  );

  return bytesToHex(new Uint8Array(signature));
}

function constantTimeHexEqual(a, b) {
  const left = String(a || "").toLowerCase();
  const right = String(b || "").toLowerCase();

  if (left.length !== right.length || left.length === 0) return false;

  let diff = 0;
  for (let i = 0; i < left.length; i += 1) {
    diff |= left.charCodeAt(i) ^ right.charCodeAt(i);
  }
  return diff === 0;
}

function ownerAllowed(ownerChatId, rawAllowlist) {
  const owner = String(ownerChatId ?? "").trim();
  if (!owner) return false;

  const allowed = String(rawAllowlist || "")
    .split(",")
    .map((v) => v.trim())
    .filter(Boolean);

  return allowed.includes(owner);
}

function selectServiceSecret(env, keyId) {
  const currentId = String(env.EAB_SERVICE_AUTH_KEY_ID || "").trim();
  const currentSecret = String(env.EAB_SERVICE_SECRET || "");

  if (currentId && currentSecret && keyId === currentId) {
    return currentSecret;
  }
  return "";
}

// Bounded 4 Operations: EAB_GET_PENDING, EAB_LIST_PENDING, EAB_SUBMIT_BATCH_CLARIFICATION, EAB_CREATE_MANUAL_TRANSACTION
const ALLOWED_EAB_OPERATIONS = new Set([
  "EAB_GET_PENDING",
  "EAB_LIST_PENDING",
  "EAB_SUBMIT_BATCH_CLARIFICATION",
  "EAB_CREATE_MANUAL_TRANSACTION"
]);

async function handleEabBoundedDispatcher(request, env) {
  const target = env.APPS_SCRIPT_URL;
  if (!target) {
    return json({ ok: false, error: "missing_apps_script_url" }, 500);
  }

  if (
    !env.EAB_SERVICE_AUTH_KEY_ID ||
    !env.EAB_SERVICE_SECRET ||
    !env.EAB_INTERNAL_AUTH_TOKEN ||
    !env.EAB_OWNER_CHAT_ID_ALLOWLIST
  ) {
    return json({ ok: false, error: "eab_configuration_missing" }, 503);
  }

  const keyId = String(request.headers.get("X-EAB-Key-ID") || "").trim();
  const timestampRaw = String(request.headers.get("X-EAB-Timestamp") || "").trim();
  const nonce = String(request.headers.get("X-EAB-Nonce") || "").trim();
  const suppliedSignature = String(request.headers.get("X-EAB-Signature") || "").trim();

  if (!keyId || !timestampRaw || !nonce || !suppliedSignature) {
    return json({ ok: false, error: "ERR_MISSING_AUTH" }, 401);
  }

  const serviceSecret = selectServiceSecret(env, keyId);
  if (!serviceSecret) {
    return json({ ok: false, error: "ERR_INVALID_AUTH_KEY" }, 401);
  }

  if (!/^[0-9a-fA-F]{16}$/.test(nonce)) {
    return json({ ok: false, error: "ERR_INVALID_NONCE" }, 401);
  }

  const timestamp = Number(timestampRaw);
  const nowSeconds = Math.floor(Date.now() / 1000);
  if (!Number.isInteger(timestamp) || Math.abs(nowSeconds - timestamp) > 300) {
    return json({ ok: false, error: "ERR_EXPIRED_AUTH_TIMESTAMP" }, 401);
  }

  const rawBody = await request.text();
  let body;
  try {
    body = JSON.parse(rawBody);
  } catch (_) {
    return json({ ok: false, error: "ERR_INVALID_JSON" }, 400);
  }

  if (
    !body ||
    body.schema_version !== "1.0" ||
    typeof body.request_id !== "string" ||
    !body.request_id.trim() ||
    !ALLOWED_EAB_OPERATIONS.has(body.operation_id) ||
    body.owner_chat_id === undefined ||
    body.owner_chat_id === null
  ) {
    return json({ ok: false, error: "ERR_INVALID_REQUEST_OR_OPERATION" }, 400);
  }

  if (!ownerAllowed(body.owner_chat_id, env.EAB_OWNER_CHAT_ID_ALLOWLIST)) {
    return json({ ok: false, error: "ERR_OWNER_NOT_AUTHORIZED" }, 403);
  }

  const bodySha256 = await sha256Hex(rawBody);
  const canonical = `v=1.0&op=${body.operation_id}&req_id=${body.request_id}&ts=${timestampRaw}&nonce=${nonce}&body_sha256=${bodySha256}`;
  const expectedSignature = await hmacSha256Hex(serviceSecret, canonical);

  if (!constantTimeHexEqual(expectedSignature, suppliedSignature)) {
    return json({ ok: false, error: "ERR_INVALID_SIGNATURE" }, 401);
  }

  // Forward cryptographically bound payload to Apps Script bounded receiver
  const upstreamResp = await fetch(target, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: rawBody
  });

  const upstreamData = await upstreamResp.json();
  return json(upstreamData, upstreamResp.status);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/eab") {
      return handleEabBoundedDispatcher(request, env);
    }
    return json({ error: "not_found" }, 404);
  }
};
