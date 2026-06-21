# AIRO New Chat Bootstrap Template

Copy this into a new ChatGPT chat:

Lanjut project Airo Personal Workflow.

Source of truth:
- GitHub repo: progamer6918/vortex-ai-skill-lab
- Branch: main
- Repo URL: https://github.com/progamer6918/vortex-ai-skill-lab.git
- Local repo dir default: ~/vortex-ai-skill-lab
- Read first: docs/personal-workflow/AIRO_PROJECT_INDEX.md
- Then read chat rules: docs/personal-workflow/AIRO_CHAT_RULES.md
- Then read continuity pack: docs/personal-workflow/AIRO_CONTINUITY_PACK.md
- Then read bootstrap template: docs/personal-workflow/AIRO_NEW_CHAT_BOOTSTRAP_TEMPLATE.md
- Then read latest handoff: docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_7_HANDOFF.md
- Then read current roadmap: docs/personal-workflow/phase-8/AIRO_PHASE_8_ROADMAP.md
- Then read latest completed Phase 8 docs:
  - docs/personal-workflow/phase-8/AIRO_PHASE_8A_FINAL_SYSTEM_AUDIT.md
  - docs/personal-workflow/phase-8/AIRO_PHASE_8B_BACKUP_RESTORE_GUIDE.md
  - docs/personal-workflow/phase-8/AIRO_PHASE_8C_FINAL_SMOKE_TEST_SUITE.md

Current stable checkpoint:
- MVP v0.1: DONE
- Phase 2: DONE
- Phase 3: DONE
- Phase 4: DONE
- Phase 5: DONE
- Phase 6: DONE
- Phase 7: DONE
- Phase 8: DONE
- Airo Personal Workflow current scope: COMPLETE

Final project status:
- Phase 8A Final System Audit: DONE
- Phase 8B Backup and Restore Guide: DONE
- Phase 8C Final Smoke Test Suite: DONE
- Phase 8D Final Source-of-Truth Refresh: DONE
- Phase 8E Final Handoff and Stable Release Tag: DONE
- Final release tag: airo-personal-workflow-phase-8-complete
- Final handoff: docs/personal-workflow/handoff/AIRO_PERSONAL_WORKFLOW_PHASE_8_HANDOFF.md
- Do not create Phase 9 unless the user explicitly expands the project scope.

Rules:
- Read Telegram gateway discovery notes before patching runtime: docs/personal-workflow/integration/AIRO_TELEGRAM_GATEWAY_DISCOVERY_NOTES.md
- Read Telegram Option A single-front-door plan before Telegram/Notion/OpenClaw changes: docs/personal-workflow/integration/AIRO_TELEGRAM_OPTION_A_SINGLE_FRONT_DOOR_PLAN.md
- Read integration collision guardrail before Telegram/Notion/OpenClaw changes: docs/personal-workflow/integration/AIRO_TELEGRAM_NOTION_OPENCLAW_COLLISION_GUARDRAIL.md
- Show Context meter in important responses.
- Do not put command fragments outside the code block.
- Put the entire command in one fenced bash code block and start it with bash -lc.
- Never assume the terminal is already inside the repo; clone/cd via the repo bootstrap rule first.
- Follow docs/personal-workflow/AIRO_CHAT_RULES.md before giving repo commands.
- Do not invent phases.
- Do not add extra sub-phases.
- If Phase 8 roadmap does not exist, create official Phase 8 roadmap first.
- Use one paste-safe command per milestone.
- Smoke test before commit.
- Commit and push after PASS.
- Keep GitHub as source of truth.
- Update docs, handoff, and index when relevant.
- Do not touch EarnsAI trading runtime unless explicitly requested.
- Do not enable live trading.
- Do not read secrets, tokens, cookies, sessions, passwords, .env files, or browser profiles.
- Do not commit local DBs, receipts, OAuth tokens, or credentials.
- Do not patch OpenClaw core or restart OpenClaw service without explicit approval.
- Real Google writes must go through approval gate.

Important commands:
- python3 scripts/personal-workflow/airo_final_smoke.py --text
- python3 scripts/personal-workflow/airo_final_smoke.py --json
- ./bin/airo-daily --text
- python3 scripts/personal-workflow/airo_intent_router.py "<message>"
- python3 scripts/personal-workflow/airo_approval_review.py list --status pending --compact
- python3 scripts/personal-workflow/airo_executor_recommend.py list-actionable --limit 10
- ./bin/airo-dashboard-align
