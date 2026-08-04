last_updated: 2026-08-04
updated_by: owner-approved-v06-architecture-correction
status: current
confidence: owner-confirmed
source: ASB v0.6 Architecture & Governance Restored

# AIRO Security Policy

## Repository Visibility
The AIRO Second Brain repository is PUBLIC.

PUBLIC visibility makes secret and privacy protection EVEN MORE CRITICAL. Never commit secrets, credentials, or private personal data.

## What Must Never Be Committed

Never commit tokens, API keys, OAuth credentials, Telegram bot tokens, Google client secrets, Google token files, `.env`, `.clasp.json`, `.clasprc.json`, credential JSON files, cookie files, OTP/2FA codes, login/security codes, full email content, raw chat transcripts, or sensitive personal data not required for agent operation.

## Google Workspace & Credentials

Google Workspace integration may exist in local environments.

Rules:
- Do not inspect credential/token files.
- Do not print credential/token file contents.
- Do not copy credential/token files into this repo.
- Do not summarize secret contents.
- Do not store full email bodies.
- Do not forward OTP/security email contents.
- Do not mutate Gmail unless the relevant project explicitly approves it.

## Local Paths

Local paths may be documented only as non-secret operational references.

Do not document credential file contents.

If a local credential/token path is found, refer to it generically:
> Local credential/token files may exist in local agent config paths. Do not inspect, print, log, copy, or commit them.

## Allowed vs Forbidden Public Content

- **Allowed Content**: Operating principles, project summaries, canonical pointers, safe worklogs, decision logs, non-sensitive architecture specifications, and public-safe contracts.
- **Forbidden Content**: Secrets, API tokens, raw private transcripts, sensitive email content, auth artifacts, and Owner private personal data not needed for agent work.
