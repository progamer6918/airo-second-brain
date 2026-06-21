const NOTION_VERSION = "2022-06-28";

export type InitialRouteLike = {
  routedTo: string;
  destinationDb: string;
  reason: string;
};

type FinalRouteConfig = {
  envKey: string;
  destinationDb: string;
};

const FINAL_ROUTE_CONFIG: Record<string, FinalRouteConfig> = {
  Inbox: { envKey: "INBOX_DB_ID", destinationDb: "Inbox" },
  Notes: { envKey: "NOTES_DB_ID", destinationDb: "Notes" },
  Tasks: { envKey: "TASKS_DB_ID", destinationDb: "Tasks" },
  Sources: { envKey: "SOURCES_DB_ID", destinationDb: "Sources / Daftar Pustaka" },
  "Top of Mind": { envKey: "TOP_OF_MIND_DB_ID", destinationDb: "Top of Mind" },
  "Work Hub": { envKey: "WORK_HUB_DB_ID", destinationDb: "Work Hub" },
  "Career & Portfolio": { envKey: "CAREER_PORTFOLIO_DB_ID", destinationDb: "Career & Portfolio" },
  "Growth Lab": { envKey: "GROWTH_LAB_DB_ID", destinationDb: "Growth Lab" },
  "Life Records": { envKey: "LIFE_RECORDS_DB_ID", destinationDb: "Life Records" },
  "EarnsAI Dev Lab": { envKey: "EARNSAI_DEV_LAB_DB_ID", destinationDb: "EarnsAI Dev Lab" },
  "AI System Log": { envKey: "AI_SYSTEM_LOG_DB_ID", destinationDb: "AI System Log" },
  "Weekly Digest": { envKey: "WEEKLY_DIGEST_DB_ID", destinationDb: "Weekly Digest" },
};

const DEFERRED_ROUTES = new Set(["Projects", "Areas", "Tags"]);

function splitText(text: string, size = 1900) {
  const parts: string[] = [];
  for (let i = 0; i < text.length; i += size) {
    parts.push(text.slice(i, i + size));
  }
  return parts.length ? parts : [""];
}

function headers(env: any) {
  return {
    Authorization: `Bearer ${env.NOTION_TOKEN}`,
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
  };
}

async function notion(env: any, path: string, init: RequestInit = {}) {
  const res = await fetch(`https://api.notion.com/v1${path}`, {
    ...init,
    headers: {
      ...headers(env),
      ...((init.headers as Record<string, string>) || {}),
    },
  });

  const data: any = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(JSON.stringify(data));
  return data;
}

async function getDbProperties(env: any, databaseId: string) {
  const db: any = await notion(env, `/databases/${databaseId}`, { method: "GET" });
  return db.properties || {};
}

function findTitleProperty(properties: Record<string, any>) {
  for (const [name, prop] of Object.entries(properties)) {
    if ((prop as any).type === "title") return name;
  }
  throw new Error("Destination database has no title property");
}

function maybeTextValue(prop: any, value: string) {
  const text = String(value || "").slice(0, 1900);
  if (!prop) return null;
  if (prop.type === "rich_text") return { rich_text: [{ text: { content: text } }] };
  if (prop.type === "url") return { url: text || null };
  return null;
}

function setIfSupported(
  out: Record<string, any>,
  props: Record<string, any>,
  name: string,
  value: string
) {
  const next = maybeTextValue(props[name], value);
  if (next) out[name] = next;
}

function setSelectOrStatusIfSupported(
  out: Record<string, any>,
  props: Record<string, any>,
  name: string,
  value: string
) {
  const prop = props[name];
  if (!prop) return;
  if (prop.type === "select") out[name] = { select: { name: value } };
  if (prop.type === "status") out[name] = { status: { name: value } };
}

async function createFinalPage(
  env: any,
  rawText: string,
  route: InitialRouteLike,
  config: FinalRouteConfig,
  recentUrl: string
) {
  const databaseId = env[config.envKey];
  if (!databaseId) throw new Error(`${config.envKey} is not configured`);

  const props = await getDbProperties(env, databaseId);
  const titleName = findTitleProperty(props);
  const title = rawText.slice(0, 80) || "Telegram Capture";

  const rawBlocks = splitText(rawText).map((part) => ({
    object: "block",
    type: "paragraph",
    paragraph: {
      rich_text: [{ type: "text", text: { content: part } }],
    },
  }));

  return notion(env, "/pages", {
    method: "POST",
    body: JSON.stringify({
      parent: { database_id: databaseId },
      properties: {
        [titleName]: { title: [{ text: { content: title } }] },
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
        {
          object: "block",
          type: "paragraph",
          paragraph: {
            rich_text: [{
              type: "text",
              text: {
                content: `Source: Telegram\nInitial Route: ${route.routedTo}\nRecent Capture: ${recentUrl}`,
              },
            }],
          },
        },
      ],
    }),
  });
}

async function updateRecentAudit(
  env: any,
  pageId: string,
  route: InitialRouteLike,
  destinationDb: string,
  destinationUrl: string,
  note: string
) {
  const props = await getDbProperties(env, env.RECENT_CAPTURES_DB_ID);
  const patch: Record<string, any> = {};

  setIfSupported(patch, props, "Destination DB", destinationDb);
  setIfSupported(patch, props, "Destination URL", destinationUrl);
  setIfSupported(patch, props, "Reason", `${route.reason}\n${note}`);
  if (destinationUrl) {
    setSelectOrStatusIfSupported(patch, props, "Status", "Routed");
  }

  if (!Object.keys(patch).length) return;

  await notion(env, `/pages/${pageId}`, {
    method: "PATCH",
    body: JSON.stringify({ properties: patch }),
  });
}

export async function runFinalRouting(
  env: any,
  rawText: string,
  initialRoute: InitialRouteLike,
  recentCapturePageId: string,
  recentCaptureUrl: string
) {
  const config = FINAL_ROUTE_CONFIG[initialRoute.routedTo];

  if (!config) {
    const note = DEFERRED_ROUTES.has(initialRoute.routedTo)
      ? `Final routing deferred: ${initialRoute.routedTo} database is intentionally not configured yet.`
      : `Final routing skipped: no config for ${initialRoute.routedTo}.`;

    await updateRecentAudit(env, recentCapturePageId, initialRoute, `${initialRoute.routedTo} (deferred)`, "", note);
    return { ok: true, skipped: true, reason: note };
  }

  const finalPage: any = await createFinalPage(env, rawText, initialRoute, config, recentCaptureUrl);

  await updateRecentAudit(
    env,
    recentCapturePageId,
    initialRoute,
    config.destinationDb,
    finalPage.url,
    `Final routing: created final page in ${config.destinationDb}.`
  );

  return { ok: true, skipped: false, url: finalPage.url };
}
