import { runFinalRouting } from "./finalRouting";

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



function buildBubuReply(pageUrl: string) {
  const templates = [
    `✅ Bubu catat ya.

Sudah masuk Recent Captures.
Raw note aman.
${pageUrl}`,

    `✅ Noted. Bubu sudah terima di meja depan.

Masuk Recent Captures.
${pageUrl}`,

    `✅ Aman, sudah Bubu simpan.

Recent Captures sudah update.
${pageUrl}`,

    `✅ Bubu sudah check-in catatan ini.

Masuk ke Recent Captures.
${pageUrl}`,

    `✅ Sip, Bubu terima.

Raw note aman di Recent Captures.
${pageUrl}`,

    `✅ Diterima di front desk Bubu.

Sudah tercatat di Recent Captures.
${pageUrl}`,

    `✅ Bubu sudah pegang catatan ini.

Sudah masuk Recent Captures.
${pageUrl}`,

    `✅ Catatan sudah mampir ke meja Bubu.

Recent Captures aman.
${pageUrl}`,

    `✅ Bubu terima.

Sudah Bubu masukin ke jalur capture.
${pageUrl}`,

    `✅ Masuk antrean rapi Bubu.

Tercatat di Recent Captures.
${pageUrl}`,

    `✅ Oke, Bubu sudah catat.

Raw note aman.
${pageUrl}`,

    `✅ Pesan diterima.

Bubu taruh di Recent Captures.
${pageUrl}`,

    `✅ Bubu sudah proses intake catatan ini.

Masuk Recent Captures.
${pageUrl}`,

    `✅ Catatan aman di meja Bubu.

Recent Captures sudah update.
${pageUrl}`,

    `✅ Bubu sudah terima dan teruskan.

Masuk Recent Captures.
${pageUrl}`,

    `✅ Front desk Bubu sudah menerima catatan ini.

Raw note aman.
${pageUrl}`,

    `✅ Bubu simpan dulu di capture desk.

Sudah masuk Recent Captures.
${pageUrl}`,

    `✅ Beres. Bubu sudah catat.

Recent Captures aman.
${pageUrl}`,
  ];

  return templates[Math.floor(Math.random() * templates.length)];
}


type InitialRoute = {
  routedTo: string;
  destinationDb: string;
  reason: string;
};


const AUTO_MERGE_IDLE_MS = 10_000;
const AUTO_MERGE_MAX_MS = 60_000;

type AutoMergeBufferEntry = {
  chatId: number;
  userId: string;
  parts: string[];
  idleVersion: number;
  flushing: boolean;
};

const autoMergeBuffers = new Map<string, AutoMergeBufferEntry>();

const AUTO_MERGE_CAPTURE_TRIGGERS = [
  "catat",
  "catat ini",
  "catat ini ya",
  "simpan",
  "simpan ini",
  "save this",
];

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function getAutoMergeUserId(message: any): string {
  return String(message?.from?.id || "unknown");
}

function getAutoMergeBufferKey(chatId: number, userId: string): string {
  return `${chatId}:${userId}`;
}

function isAutoMergeCaptureTrigger(rawText: string): boolean {
  const text = rawText.trim().toLowerCase();

  return AUTO_MERGE_CAPTURE_TRIGGERS.some((trigger) =>
    text === trigger ||
    text.startsWith(`${trigger} `) ||
    text.startsWith(`${trigger}\n`) ||
    text.startsWith(`${trigger}:`)
  );
}

async function flushAutoMergeBuffer(
  env: any,
  ctx: ExecutionContext,
  chatId: number,
  userId: string,
  reason: string
): Promise<any | null> {
  const key = getAutoMergeBufferKey(chatId, userId);
  const entry = autoMergeBuffers.get(key);

  if (!entry || entry.flushing) return null;

  entry.flushing = true;
  autoMergeBuffers.delete(key);

  const mergedText = entry.parts.map((x) => x.trim()).filter(Boolean).join("\n").trim();
  if (!mergedText) return null;

  try {
    const page = await createRecentCapture(env, mergedText);
    const initialRoute = classifyInitialRoute(mergedText);
    const job = runFinalRouting(env, mergedText, initialRoute, page.id, page.url)
      .catch((err: any) => console.error("Final routing failed", err?.message || err));

    ctx.waitUntil(job);

    await sendTelegram(env, chatId, buildBubuReply(page.url));
    return page;
  } catch (err: any) {
    console.error(`Auto merge flush failed: ${reason}`, err?.message || err);
    await sendTelegram(
      env,
      chatId,
      `❌ Gagal mencatat gabungan pesan ke Notion.\n\n${String(err.message || err).slice(0, 500)}`
    ).catch((sendErr: any) => console.error("Failed to send auto merge error", sendErr?.message || sendErr));

    return null;
  }
}

function scheduleAutoMergeIdleFlush(
  env: any,
  ctx: ExecutionContext,
  chatId: number,
  userId: string,
  idleVersion: number
): void {
  const key = getAutoMergeBufferKey(chatId, userId);

  ctx.waitUntil(
    sleep(AUTO_MERGE_IDLE_MS).then(() => {
      const current = autoMergeBuffers.get(key);
      if (!current || current.idleVersion !== idleVersion) return null;
      return flushAutoMergeBuffer(env, ctx, chatId, userId, "idle-timeout");
    })
  );
}

function scheduleAutoMergeMaxFlush(env: any, ctx: ExecutionContext, chatId: number, userId: string): void {
  ctx.waitUntil(
    sleep(AUTO_MERGE_MAX_MS).then(() => flushAutoMergeBuffer(env, ctx, chatId, userId, "max-timeout"))
  );
}

async function startAutoMergeBuffer(
  env: any,
  ctx: ExecutionContext,
  chatId: number,
  userId: string,
  rawText: string
): Promise<void> {
  const entry: AutoMergeBufferEntry = {
    chatId,
    userId,
    parts: [rawText.trim()],
    idleVersion: 1,
    flushing: false,
  };

  autoMergeBuffers.set(getAutoMergeBufferKey(chatId, userId), entry);

  scheduleAutoMergeIdleFlush(env, ctx, chatId, userId, entry.idleVersion);
  scheduleAutoMergeMaxFlush(env, ctx, chatId, userId);

  await sendTelegram(
    env,
    chatId,
    "🧩 Siap, aku tunggu lanjutan catatannya sekitar 10 detik. Kalau sudah diam, aku gabungkan lalu simpan ke Notion."
  );
}

function appendAutoMergeBuffer(
  env: any,
  ctx: ExecutionContext,
  chatId: number,
  userId: string,
  rawText: string
): boolean {
  const entry = autoMergeBuffers.get(getAutoMergeBufferKey(chatId, userId));
  if (!entry || entry.flushing) return false;

  entry.parts.push(rawText.trim());
  entry.idleVersion += 1;

  scheduleAutoMergeIdleFlush(env, ctx, chatId, userId, entry.idleVersion);
  return true;
}


function classifyInitialRoute(rawText: string): InitialRoute {
  const text = rawText.toLowerCase();

  const escapeRegExp = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  const hasAny = (words: string[]) =>
    words.some((word) => {
      const escaped = escapeRegExp(word.toLowerCase()).replace(/\\s+/g, "\\s+");
      const pattern = new RegExp(`(^|[^a-z0-9])${escaped}([^a-z0-9]|$)`, "i");
      return pattern.test(text);
    });

  if (hasAny(["ai system log", "system log", "log teknis", "error sistem", "migrasi", "migration", "perubahan workflow", "workflow log", "log ai"])) {
    return {
      routedTo: "AI System Log",
      destinationDb: "AI System Log (pending final routing)",
      reason: "Rule-based initial route: system error, migration, workflow change, or technical AI log related capture.",
    };
  }

  if (hasAny(["openc claw", "openclaw", "notion", "worker", "cloudflare", "wrangler", "bug", "error", "api", "deploy", "webhook", "typescript", "script"])) {
    return {
      routedTo: "EarnsAI Dev Lab",
      destinationDb: "EarnsAI Dev Lab (pending final routing)",
      reason: "Rule-based initial route: technical setup, bug, API, deployment, Notion, OpenClaw, or Worker related capture.",
    };
  }

  if (hasAny(["projects", "project", "proyek", "proyek besar", "milestone", "fase kerja", "inisiatif besar", "roadmap"])) {
    return {
      routedTo: "Projects",
      destinationDb: "Projects (pending final routing)",
      reason: "Rule-based initial route: project, initiative, milestone, roadmap, or multi-phase work related capture.",
    };
  }

  if (hasAny(["areas", "area", "area hidup", "tanggung jawab jangka panjang", "bidang tanggung jawab", "jangka panjang", "life area"])) {
    return {
      routedTo: "Areas",
      destinationDb: "Areas (pending final routing)",
      reason: "Rule-based initial route: long-term responsibility, life area, or ongoing area of responsibility related capture.",
    };
  }

  if (hasAny(["weekly digest", "rekap mingguan", "review mingguan", "ringkasan mingguan", "ringkasan progress", "archive digest", "digest mingguan"])) {
    return {
      routedTo: "Weekly Digest",
      destinationDb: "Weekly Digest (pending final routing)",
      reason: "Rule-based initial route: weekly recap, weekly review, progress summary, archive digest, or digest related capture.",
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

  if (hasAny(["top of mind", "prioritas aktif", "memenuhi kepala", "urgent", "fokus utama", "fokus", "kepikiran", "pikiran utama"])) {
    return {
      routedTo: "Top of Mind",
      destinationDb: "Top of Mind (pending final routing)",
      reason: "Rule-based initial route: active priority, urgent focus, or top-of-mind capture.",
    };
  }

  if (hasAny(["finance", "keuangan", "household", "personal record", "asset", "aset", "life admin", "dokumen pribadi", "administrasi", "rumah tangga"])) {
    return {
      routedTo: "Life Records",
      destinationDb: "Life Records (pending final routing)",
      reason: "Rule-based initial route: finance, household, personal record, asset, life admin, or personal administration related capture.",
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

  if (hasAny(["tags", "tag", "label", "label lintas database", "lintas database", "kategori lintas database", "taxonomy", "taksonomi"])) {
    return {
      routedTo: "Tags",
      destinationDb: "Tags (pending final routing)",
      reason: "Rule-based initial route: tag, label, taxonomy, or cross-database category related capture.",
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
  async fetch(request: Request, env: any, ctx: ExecutionContext): Promise<Response> {
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

      if (!chatId || !rawText.trim()) { // Line 351: rawText validation starts
        return json({ ok: true, ignored: true, reason: "No text message found" });
      }
        if (["/status", "/system_status", "/system-status"].includes(rawText.trim().split(/\s+/)[0].split("@")[0].toLowerCase())) { // Line 354: /status handler starts
          await sendTelegram(env, chatId, `🟢 Bubu System Status
Phase: 3B — System Status Command MVP
Worker: online
Role: capture-by-default
Auto Merge: enabled
Recent Captures routing: Phase 3A passed (validation confirmed).
Limitations: In-memory auto-merge buffer (volatile).

Source SHA16: 246e4aeeef349b86
Checkpoint Path: /home/egitaristorandas/.openclaw/workspace/checkpoints/bubu-system-status-command-20260501-LIVE`);
          return json({ ok: true, command: "system-status", captured: false });
        }


        const userId = getAutoMergeUserId(message); // Line 359: autoMergeBuffers logic starts
        const bufferKey = getAutoMergeBufferKey(chatId, userId);
        const hasExistingBuffer = autoMergeBuffers.has(bufferKey);
        const isCaptureTrigger = isAutoMergeCaptureTrigger(rawText);

        try {
          if (hasExistingBuffer && isCaptureTrigger) {
            await flushAutoMergeBuffer(env, ctx, chatId, userId, "new-capture-trigger");
          }

          if (hasExistingBuffer && !isCaptureTrigger) {
            const appended = appendAutoMergeBuffer(env, ctx, chatId, userId, rawText);

            return json({
              ok: true,
              captured: false,
              buffering: appended,
              auto_merge: true,
              reason: appended ? "message appended to active buffer" : "buffer missing or flushing",
            });
          }

          await startAutoMergeBuffer(env, ctx, chatId, userId, rawText);

          return json({
            ok: true,
            captured: false,
            buffering: true,
            auto_merge: true,
            reason: isCaptureTrigger ? "capture trigger detected" : "default capture buffering",
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
