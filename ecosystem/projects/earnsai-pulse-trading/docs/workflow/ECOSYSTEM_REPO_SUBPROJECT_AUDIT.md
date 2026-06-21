# Ecosystem Repo and Subproject Audit

## Result
This audit maps EarnsAI local folders before any additional GitHub handover.
No subproject is pushed by this issue.

## Audit Scope
- ~/earnsai-pulse-trading
- ~/earnsai-telegram-gateway
- ~/earnsai-telegram-gateway/trading-research-lab
- ~/earnsai-telegram-gateway/trading-research-lab/agent_os
- ~/.openclaw/workspace
- ~/AI_AGENT_WORKSPACE

## Safety Rule
This audit checks structure, git status, and risk indicators without printing secret values.

## Folder Existence
- EXISTS: /home/egitaristorandas/earnsai-pulse-trading
- EXISTS: /home/egitaristorandas/earnsai-telegram-gateway
- EXISTS: /home/egitaristorandas/earnsai-telegram-gateway/trading-research-lab
- EXISTS: /home/egitaristorandas/earnsai-telegram-gateway/trading-research-lab/agent_os
- EXISTS: /home/egitaristorandas/.openclaw/workspace
- EXISTS: /home/egitaristorandas/AI_AGENT_WORKSPACE

## Git Repository Status
- /home/egitaristorandas/earnsai-pulse-trading: git_repo=yes branch=local-issue-workflow remote_lines=2 status_lines=2
- /home/egitaristorandas/earnsai-telegram-gateway: git_repo=yes branch=master remote_lines=0 status_lines=85
- /home/egitaristorandas/earnsai-telegram-gateway/trading-research-lab: git_repo=yes branch=master remote_lines=0 status_lines=77

## Risk Indicator Counts
- /home/egitaristorandas/earnsai-telegram-gateway: files_depth3=1831 gitignore_files=2 risk_name_matches=32
- /home/egitaristorandas/earnsai-telegram-gateway/trading-research-lab: files_depth3=1803 gitignore_files=1 risk_name_matches=28
- /home/egitaristorandas/.openclaw/workspace: files_depth3=140 gitignore_files=0 risk_name_matches=1
- /home/egitaristorandas/AI_AGENT_WORKSPACE: files_depth3=67 gitignore_files=0 risk_name_matches=3

## Preliminary Classification
- ~/earnsai-pulse-trading: already handed over to GitHub as the primary PAPER_ONLY trading repo.
- ~/earnsai-telegram-gateway: candidate separate repo, requires cleanup before push.
- ~/earnsai-telegram-gateway/trading-research-lab: candidate separate repo or isolated research subproject, requires cleanup before push.
- trading-research-lab/agent_os: Notion Agent OS area, must remain guarded and separate from trading execution.
- ~/.openclaw/workspace: local-only workspace, do not push directly.
- ~/AI_AGENT_WORKSPACE: local-only workspace, do not push directly.

## Next Recommendation
Prepare the next issue only after reviewing this audit report. Do not push additional subprojects until risk indicators are resolved.
