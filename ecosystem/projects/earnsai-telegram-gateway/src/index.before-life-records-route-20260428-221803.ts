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


type InitialRoute = {
  routedTo: string;
  destinationDb: string;
  reason: string;
};

function classifyInitialRoute(rawText: string): InitialRoute {
  const text = rawText.toLowerCase();

  const escapeRegExp = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  const hasAny = (words: string[]) =>
    words.some((word) => {
      const escaped = escapeRegExp(word.toLowerCase()).replace(/\\s+/g, "\\s+");
      const pattern = new RegExp(`(^|[^a-z0-9])${escaped}([^a-z0-9]|$)`, "i");
      return pattern.test(text);
    });

  if (hasAny(["openc claw", "openclaw", "notion", "worker", "cloudflare", "wrangler", "bug", "error", "api", "deploy", "webhook", "typescript", "script"])) {
    return {
      routedTo: "EarnsAI Dev Lab",
      destinationDb: "EarnsAI Dev Lab (pending final routing)",
      reason: "Rule-based initial route: technical setup, bug, API, deployment, Notion, OpenClaw, or Worker related capture.",
    };
  }

  if (hasAny(["jurnal", "artikel", "buku", "paper", "doi", "daftar pustaka", "referensi", "citation", "sitasi"])) {
    return {
      routedTo: "Sources",
      destinationDb: "Sources / Daftar Pustaka (pending final routing)",
      reason: "Rule-based initial route: academic source, article, book, paper, citation, or bibliography related capture.",
    };
  }

  const hasNegatedReminder = hasAny([
    "bukan reminder",
    "tanpa reminder",
    "bukan tolong ingatkan",
    "jangan ingatkan",
    "tidak perlu diingatkan",
    "bukan pengingat",
    "tanpa pengingat",
  ]);

  const hasExplicitReminder = !hasNegatedReminder && hasAny([
    "ingatkan",
    "reminder",
    "tolong ingatkan",
  ]);

  const hasTaskSignal = hasAny([
    "deadline",
    "follow up",
    "todo",
    "tugas",
    "kerjakan",
    "action item",
  ]);

  if (hasExplicitReminder || hasTaskSignal) {
    return {
      routedTo: "Tasks",
      destinationDb: "Tasks (pending final routing)",
      reason: "Rule-based initial route: explicit reminder, task, deadline, follow-up, or action item detected.",
    };
  }

  if (hasAny(["portfolio", "portofolio", "cv", "cv bullet", "achievement", "star story", "linkedin", "career", "karier", "prestasi"])) {
    return {
      routedTo: "Career & Portfolio",
      destinationDb: "Career & Portfolio (pending final routing)",
      reason: "Rule-based initial route: achievement, CV bullet, portfolio, STAR story, LinkedIn, or career-related capture.",
    };
  }

  if (hasAny(["goal", "habit", "skill", "latihan", "perkembangan diri", "self improvement", "belajar", "target pribadi"])) {
    return {
      routedTo: "Growth Lab",
      destinationDb: "Growth Lab (pending final routing)",
      reason: "Rule-based initial route: goal, habit, skill, practice, learning, or personal growth related capture.",
    };
  }

  if (hasAny(["honda", "dealer", "sales", "leasing", "prospek", "market", "coaching"])) {
    return {
      routedTo: "Work Hub",
      destinationDb: "Work Hub (pending final routing)",
      reason: "Rule-based initial route: Honda, dealer, sales, coaching, or work-related capture.",
    };
  }

  if (hasAny(["ide", "insight", "refleksi", "catatan", "catatan umum", "skripsi", "pai", "penelitian", "tesis", "rumusan masalah", "metode penelitian", "kajian teori"])) {
    return {
      routedTo: "Notes",
      destinationDb: "Notes (pending final routing)",
      reason: "Rule-based initial route: academic note, research idea, thesis, PAI, or study-related capture.",
    };
  }

  return {
    routedTo: "Inbox",
    destinationDb: "Inbox (pending final routing)",
    reason: "Rule-based initial route: ambiguous capture, keep in Inbox until final routing.",
  };
}

async function createRecentCapture(env: any, rawText: string) {
  const title = rawText.slice(0, 80) || "Telegram Capture";
  const initialRoute = classifyInitialRoute(rawText);

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
          select: { name: initialRoute.routedTo },
        },
        Reason: {
          rich_text: [
            {
              text: {
                content: initialRoute.reason,
              },
            },
          ],
        },
        "Destination DB": {
          rich_text: [{ text: { content: initialRoute.destinationDb } }],
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
