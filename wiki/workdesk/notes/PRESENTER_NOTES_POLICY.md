---
type: workdesk-contract
project: AIRO_WORKDESK
workdesk_status: ACTIVE
audience: human-ai
---
# Presenter / Notion Notes Policy

Notion export is useful for presenter explanation, examples and context, but its pipeline can be:

`presenter → audio → speech-to-text → optional AI cleanup/summary → Notion`

Therefore notes are not a single authority class.

## Labels

- `CORROBORATED` — matches stronger formal/current source.
- `PLAUSIBLE_CONTEXT` — useful context, no contradiction, but not enough for a hard rule.
- `TRANSCRIPTION_RISK` — wording/acronym/number looks corrupted or ambiguous.
- `AI_DERIVED_SUMMARY` — text has been transformed/summarized by AI.
- `OWNER_APPLIED_NOTE` — Owner work/project thought, not necessarily formal rule.
- `OUT_OF_SCOPE` — unrelated to WorkDesk.
- `SECRET_EXCLUDED` — credentials/auth/sensitive secret; never ingest into public knowledge.

## Canonicalization rule

If a Notion note conflicts with formal material, formal material wins unless a stronger current source proves an update.

Do not “repair” strange transcription by guessing. Record uncertainty or find corroborating source.

## Known examples

- `WD-SRC-097` Reshape note contains obvious semantic/transcription anomalies and must not be used to define Reshape without corroboration from `WD-SRC-073` / current sources.
- `WD-SRC-078` and `WD-SRC-098` are secret-excluded.
