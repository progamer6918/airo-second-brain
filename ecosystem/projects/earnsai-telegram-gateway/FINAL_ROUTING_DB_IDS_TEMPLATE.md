# Final Routing Database IDs Template

Use this file to collect Notion final database IDs before adding them to Cloudflare Worker secrets.

Do not commit or share filled database IDs publicly.

| Route | Secret Name | Notion Database ID |
|---|---|---|
| Inbox | INBOX_DB_ID |  |
| Notes | NOTES_DB_ID |  |
| Tasks | TASKS_DB_ID |  |
| Sources / Daftar Pustaka | SOURCES_DB_ID |  |
| Projects | PROJECTS_DB_ID |  |
| Areas | AREAS_DB_ID |  |
| Top of Mind | TOP_OF_MIND_DB_ID |  |
| Work Hub | WORK_HUB_DB_ID |  |
| Career & Portfolio | CAREER_PORTFOLIO_DB_ID |  |
| Growth Lab | GROWTH_LAB_DB_ID |  |
| Life Records | LIFE_RECORDS_DB_ID |  |
| EarnsAI Dev Lab | EARNSAI_DEV_LAB_DB_ID |  |
| AI System Log | AI_SYSTEM_LOG_DB_ID |  |
| Weekly Digest | WEEKLY_DIGEST_DB_ID |  |
| Tags | TAGS_DB_ID |  |

Next:
- Fill database IDs manually from Notion.
- Add each one using wrangler secret put.
- Verify with npx wrangler secret list.
