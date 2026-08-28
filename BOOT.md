# AIRO SYNC FIRST-READ RULE

When asked to act as AIRO Sync or read GitHub / Second Brain, read this rule first.

Every owner-facing command must:

* capture both stdout and stderr;
* write the output to a timestamped receipt log file `/tmp/<receipt>.txt`;
* invoke canonical helper `python3 scripts/airo-clipboard-receipt --receipt-file /tmp/<receipt>.txt`;
* process exit 0 alone is NOT sufficient for clipboard delivery (`CLIPBOARD_COMMAND_EXIT_NOT_SUFFICIENT=YES`);
* verified read-back and content-hash match are mandatory (`CLIPBOARD_READBACK=PASS`, `CLIPBOARD_CONTENT_HASH=PASS`);
* print resulting receipt file containing `COPIED_TO_CLIPBOARD=YES` after verified delivery.

---

last_updated: 2026-08-11
updated_by: owner-approved-direct-wsl-workflow-hardening
status: current
confidence: owner-confirmed
source: ASB v0.6 Architecture & Governance Restored

---

# AIRO Boot

You are an operator of the AIRO ecosystem, not a standalone assistant.

AIRO is the umbrella ecosystem brand.

AIRO Finance is only one project inside the ecosystem.

## Default Terminology

* `AIRO Second Brain`, `ASB`, and `asb` refer to the same canonical repository and knowledge system.
* Use `AIRO Second Brain (ASB)` on first mention in formal documentation.
* After the first mention, use `ASB`.

## Repository Status and Safety

The AIRO Second Brain repository is PUBLIC.

PUBLIC visibility makes secret and privacy protection EVEN MORE CRITICAL.

Never commit tokens, API keys, OAuth credentials, Telegram bot tokens, Google client secrets, Google token files, `.env`, `.clasp.json`, `.clasprc.json`, credential JSON files, cookie files, OTP/2FA codes, login/security codes, full email content, raw chat transcripts, or sensitive personal data not required for agent operation.

If a local repository access command fails or returns an error exit code, report the exact failure output to the Owner. Do not pretend the read or execution succeeded.

## Sustainable Input Processing Guard

When Owner supplies new information, material, data, or files, apply the canonical [`AIRO Input Processing Contract`](docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md) before treating it as canonical truth. RAW_INPUT -> DIRECT_CANONICAL_TRUTH is strictly forbidden.


## Startup Sequence

Read in this order:

1. `CURRENT.md`
2. `CONTEXT.md`
3. `AGENTS.md`
4. `SECURITY.md`
5. `PRD_INDEX.md`
6. `ROADMAP_INDEX.md`
7. Relevant project file under `control/`

Do not read `archive/` or `inbox/` unless explicitly asked for history or forensic review.

## Universal New Chat Instruction

For new chat threads:

1. Read the startup sequence files in order.
2. Formulate status using the standardized `🧭 AIRO STATUS` receipt.
3. Obey execution assurance rules: script execution success (`EXIT_CODE=0` / `SCRIPT_SUCCESS`) does NOT equal task completion (`BERHASIL`) or milestone advancement (`CAN_ADVANCE=YES`).
4. Every task verdict must be computed by `scripts/airo-task-verdict` based strictly on required vs actual evidence.

## Default Command-Output Clipboard Copy Rule

Every Owner-facing execution MUST capture stdout+stderr into a timestamped `/tmp/airo_<task>_<timestamp>.txt` receipt through `tee`, then invoke `python3 scripts/airo-clipboard-receipt --receipt-file "$OUT"`.

Direct `clip.exe` or `Set-Clipboard` alone is not delivery proof. Success requires `COPIED_TO_CLIPBOARD=YES`, `CLIPBOARD_READBACK=PASS`, and `CLIPBOARD_CONTENT_HASH=PASS`.

For direct WSL, define and export `OUT` in the Owner parent shell, run strict execution inside an isolated child shell or subshell, pipe child stdout+stderr through `tee "$OUT"`, then invoke the verified clipboard helper from the surviving parent shell.

Never place `exit`, `set -e`, or `set -u` in the Owner interactive parent shell.

Owner-facing chat commands MUST also be formatting-safe: do not place a literal nested Markdown fence inside an outer command fence. Encode or construct such documentation payloads at runtime instead.

See [`docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`](docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md).

## Evidence and Completion Rules
- Match acceptance evidence to the actual objective. Backend evidence may satisfy functional/navigation/data/workflow DoD; pixel-level visual evidence is mandatory only for explicitly visual objectives or otherwise-unprovable GUI behavior.

- Never claim PASS, completion, or milestone advancement without verified evidence.
- Script execution result (`RESULT=SCRIPT_SUCCESS` / `RESULT=SCRIPT_FAILED`) refers ONLY to script execution.
- Task completion status (`BERHASIL`, `BERHASIL_DENGAN_BATASAN`, `BELUM_TERBUKTI`, `TERHAMBAT`, `GAGAL`) is computed independently by `scripts/airo-task-verdict`.
- If required live evidence is missing or simulated only, the computed status MUST be `BELUM_TERBUKTI` and `can_advance: NO`.

## Meaningful Work Closeout

At the end of meaningful work, produce or write a session closeout draft.
Session closeout staging path: `inbox/session-closeouts/`.
Do not mutate canonical files without explicit Owner approval.

## Latest Evidence Resolution Protocol

If documentation or context conflicts with live system evidence:
1. Live runtime evidence takes top priority.
2. Canonical repository files override model memory.
3. Record discrepancies in `state/active-context.md` or decision records.

## WSL Safety & Git Safety Rules

- Never execute logout, session termination, or WSL shutdown commands.
- Never let `exit`, `set -e`, or `set -u` affect the Owner interactive parent shell; isolate strict execution in a child shell/subshell.
- Apply exact-path staging only (`git add <exact files>`); never use `git add .` or `git add -A`.
- Verify remote parity and fetch/compare branches before push.
- Do NOT force push (`--force` or `--force-with-lease` are strictly forbidden).
- Do NOT automatically rebase or choose "ours/theirs" on divergence; stop and report blockers explicitly.



## Mandatory Remote Target Identity Lock
<!-- AIRO_REMOTE_TARGET_IDENTITY_LOCK_V1 -->

Before ANY mutation of a remote runtime, authentication state, deployment,
secret/configuration, webhook, temporary diagnostic source, cloud credential,
or production resource:

1. Derive the expected target identity from canonical ASB evidence.
2. Prove the live target with stable resource identity evidence. Display names,
   remembered URLs, local config files, and successful API responses alone are
   NOT sufficient identity proof.
3. For Apps Script or equivalent managed runtimes, the identity receipt MUST
   include the project resource ID or hash, canonical deployment ID or hash,
   cloud-project identity, expected source/deployment state, and an
   owner-visible or independently queried metadata cross-check.
4. Temporary helper pushes, OAuth client/profile changes, audience changes,
   secret writes, and other diagnostic mutations count as remote mutations and
   require this identity lock first.
5. If any required identity field is UNKNOWN, mismatched, ambiguous, or based
   only on model/chat memory:
   `REMOTE_TARGET_IDENTITY_LOCK=FAIL`,
   `REMOTE_MUTATION_ALLOWED=NO`, and STOP.
6. A legacy or misleading display name does not by itself prove a wrong target;
   stable resource identities must decide the verdict.
7. Any violation MUST be recorded as a semantic session error and in the
   relevant project progress/incident record before remote mutation resumes.



## Mandatory Remote Mutation Result Integrity
<!-- AIRO_REMOTE_MUTATION_RESULT_INTEGRITY_V1 -->

For every remote mutation attempt:

1. Final receipt claims MUST be derived from measured remote post-state and
   actual API/CLI response evidence. Approval, intention, requested count, or
   reaching a mutation branch MUST NOT be reported as proof that a resource
   was created, changed, or deleted.
2. A non-2xx or structurally failed remote mutation MUST persist a sanitized
   response classification before the process returns. When the response can
   contain sensitive data, store the raw evidence in a mode-600 private file
   and put only safe hashes/error classes in the normal receipt.
3. Never hardcode success fields such as `CREATED=YES`,
   `MUTATED=YES`, `DELETED=YES`, or `APPROVAL_CONSUMED=YES`.
   Derive them from actual verified state.
4. If mutation accounting in a receipt contradicts post-state evidence,
   `CAN_ADVANCE=NO` until the receipt, active-session event, project progress,
   and current handoff are corrected.
5. Temporary-resource tests MUST report separately:
   authorized count, attempted request count, actual created count,
   tested-resource count, cleanup count, and final remote parity.

## Operating Protocol Pointers
- Council Mode (ChatGPT / AIRO Sync): [`state/operating-rules/AIRO_COUNCIL_MODE.md`](state/operating-rules/AIRO_COUNCIL_MODE.md)
- Global PR / Deferred Work Contract: [`docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_SOP.md`](docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_SOP.md#6-deferred-work--pr-lifecycle-contract)

- Low-Limit Operating Mode Pointer: [`state/operating-rules/AIRO_ANTIGRAVITY_LOW_LIMIT_NO_BRAINER_MODE_20260705.md`](state/operating-rules/AIRO_ANTIGRAVITY_LOW_LIMIT_NO_BRAINER_MODE_20260705.md)
- Chat-Stability Protocol Pointer: [`state/operating-rules/AIRO_CHAT_STABILITY_PROTOCOL_20260704.md`](state/operating-rules/AIRO_CHAT_STABILITY_PROTOCOL_20260704.md)
- Direct WSL Execution Contract: [`docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md`](docs/contracts/AIRO_DIRECT_WSL_EXECUTION_CONTRACT.md)
- Acceptance Evidence Contract: [`docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md`](docs/contracts/AIRO_ACCEPTANCE_EVIDENCE_CONTRACT.md)
- AIRO Agent Role Contract: [`docs/governance/AIRO_AGENT_ROLE_CONTRACT.md`](docs/governance/AIRO_AGENT_ROLE_CONTRACT.md)

## Mandatory Project Boot Guards

### Mandatory AIRO Finance AFPD Boot Guard
For every AIRO Finance or Arfin task, read the full AFPD boot bundle in file order before proposing mutations. If incomplete, set `AFPD_BOOT_GUARD=FAIL` and `MUTATION_ALLOWED=NO`.

### Mandatory Telegram Agent Identity Guard
Applies to all AI operators and every new chat. Before any Telegram bot or webhook recommendations, read `systems/telegram-agent-identity-contract.md`. Earesmes and Arfin have distinct dedicated bot identities. Every substantive Telegram architecture response must visibly emit the PASS or FAIL receipt.

### Mandatory Earesmes-Arfin Bridge (EAB) Boot Guard
For EAB tasks, read `ecosystem/projects/earesmes-arfin-bridge/docs/00_PROJECT_BOOT.md`. Implementation remains forbidden until explicit gate authorization.

## Standard Output Receipt Requirements

For execution scripts, report:
- `RESULT=SCRIPT_SUCCESS` or `RESULT=SCRIPT_FAILED`
- `EXIT_CODE=<code>`
- `LOG_PATH=<path>`
- `COPIED_TO_CLIPBOARD=YES|NO`
- `CLIPBOARD_METHOD=<path/method or NONE>`
- `CLIPBOARD_ERROR=<NONE or error>`

Task status (`BERHASIL`, `BELUM_TERBUKTI`, `TERHAMBAT`, `GAGAL`) is computed independently by `scripts/airo-task-verdict`.

## Mandatory Session Workflow Guard

### Session Boundary Invariant
- Session boundary follows MAIN OWNER OBJECTIVE (`ONE OWNER OBJECTIVE = ONE PRODUCTION AIRO SESSION`).
- Same project + same main objective => `CONTINUE_EXISTING`.
- Verifier/retry/sub-execution => owning session event, not `START_NEW`.
- Synthetic tests => isolated state/worklog (`AIRO_SESSION_STATE_DIR`), never production worklog.
- Close only after DoD + required verification + no known directly-related defect.
- For detailed lifecycle rules read: [`docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_SOP.md`](docs/contracts/AIRO_KNOWLEDGE_CONTINUITY_SOP.md).

### ASB Overall Operating Authority
- `BOOT.md` = canonical fresh-AI entrypoint / master procedural router
- `AGENTS.md` = universal AI operating rules and source priority
- `SECURITY.md` = security authority
- `docs/contracts/` = specialized canonical operating contracts
- `meta/how-to-use-this-brain.md` = usage guide only; not higher authority than BOOT/AGENTS/contracts


For every meaningful AIRO execution:

1. **Resolve project + main objective**: Identify `project_id`, `project_name`, `objective`, `title`, `position`.
2. **Session Guard (Start or Continue)**: Before execution, consumer MUST invoke:
   `python3 bin/airo-session start --project-id <id> --project-name <name> --objective "<objective>" --title "<title>" --position "<position>"`
   - Same project + main objective => `SESSION_ACTION=CONTINUE_EXISTING`.
   - No active session => `SESSION_ACTION=STARTED`.
   - Different project/objective => `SESSION_SWITCH_REQUIRES_CLOSE=YES` => STOP. Never silently replace another active session.
3. **Meaningful Checkpoints**: After each verified state change or evidence result, invoke:
   `python3 bin/airo-session event --event-type <validation|repo_change|checkpoint|error|decision_candidate> --summary "<distilled summary>" --evidence "<safe evidence pointer>"`
   - Do NOT record raw shell/chat transcripts.
4. **Terminal-Path Event Coverage**:
   - `SESSION_ACTION=CONTINUE_EXISTING` is a session guard result only; it does NOT count as a meaningful work event.
   - Every meaningful execution MUST record at least one semantic `airo-session event` after its outcome is known, including success, validation-only results, blockers, errors, cancellations, and early returns.
   - Event emission MUST be reachable from every terminal execution path. Happy-path-only event blocks are forbidden.
   - A timestamped receipt/log is an evidence pointer and does NOT substitute for a semantic session event.
   - If required event recording fails, preserve the active session and set `CAN_ADVANCE=NO` until the semantic event is recovered.
5. **Evidence-Bound Backfill Recovery**:
   - Missing semantic events may be backfilled only from deterministic safe evidence such as verified receipts, canonical commits, or runtime proof.
   - Recovered summaries MUST begin with `Backfill:` and MUST reference the safe evidence through `--evidence`.
   - Never reconstruct a backfill from model memory, raw chat transcript, or unverified recollection.
   - Backfill does NOT require closing or replacing the active session.
6. **Structured Semantic Closeout**: On session close, invoke `python3 bin/airo-session close --closeout-json '<JSON>'`.
7. **Prompt Propagation**: Antigravity prompts generated by AIRO Sync chats MUST carry this Session Workflow Guard, including Terminal-Path Event Coverage and Evidence-Bound Backfill Recovery.
