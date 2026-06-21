const NOTION_VERSION = "2022-06-28";

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function splitText(text: string, size = 1900) {
  const parts: string[] = [];
  for (let i = 0; i < text.length; i += size) {
    parts.push(text.slice(i, i + size));
  }
  return parts.length ? parts : [""];
}

async function sendTelegram(env: any, chatId: number, text: string) {
  await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      chat_id: chatId,
      text,
      disable_web_page_preview: true,
    }),
  });
}

async function createRecentCapture(env: any, rawText: string) {
  const title = rawText.slice(0, 80) || "Telegram Capture";

  const rawBlocks = splitText(rawText).map((part) => ({
    object: "block",
    type: "paragraph",
    paragraph: {
      rich_text: [{ type: "text", text: { content: part } }],
    },
  }));

  const res = await fetch("https://api.notion.com/v1/pages", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.NOTION_TOKEN}`,
      "Notion-Version": NOTION_VERSION,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      parent: { database_id: env.RECENT_CAPTURES_DB_ID },
      properties: {
        Capture: {
          title: [{ text: { content: title } }],
        },
        "Raw Input": {
          rich_text: [{ text: { content: rawText.slice(0, 1900) } }],
        },
        Source: {
          select: { name: "Telegram" },
        },
        Status: {
          select: { name: "Captured" },
        },
        "Routed To": {
          select: { name: "Inbox" },
        },
        Reason: {
          rich_text: [
            {
              text: {
                content:
                  "Telegram quick capture default: masuk Inbox dulu. Final routing akan diproses belakangan.",
              },
            },
          ],
        },
        "Destination DB": {
          rich_text: [{ text: { content: "Inbox (pending final routing)" } }],
        },
        "Captured At": {
          date: { start: new Date().toISOString() },
        },
      },
      children: [
        {
          object: "block",
          type: "heading_2",
          heading_2: {
            rich_text: [{ type: "text", text: { content: "Raw Note" } }],
          },
        },
        ...rawBlocks,
      ],
    }),
  });

  const data: any = await res.json();

  if (!res.ok) {
    throw new Error(JSON.stringify(data));
  }

  return data;
}

export default {
  async fetch(request: Request, env: any): Promise<Response> {
    const url = new URL(request.url);

    if (request.method === "GET" && url.pathname === "/health") {
      return json({
        ok: true,
        service: "earnsai-telegram-gateway",
        phase: "telegram-webhook-minimal",
      });
    }

    if (request.method === "POST" && url.pathname === `/telegram/${env.TELEGRAM_SECRET_PATH}`) {
      const update: any = await request.json();

      const message = update.message || update.edited_message;
      const chatId = message?.chat?.id;
      const rawText = message?.text || message?.caption || "";

      if (!chatId || !rawText.trim()) {
        return json({ ok: true, ignored: true, reason: "No text message found" });
      }

      try {
        const page = await createRecentCapture(env, rawText);

        await sendTelegram(
          env,
          chatId,
          `✅ Tercatat di Recent Captures.\n\nRaw note aman.\n${page.url}`
        );

        return json({
          ok: true,
          captured: true,
          page_id: page.id,
          url: page.url,
        });
      } catch (err: any) {
        await sendTelegram(
          env,
          chatId,
          `❌ Gagal mencatat ke Notion.\n\n${String(err.message || err).slice(0, 500)}`
        );

        return json(
          {
            ok: false,
            error: String(err.message || err),
          },
          500
        );
      }
    }

    return json({ ok: false, error: "Not found" }, 404);
  },
};
