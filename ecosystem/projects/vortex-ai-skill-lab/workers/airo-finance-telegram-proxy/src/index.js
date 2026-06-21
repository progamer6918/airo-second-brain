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

export default {
  async fetch(request, env, ctx) {
    const startedAt = Date.now();

    if (request.method === "GET") {
      return json({
        ok: true,
        service: "airo-finance-telegram-proxy",
        mode: "async_ack",
        target_configured: Boolean(env.APPS_SCRIPT_URL)
      });
    }

    if (request.method !== "POST") {
      return json({
        ok: false,
        error: "method_not_allowed",
        allowed: ["GET", "POST"]
      }, 405);
    }

    const target = env.APPS_SCRIPT_URL;
    if (!target) {
      console.error("AIRO_PROXY_MISSING_APPS_SCRIPT_URL");
      return json({
        ok: false,
        error: "missing_apps_script_url"
      }, 500);
    }

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
