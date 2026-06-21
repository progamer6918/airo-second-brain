type Env = {
  NOTION_TOKEN: string;
  RECENT_CAPTURES_DB_ID: string;
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/health") {
      return json({
        ok: true,
        service: "earnsai-telegram-gateway",
        phase: "notion-test"
      });
    }

    if (url.pathname === "/test-notion") {
      const rawNote =
        "RAW TEST dari Cloudflare Worker ke Notion Recent Captures.\n\nBaris 1 harus muncul.\nBaris 2 harus muncul.\nRaw note tidak boleh hilang.";

      const page = await createRecentCapture(env, rawNote);

      return json({
        ok: true,
        page_id: page.id,
        url: page.url
      });
    }

    return new Response("EarnsAI Telegram Gateway is alive.");
  }
};

async function createRecentCapture(env: Env, rawNote: string) {
  const payload = {
    parent: {
      database_id: env.RECENT_CAPTURES_DB_ID
    },
    properties: {
      "Capture": {
        title: [
          {
            text: {
              content: "WORKER TEST raw note preservation"
            }
          }
        ]
      }
    },
    children: [
      {
        object: "block",
        type: "heading_2",
        heading_2: {
          rich_text: [
            {
              type: "text",
              text: {
                content: "Raw Note"
              }
            }
          ]
        }
      },
      {
        object: "block",
        type: "paragraph",
        paragraph: {
          rich_text: [
            {
              type: "text",
              text: {
                content: rawNote
              }
            }
          ]
        }
      }
    ]
  };

  const res = await fetch("https://api.notion.com/v1/pages", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${env.NOTION_TOKEN}`,
      "Notion-Version": "2022-06-28",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  const data: any = await res.json();

  if (!res.ok) {
    return {
      id: "ERROR",
      url: JSON.stringify(data)
    };
  }

  return data;
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "Content-Type": "application/json"
    }
  });
}
