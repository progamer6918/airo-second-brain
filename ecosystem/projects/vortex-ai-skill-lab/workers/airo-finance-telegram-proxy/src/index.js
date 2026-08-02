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

function constantTimeCompare(a, b) {
  if (typeof a !== "string" || typeof b !== "string") return false;
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return result === 0;
}

export default {
  async fetch(request, env, ctx) {
    const startedAt = Date.now();
    const url = new URL(request.url);

    // Check for EAB header ingress (/eab route or X-EAB-Key-ID header)
    const eabKeyId = request.headers.get("X-EAB-Key-ID");
    const isEabRoute = url.pathname === "/eab" || Boolean(eabKeyId);

    if (isEabRoute) {
      const timestamp = request.headers.get("X-EAB-Timestamp");
      const nonce = request.headers.get("X-EAB-Nonce");
      const signature = request.headers.get("X-EAB-Signature");

      if (!eabKeyId || !timestamp || !nonce || !signature) {
        return json({ status: "UNAUTHORIZED", error: "Missing required X-EAB headers" }, 401);
      }

      const eabSecret = env.EAB_SERVICE_SECRET;
      if (!eabSecret) {
        return json({ status: "CONFIG_ERROR", error: "Missing external EAB service secret configuration" }, 500);
      }

      const internalSecret = env.EAB_INTERNAL_AUTH_TOKEN;
      if (!internalSecret) {
        return json({ status: "CONFIG_ERROR", error: "Missing internal EAB shared secret configuration" }, 500);
      }

      const tsNum = parseInt(timestamp, 10);
      const nowSec = Math.floor(Date.now() / 1000);
      if (isNaN(tsNum) || Math.abs(nowSec - tsNum) > 300) {
        return json({ status: "EXPIRED_TIMESTAMP", error: "Timestamp skew exceeded window" }, 401);
      }

      const bodyText = await request.text();
      let eabPayload = {};
      try { eabPayload = JSON.parse(bodyText); } catch (e) {
        return json({ status: "MALFORMED_REQUEST", error: "Invalid JSON body" }, 400);
      }

      if (eabPayload.action !== "eabListPending") {
        return json({ status: "INVALID_ACTION", error: "Operation not allowed" }, 403);
      }

      if (!constantTimeCompare(signature, eabSecret)) {
        return json({ status: "UNAUTHORIZED", error: "Invalid signature" }, 401);
      }

      const internalEnvelope = {
        is_eab_internal: true,
        action: "eabListPending",
        chat_id: eabPayload.chat_id,
        actor_user_id: eabPayload.actor_user_id,
        internal_auth_token: internalSecret
      };

      const target = env.APPS_SCRIPT_URL;
      const appsScriptRes = await fetch(target, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(internalEnvelope),
        redirect: "follow"
      });

      const resText = await appsScriptRes.text().catch(() => "");
      try { return json(JSON.parse(resText), appsScriptRes.status); } catch (err) {
        return json({ status: "UPSTREAM_ERROR", raw: resText.slice(0, 200) }, 502);
      }
    }

    // Normal Telegram Worker forwarding path (UNCHANGED)
    const body = await request.text();

    const forwardPromise = fetch(target, {
      method: "POST",
      headers: {
        "content-type": request.headers.get("content-type") || "application/json"
      },
      body,
      redirect: "follow"
    })
      .then(async (res) => {
        const text = await res.text().catch(() => "");
        console.log("AIRO_PROXY_FORWARD_DONE", {
          status: res.status,
          ok: res.ok,
          elapsed_ms: Date.now() - startedAt,
          response_preview: text.slice(0, 160)
        });
      })
      .catch((err) => {
        console.error("AIRO_PROXY_FORWARD_FAILED", {
          message: err && err.message ? err.message : String(err)
        });
      });

    if (ctx && typeof ctx.waitUntil === "function") {
      ctx.waitUntil(forwardPromise);
      return json({
        ok: true,
        mode: "async_ack"
      });
    }

    await forwardPromise;
    return json({
      ok: true,
      mode: "sync_fallback"
    });
  }
};
