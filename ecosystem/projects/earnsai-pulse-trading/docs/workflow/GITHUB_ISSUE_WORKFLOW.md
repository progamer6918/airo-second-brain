
EarnsAI GitHub Issue Workflow

Current stage: local-first issue workflow.

GitHub will later become the online project workbook, but for now tasks are stored locally in tasks/.

Workflow:

Pick or create one issue.
Keep changes inside scope.
Run validation commands.
Commit only when acceptance criteria pass.
Move issue to done after completion.

Project boundary:

Pulse Trading stays PAPER_ONLY.
Telegram Gateway Notion must not touch trading runtime.
Notion work must not print token or delete/bulk update.
OpenClaw/Airo needs inventory first before patching.
