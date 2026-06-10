last_updated: 2026-06-10
updated_by: owner-confirmed-design
status: current
confidence: owner-confirmed
source: chat-derived
AIRO Security Policy

This repo is private, but private does not mean safe for secrets.

Treat all content as internal. Never commit secrets or sensitive raw data.

What Must Never Be Committed

Never commit tokens, API keys, OAuth credentials, Telegram bot tokens, Google client secrets, Google token files, .env, .clasp.json, .clasprc.json, credential JSON files, cookie files, OTP/2FA codes, login/security codes, full email content, raw chat transcripts, or sensitive personal data not required for agent operation.

Google Workspace

Google Workspace integration may exist in local environments.

Rules:

Do not inspect credential/token files.
Do not print credential/token file contents.
Do not copy credential/token files into this repo.
Do not summarize secret contents.
Do not store full email bodies.
Do not forward OTP/security email contents.
Do not mutate Gmail unless the relevant project explicitly approves it.
Local Paths

Local paths may be documented only as non-secret operational references.

Do not document credential file contents.

If a local credential/token path is found, refer to it generically:

Local credential/token files may exist in local agent config paths.
Do not inspect, print, log, copy, or commit them.
Repo Visibility

This repo is private.

Allowed content: operating principles, project summaries, canonical pointers, safe worklogs, decision logs, and non-sensitive architecture notes.

Forbidden content: secrets, raw private transcripts, sensitive email content, auth artifacts, and owner private data not needed for agent work.
