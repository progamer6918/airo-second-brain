# AIRO SECOND BRAIN PRD v0.4.1

## No-Brainer Execution Edition

**Local-First Workspace Governance, Sync, Truth Resolution, and Knowledge Lifecycle Layer**

---

## 0. Document Status

**Status:** Approved baseline for execution
**Previous baseline:** AIRO Second Brain PRD v0.4
**This version:** v0.4.1 No-Brainer Execution Edition
**Purpose:** Make the PRD executable by Antigravity or any AI consumer with minimal interpretation.

This version does not change the architecture. It expands the PRD with:

* exact execution phases
* required files
* script contracts
* validation commands
* PASS/FAIL criteria
* safety rules
* failure recovery
* consumer-specific behavior
* commit and push policy

---

# 1. Problem & Goal

## 1.1 Problem

Owner uses multiple AI consumers:

* ChatGPT
* Claude
* Antigravity
* Earesmes / Hermes
* local WSL tools

Current pain points:

1. AI sessions lose context.
2. Progress can disappear if session breaks or limit ends.
3. AIRO Second Brain can become stale while project repos have changed.
4. Raw logs and closeouts can pile up and become garbage.
5. Different consumers may write to the wrong place.
6. Owner is forced to remember too much: push, closeout, context, state, repo status.
7. Earesmes has limited reasoning capacity and cannot be trusted with semantic decisions.
8. Existing WSL repos are scattered and not all known to Second Brain.
9. There is no guaranteed mechanism that project progress gets detected, recorded, pushed, and organized.

## 1.2 Goal

AIRO Second Brain v0.4.1 must become a local-first control layer that:

* detects all WSL workspaces
* checks whether its own memory is current or stale
* records safe operational events
* pushes safe updates to GitHub
* prevents secrets from being committed
* organizes raw information into a lifecycle
* produces distillation proposals
* gates canonical knowledge updates
* gives every AI consumer the same startup protocol
* tells the system when it is healthy, stale, dirty, degraded, or blocked

## 1.3 Core Principle

AIRO Second Brain is not only a memory repo.

It must know:

* what it knows
* what it does not know
* when it is stale
* when repo/live state must override memory
* when a consumer is not allowed to execute

## 1.4 Out of Scope for v0.4.1

Do not implement:

* browser extension
* full ChatGPT/Claude web auto-capture
* AIRO Gateway
* monorepo migration
* submodule migration
* semantic auto-promote
* visual dashboard UI
* full autonomous reasoning by Earesmes
* automatic editing of non-governed repos

---

# 2. Locked Architecture

## 2.1 Module Count Is Locked

There are exactly 9 core modules.

Do not add module 10 during v0.4.1.

Internal features such as lock, retry, secret guard, logging, and recovery belong inside existing modules.

## 2.2 The 9 Modules

| Module           | Purpose                                        | Automation Level            |
| ---------------- | ---------------------------------------------- | --------------------------- |
| `airo-inventory` | Detect WSL repos/folders and update registry   | automatic                   |
| `airo-bootstrap` | Standard session entry point for all consumers | semi-automatic              |
| `airo-preflight` | Check truth/staleness before execution         | automatic through bootstrap |
| `airo-capture`   | Write local event logs                         | automatic                   |
| `airo-sync`      | Commit/push safe changes to GitHub             | automatic                   |
| `airo-organize`  | Prevent Second Brain from becoming garbage     | automatic                   |
| `airo-distill`   | Convert raw/inbox into proposal knowledge      | semi-automatic              |
| `airo-promote`   | Promote proposal to canonical memory           | gated                       |
| `airo-health`    | Write system health report                     | automatic                   |

## 2.3 Automation Rule

Automatic:

* inventory
* preflight
* capture
* sync
* organize
* health

Semi-automatic:

* bootstrap
* distill

Gated:

* promote

## 2.4 Absolute Rule

Technical/objective updates may be automated.

Semantic decisions must not be automatically promoted to canonical knowledge.

---

# 3. Target Repository Paths

## 3.1 Main Second Brain Repo

```text
/home/egitaristorandas/AI_WORKSPACES/airo-second-brain
```

GitHub:

```text
https://github.com/progamer6918/airo-second-brain
```

## 3.2 Main Project Repo

```text
/home/egitaristorandas/vortex-ai-skill-lab
```

Project identity:

```text
AIRO Finance
```

## 3.3 Canonical PRD File

This PRD must be stored as Markdown:

```text
docs/AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md
```

Optional export:

```text
docs/exports/AIRO_Second_Brain_PRD_v0.4.1.docx
```

Markdown is the source of truth. DOCX is export only.

---

# 4. Workspace Governance

## 4.1 Principle

AIRO Second Brain does not physically absorb all repos in v0.4.1.

It governs them through:

* inventory
* registry
* preflight
* sync policy
* health status
* event capture
* distillation
* promotion gate

## 4.2 Repo Tiers

| Tier               | Meaning                      | Policy                                  |
| ------------------ | ---------------------------- | --------------------------------------- |
| `GOVERNED-BRAIN`   | AIRO Second Brain itself     | auto-sync allowed for safe paths        |
| `GOVERNED-GUARDED` | critical implementation repo | guarded commit/push only                |
| `OBSERVE-ONLY`     | known but not controlled     | scan metadata only                      |
| `UNKNOWN`          | detected but unidentified    | record path only, do not inspect deeply |

## 4.3 Default v0.4.1 Scope

### GOVERNED-BRAIN

```text
/home/egitaristorandas/AI_WORKSPACES/airo-second-brain
```

### GOVERNED-GUARDED

```text
/home/egitaristorandas/vortex-ai-skill-lab
```

### OBSERVE-ONLY

```text
/home/egitaristorandas/earnsai-pulse-trading
/home/egitaristorandas/earnsai-telegram-gateway
/home/egitaristorandas/katoolin3
/home/egitaristorandas/AI_AGENT_WORKSPACE
/home/egitaristorandas/vibe-coding
/home/egitaristorandas/finance-bot-alternatives
/home/egitaristorandas/github-handover
```

All other discovered folders default to `UNKNOWN`.

## 4.4 Registry Files

Create:

```text
registry/repos.yaml
registry/sync-policy.yaml
registry/capture-policy.yaml
registry/consumer-policy.yaml
```

## 4.5 Minimum `registry/repos.yaml` Entry

```yaml
id: airo-finance
name: AIRO Finance
local_path: /home/egitaristorandas/vortex-ai-skill-lab
remote: https://github.com/progamer6918/vortex-ai-skill-lab
tier: GOVERNED-GUARDED
brain_file: projects/airo-finance.md
source_of_truth:
  - docs/AIRO_FINANCE_CURRENT_STATE.md
  - docs/AIRO_FINANCE_PRD_LIVING.md
truth_status: unknown
last_known_commit: null
last_checked_at: null
last_synced_at: null
safe_to_execute: false
notes: Project repo remains source of implementation truth.
```

## 4.6 AIRO Manifest

Create in governed project repo:

```text
/home/egitaristorandas/vortex-ai-skill-lab/AIRO_MANIFEST.md
```

Minimum content:

```markdown
---
project_id: airo-finance
tier: GOVERNED-GUARDED
owner: progamer6918
brain_repo: /home/egitaristorandas/AI_WORKSPACES/airo-second-brain
brain_file: projects/airo-finance.md
---

# AIRO Finance Manifest

## Source of Truth

- docs/AIRO_FINANCE_CURRENT_STATE.md
- docs/AIRO_FINANCE_PRD_LIVING.md
- docs/airo-finance/records/

## Guarded Paths

- apps-script-prod-v2/
- scripts/personal-workflow/apps-script/
- docs/airo-finance/
- .clasp.json
- .clasprc.json
- any token/credential file

## Commit Policy

This repo is PROJECT-GUARDED.

Do not auto-commit source code unless:

- secret guard PASS
- task context exists
- diff is reviewed
- validation output exists or is explicitly skipped with reason
```

---

# 5. Truth Resolution Protocol

## 5.1 Hierarchy of Truth

When sources conflict, higher source wins.

| Rank | Source                    | Example                                                       |
| ---: | ------------------------- | ------------------------------------------------------------- |
|    1 | Live runtime evidence     | Apps Script deployment, workbook state, actual command output |
|    2 | Project repository state  | git HEAD, git status, canonical project docs                  |
|    3 | Second Brain registry     | `registry/repos.yaml`, sync policy, truth status              |
|    4 | Second Brain active state | `CURRENT.md`, `state/active-context.md`, `projects/*.md`      |
|    5 | Raw events / inbox        | `events/raw/`, `inbox/`                                       |
|    6 | Chat/model memory         | lowest priority                                               |

## 5.2 Staleness Rule

If project repo HEAD differs from `last_known_commit` in registry:

```text
truth_status = stale
```

If repo has uncommitted changes:

```text
truth_status = dirty
```

If push/pull conflict occurs:

```text
truth_status = conflict
```

If repo has never been checked:

```text
truth_status = unknown
```

If repo HEAD equals registry and repo is clean:

```text
truth_status = current
```

## 5.3 Consumer Obligation

No consumer may execute project work before bootstrap has run preflight.

Correct flow:

```text
session starts
→ airo-bootstrap
→ airo-health
→ airo-preflight
→ truth_status evaluated
→ consumer may execute only if safe_to_execute allows it
```

Consumer must not be responsible for remembering preflight. Bootstrap enforces it.

---

# 6. Knowledge Lifecycle

## 6.1 Lifecycle Flow

```text
capture
→ sync
→ organize
→ distill
→ promote
→ archive
```

## 6.2 Folder Meaning

| Level     | Folder                                                        | Meaning                                    |
| --------- | ------------------------------------------------------------- | ------------------------------------------ |
| Raw       | `events/raw/`                                                 | machine events, not knowledge              |
| Inbox     | `inbox/`                                                      | session closeouts, scans, checkpoints      |
| Proposal  | `distill/proposals/`                                          | AI-generated interpretation, not canonical |
| Canonical | `CURRENT.md`, `projects/*.md`, `decisions/*.md`, `state/*.md` | default memory                             |
| Archive   | `archive/`                                                    | old/superseded evidence                    |

## 6.3 Canonical Files

Canonical files include:

```text
BOOT.md
CURRENT.md
CONTEXT.md
AGENTS.md
SECURITY.md
state/active-context.md
state/system-health.md
projects/*.md
decisions/decision-log.md
decisions/pending-decisions.md
registry/*.yaml
```

## 6.4 Required Metadata

Every canonical project/state/decision file must include frontmatter:

```yaml
---
status: current | stale | draft | archived | superseded
confidence: repo-derived | owner-confirmed | provisional | unknown
last_updated: YYYY-MM-DDTHH:mm:ss+07:00
source: repo | owner | antigravity | chatgpt | claude | earesmes | system
---
```

## 6.5 Anti-Garbage Rule

Raw and inbox files must not become default context.

Consumers read raw/inbox only when investigating.

---

# 7. Consumer Protocol

## 7.1 ChatGPT / Claude Web

Can read:

```text
BOOT.md
CURRENT.md
CONTEXT.md
AGENTS.md
SECURITY.md
state/system-health.md
projects/<active>.md
decisions/pending-decisions.md
```

Can write:

```text
inbox/session-closeouts/
distill/proposals/
```

Cannot:

```text
promote canonical directly
claim repo access without evidence
rewrite CURRENT.md directly
mark DONE/PASS without runtime or repo evidence
```

Capture mode:

```text
manual checkpoint only in v0.4.1
```

## 7.2 Antigravity

Can read:

```text
all canonical files
actual repo files
registry
system health
project manifests
```

Can write:

```text
scripts/
registry/
events/
logs/
distill/proposals/
docs/
source code only when task requires it
```

Can promote:

```text
factual repo-derived updates only
```

If Antigravity promotes factual canonical update without owner review, it must add:

```yaml
promoted_by: antigravity
awaiting_owner_review: true
```

Cannot:

```text
promote semantic decisions without owner
change architecture without explicit approval
skip preflight
force push
commit secrets
```

## 7.3 Earesmes / Hermes

Can run:

```text
airo-bootstrap
airo-inventory
airo-health
airo-sync
airo-organize
airo-capture
```

Can notify:

```text
Telegram error summary
sync failure
secret guard hit
conflict detected
system degraded
```

Cannot:

```text
promote semantic canonical knowledge
rewrite CURRENT.md based on interpretation
make architecture decisions
approve proposals
decide task completion
```

Earesmes is executor, not brain.

## 7.4 Owner

Can:

```text
approve semantic decisions
override policy
promote canonical without awaiting-review
change repo tier
resolve conflicts
approve risky automation
```

Should not need to:

```text
classify every repo manually
remember every push
repeat context from zero
manually organize raw logs
```

## 7.5 Remote Session Without PC Access

If the session happens outside the main PC/WSL:

1. If no WSL command runs, local automation cannot see the session.
2. Use manual checkpoint.
3. Save output to `inbox/session-closeouts/` when PC access returns.
4. Do not assume real-time capture from ChatGPT/Claude web.
5. Full remote capture is deferred to v2 AIRO Gateway or browser bridge.

---

# 8. Safety Policy

## 8.1 Secret Guard Blocked Files

Block commit/push if diff includes:

```text
.env
.env.*
*.pem
*.key
*.token
*.secret
credentials*.json
token*.json
client_secret*.json
google_token*.json
.clasp.json
.clasprc.json
*oauth*
*credential*
.htpasswd
```

## 8.2 Secret Guard Blocked Content

Block commit/push if diff contains:

```text
ghp_
github_pat_
AIza
AKIA
-----BEGIN PRIVATE KEY-----
-----BEGIN RSA PRIVATE KEY-----
refresh_token
client_secret
bot_token
password
passwd
api_key
api_secret
```

## 8.3 Secret Guard Behavior

If hit:

```text
BLOCK commit
DO NOT push
log filename only, not content
write logs/sync-errors/<timestamp>-secret-guard.md
update state/system-health.md
notify via Earesmes if configured
```

## 8.4 Brain-Safe Paths

Allowed for aggressive auto-sync in `airo-second-brain`:

```text
events/
inbox/
logs/
registry/
state/
meta/
docs/
distill/proposals/
```

Still subject to secret guard.

## 8.5 Project-Guarded Paths

For `vortex-ai-skill-lab`, guarded paths include:

```text
apps-script-prod-v2/
scripts/
docs/airo-finance/
.clasp.json
.clasprc.json
credentials
tokens
```

Do not auto-commit source code unless:

```text
secret guard PASS
task context exists
commit message exists
diff summary generated
validation exists or skipped with reason
```

## 8.6 Locking

`airo-sync` must use:

```text
locks/airo-sync.lock
```

Rules:

```text
if lock exists and age < 10 minutes: skip
if lock exists and age >= 10 minutes: mark stale lock, remove, continue
always release lock in cleanup/finally
```

---

# 9. Failure Mode & Recovery

## 9.1 Sync Push Failure

If push fails:

```text
retry 3 times
write logs/sync-errors/<timestamp>-push-failed.md
do not delete raw events
update state/system-health.md
set safe_to_work=false only if conflict or repeated failure affects governed repo
```

## 9.2 Git Conflict

If conflict detected:

```text
STOP
do not force push
do not auto-resolve
set truth_status=conflict
write logs/sync-errors/<timestamp>-conflict.md
update state/system-health.md
notify owner/Earesmes if available
```

## 9.3 Secret Guard Hit

If secret detected:

```text
BLOCK commit
log filename only
do not log secret content
set affected repo status=blocked
update health
wait for owner/manual cleanup
```

## 9.4 Bootstrap Failure

If bootstrap fails:

```text
fallback to BOOT.md
mark system degraded
do not fully block consumer
consumer may only perform read-only investigation
```

## 9.5 PC Main Offline

If main PC is off:

```text
no local automation runs
events remain where they are
next startup resumes sync
remote sessions must use manual checkpoint
```

## 9.6 Internet Offline

If internet fails:

```text
capture continues locally
sync fails safely
retry later
health marks sync degraded
```

## 9.7 Corrupt Registry

If `registry/repos.yaml` cannot be parsed:

```text
do not run sync
write error to logs/errors/
fallback bootstrap to BOOT.md + CURRENT.md
run inventory in dry-run mode
require owner/Antigravity repair
```

---

# 10. Folder Structure Target

Create or ensure:

```text
airo-second-brain/
  BOOT.md
  CURRENT.md
  CONTEXT.md
  AGENTS.md
  SECURITY.md

  docs/
    AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md
    implementation/
      AIRO_SECOND_BRAIN_v0.4.1_IMPLEMENTATION_PLAN.md
    contracts/
      AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md
    validation/
      AIRO_SECOND_BRAIN_v0.4.1_VALIDATION_CHECKLIST.md
    handoff/
      ANTIGRAVITY_AIRO_SECOND_BRAIN_v0.4.1_EXECUTION_PROMPT.md
    exports/

  registry/
    repos.yaml
    sync-policy.yaml
    capture-policy.yaml
    consumer-policy.yaml

  scripts/
    airo-inventory
    airo-bootstrap
    airo-preflight
    airo-capture
    airo-sync
    airo-organize
    airo-distill
    airo-promote
    airo-health

  events/
    raw/
    synced/
    failed/

  inbox/
    session-closeouts/
    workspace-scans/
    remote/

  distill/
    proposals/
    accepted/
    rejected/
    superseded/

  state/
    active-context.md
    active-sessions.md
    system-health.md

  logs/
    sync/
    sync-errors/
    errors/

  locks/

  projects/
    _index.md
    airo-finance.md

  decisions/
    decision-log.md
    pending-decisions.md

  archive/
```

---

# 11. Script Contracts

## 11.1 Shared Contract

Every script must support:

```text
--help
--dry-run
--json
```

Every script must write logs to:

```text
logs/
```

Every script must return exit codes:

```text
0 = success
1 = warning/degraded
2 = blocked/failure
```

Every script must avoid printing secrets.

## 11.2 `airo-inventory`

Purpose:

```text
scan WSL paths and update registry
```

Allowed writes:

```text
registry/repos.yaml
inbox/workspace-scans/
logs/
state/system-health.md
```

Must not write:

```text
project source files
canonical project summaries except metadata proposal
```

Validation:

```bash
scripts/airo-inventory --dry-run
scripts/airo-inventory --json
```

PASS if:

```text
airo-second-brain found
vortex-ai-skill-lab found
observe-only repos found where present
unknown folders do not get deep-scanned
registry/repos.yaml valid YAML
```

## 11.3 `airo-bootstrap`

Purpose:

```text
standard startup protocol
```

Required sequence:

```text
read BOOT.md
read CURRENT.md
run/read airo-health
run airo-preflight for active project
print active project
print truth_status
print safe_to_work
print pending decisions
print pending proposals
```

Allowed writes:

```text
logs/
state/active-sessions.md
state/system-health.md
events/raw/
```

Validation:

```bash
scripts/airo-bootstrap --project airo-finance
```

PASS if:

```text
preflight runs automatically
system-health is shown
safe_to_work displayed
no canonical semantic rewrite occurs
```

## 11.4 `airo-preflight`

Purpose:

```text
compare registry memory with actual repo state
```

Allowed writes:

```text
registry/repos.yaml
state/system-health.md
logs/
events/raw/
```

Validation:

```bash
scripts/airo-preflight --project airo-finance --json
```

PASS if output includes:

```text
project_id
repo_path
repo_head
last_known_commit
git_dirty
truth_status
safe_to_execute
required_action
```

## 11.5 `airo-capture`

Purpose:

```text
append safe operational events to local disk
```

Allowed writes:

```text
events/raw/
logs/
```

Must not:

```text
push to GitHub
distill
organize
promote
```

Event format:

```json
{
  "timestamp": "ISO-8601",
  "consumer": "chatgpt|claude|antigravity|earesmes|system",
  "session_id": "string",
  "project_id": "string|null",
  "event_type": "repo_change|command|validation|error|checkpoint|decision_candidate",
  "summary": "safe short summary",
  "source": "system|manual|consumer",
  "sensitive": false
}
```

Validation:

```bash
scripts/airo-capture --event checkpoint --summary "test event" --project airo-second-brain
```

PASS if:

```text
NDJSON event appended
no Git push occurs
event contains no secret
```

## 11.6 `airo-sync`

Purpose:

```text
safe commit/push engine
```

Allowed writes:

```text
logs/sync/
logs/sync-errors/
state/system-health.md
registry/repos.yaml
git commits where allowed by policy
```

Required behavior:

```text
acquire lock
run secret guard
sync brain-safe paths
guard project repo
retry push 3x
update health
release lock
```

Validation:

```bash
scripts/airo-sync --dry-run
scripts/airo-sync --json
```

PASS if:

```text
lock works
secret guard runs
dry-run shows planned files
brain-safe paths identified
project-guarded repo not blindly committed
health updated
```

## 11.7 `airo-organize`

Purpose:

```text
apply lifecycle and prevent garbage accumulation
```

Allowed writes:

```text
events/synced/
events/failed/
inbox/
distill/
archive/
projects/_index.md
logs/
```

Must not:

```text
promote semantic proposal to canonical
delete raw data without retention rule
```

Validation:

```bash
scripts/airo-organize --dry-run
```

PASS if:

```text
planned moves shown
old raw events classified
proposal statuses indexed
no canonical semantic rewrite happens
```

## 11.8 `airo-distill`

Purpose:

```text
convert raw/inbox into deterministic metadata or semantic proposal
```

Modes:

```text
--mode deterministic
--mode semantic-proposal
```

Deterministic allowed writes:

```text
registry/repos.yaml
state/system-health.md
projects/_index.md
```

Semantic allowed writes:

```text
distill/proposals/
```

Must not:

```text
write directly to CURRENT.md
write directly to decisions/decision-log.md
write directly to projects/airo-finance.md without promote
```

Validation:

```bash
scripts/airo-distill --mode deterministic --dry-run
scripts/airo-distill --mode semantic-proposal --project airo-finance --dry-run
```

PASS if:

```text
deterministic metadata is objective
semantic output goes to proposal only
```

## 11.9 `airo-promote`

Purpose:

```text
promote approved proposal into canonical docs
```

Allowed actors:

```text
owner
antigravity factual awaiting-owner-review
```

Required fields:

```text
proposal_id
target_file
actor
promotion_type
source_evidence
awaiting_owner_review true|false
```

Must not allow:

```text
Earesmes semantic promotion
anonymous promotion
promotion without source evidence
```

Validation:

```bash
scripts/airo-promote --proposal <file> --target <file> --dry-run
```

PASS if:

```text
diff shown
metadata added
owner-review tag applied where needed
no silent overwrite
```

## 11.10 `airo-health`

Purpose:

```text
write system health file
```

Required output:

```text
state/system-health.md
```

Minimum content:

```yaml
generated_at: ISO-8601
safe_to_work: true|false
system_status: healthy|degraded|blocked
repos:
  airo-second-brain:
    truth_status: current|stale|dirty|conflict|unknown
    last_sync: ISO-8601|null
  airo-finance:
    truth_status: current|stale|dirty|conflict|unknown
    last_known_commit: string|null
    repo_head: string|null
pending:
  proposals: number
  decisions: number
  inbox_unprocessed: number
errors:
  count: number
  latest: string|null
```

Validation:

```bash
scripts/airo-health --json
```

PASS if:

```text
state/system-health.md exists
timestamp present
safe_to_work present
repo statuses present
errors summarized without secrets
```

---

# 12. Execution Plan

## 12.1 Execution Rules for Antigravity

Antigravity must not redesign architecture.

Antigravity must execute phases in order.

Antigravity must not skip validation.

Antigravity must not implement v2 features.

Antigravity must commit after each phase only after PASS.

Antigravity must stop on:

```text
secret guard hit
git conflict
unexpected dirty project repo
bootstrap degraded with missing required files
registry parse failure
```

## 12.2 Commit Strategy

Use one commit per phase.

Commit messages:

```text
docs: canonicalize AIRO Second Brain PRD v0.4.1
feat(airo-brain): add registry and inventory foundation
feat(airo-brain): add capture and health reporting
feat(airo-brain): add sync and preflight automation
feat(airo-brain): add bootstrap and organization lifecycle
feat(airo-brain): add distill and promote workflow
test(airo-brain): add v0.4.1 validation coverage
```

Do not combine all phases into one commit.

## 12.3 Phase 0 — Canonicalize PRD

### Goal

Make this PRD official in repo.

### Required files

```text
docs/AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md
docs/implementation/AIRO_SECOND_BRAIN_v0.4.1_IMPLEMENTATION_PLAN.md
docs/contracts/AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md
docs/validation/AIRO_SECOND_BRAIN_v0.4.1_VALIDATION_CHECKLIST.md
docs/handoff/ANTIGRAVITY_AIRO_SECOND_BRAIN_v0.4.1_EXECUTION_PROMPT.md
```

### Validation

```bash
test -f docs/AIRO_SECOND_BRAIN_PRD_v0.4.1_NO_BRAINER.md
test -f docs/implementation/AIRO_SECOND_BRAIN_v0.4.1_IMPLEMENTATION_PLAN.md
test -f docs/contracts/AIRO_SECOND_BRAIN_SCRIPT_CONTRACTS.md
test -f docs/validation/AIRO_SECOND_BRAIN_v0.4.1_VALIDATION_CHECKLIST.md
test -f docs/handoff/ANTIGRAVITY_AIRO_SECOND_BRAIN_v0.4.1_EXECUTION_PROMPT.md
git status --short
```

### PASS

```text
all files exist
Markdown source committed
no secret-like files
repo clean after commit
```

### Estimate

```text
0.5 day
```

## 12.4 Phase 1 — Registry & Inventory

### Goal

Second Brain knows all WSL repos/folders.

### Required files

```text
registry/repos.yaml
registry/sync-policy.yaml
registry/capture-policy.yaml
registry/consumer-policy.yaml
scripts/airo-inventory
inbox/workspace-scans/
logs/
```

Also create in AIRO Finance repo:

```text
/home/egitaristorandas/vortex-ai-skill-lab/AIRO_MANIFEST.md
```

### Validation

```bash
scripts/airo-inventory --dry-run
scripts/airo-inventory --json
python3 - <<'PY'
import yaml, pathlib
p=pathlib.Path("registry/repos.yaml")
assert p.exists()
data=yaml.safe_load(p.read_text())
assert data
print("PASS registry yaml")
PY
```

### PASS

```text
airo-second-brain registered as GOVERNED-BRAIN
vortex-ai-skill-lab registered as GOVERNED-GUARDED
known extra repos registered as OBSERVE-ONLY if present
unknown folders not deeply scanned
AIRO_MANIFEST.md exists in vortex-ai-skill-lab
```

### Estimate

```text
0.5–1 day
```

## 12.5 Phase 2 — Capture & Health

### Goal

Progress becomes visible and system health exists.

### Required files

```text
scripts/airo-capture
scripts/airo-health
events/raw/
state/system-health.md
logs/errors/
```

### Validation

```bash
scripts/airo-capture --event checkpoint --summary "phase 2 validation" --project airo-second-brain
scripts/airo-health --json
test -f state/system-health.md
find events/raw -type f | head
```

### PASS

```text
capture writes NDJSON
health writes state/system-health.md
health has generated_at, safe_to_work, repo statuses
no secret content logged
```

### Estimate

```text
1 day
```

## 12.6 Phase 3 — Sync & Preflight

### Goal

Automation core starts protecting and syncing.

### Required files

```text
scripts/airo-sync
scripts/airo-preflight
logs/sync/
logs/sync-errors/
locks/
```

Optional timer files:

```text
systemd/airo-sync.service
systemd/airo-sync.timer
```

or documented Windows Task Scheduler fallback.

### Validation

```bash
scripts/airo-preflight --project airo-finance --json
scripts/airo-sync --dry-run --json
test ! -f locks/airo-sync.lock || echo "lock exists"
```

Secret guard test must be dry-run only.

### PASS

```text
preflight shows repo_head and truth_status
sync dry-run shows planned actions
secret guard blocks test secret file
lock prevents concurrent sync
project-guarded repo is not blindly committed
health updates after preflight/sync
```

### Estimate

```text
1–2 days
```

## 12.7 Phase 4 — Bootstrap & Organize

### Goal

Consumers start from same entry point and Second Brain does not become garbage.

### Required files

```text
scripts/airo-bootstrap
scripts/airo-organize
events/synced/
events/failed/
distill/proposals/
archive/
state/active-sessions.md
```

### Validation

```bash
scripts/airo-bootstrap --project airo-finance
scripts/airo-organize --dry-run
```

### PASS

```text
bootstrap runs health
bootstrap runs preflight automatically
bootstrap prints safe_to_work
organize shows lifecycle actions
organize does not promote semantic canonical
```

### Estimate

```text
1 day
```

## 12.8 Phase 5 — Distill & Promote

### Goal

Raw/inbox can become proposal, and proposal can become canonical through gate.

### Required files

```text
scripts/airo-distill
scripts/airo-promote
distill/proposals/
distill/accepted/
distill/rejected/
distill/superseded/
```

### Validation

```bash
scripts/airo-distill --mode deterministic --dry-run
scripts/airo-distill --mode semantic-proposal --project airo-finance --dry-run
scripts/airo-promote --help
```

### PASS

```text
deterministic distill outputs metadata only
semantic distill outputs proposal only
promote shows diff in dry-run
Earesmes cannot promote semantic canonical
owner/Antigravity rules enforced
```

### Estimate

```text
1 day
```

## 12.9 Phase 6 — Stabilization & Abuse Testing

### Goal

System survives bad conditions.

### Required tests

```text
secret guard test
git conflict test
dirty repo test
stale repo test
push failure test
internet-off simulation or remote fail mock
stale lock test
bootstrap degraded test
corrupt registry test
observe-only repo test
```

### PASS

```text
no force push
no secret content logged
raw events preserved after failure
health reports degraded/blocked correctly
conflict stops automation
registry corruption stops sync
```

### Estimate

```text
1–2 days
```

---

# 13. Master Validation Checklist

v0.4.1 is complete only if all are true:

```text
[ ] PRD canonical Markdown exists
[ ] implementation plan exists
[ ] script contracts exist
[ ] validation checklist exists
[ ] Antigravity handoff prompt exists
[ ] registry exists and validates
[ ] airo-second-brain registered
[ ] vortex-ai-skill-lab registered
[ ] AIRO_MANIFEST.md exists in vortex-ai-skill-lab
[ ] all 9 scripts exist
[ ] all scripts support --help
[ ] all scripts support --dry-run where relevant
[ ] all scripts support --json where relevant
[ ] state/system-health.md exists
[ ] bootstrap calls preflight automatically
[ ] preflight detects current/stale/dirty/conflict/unknown
[ ] capture writes NDJSON locally
[ ] sync has lock
[ ] sync has secret guard
[ ] sync retries push
[ ] sync blocks secrets
[ ] organize does not promote semantic canonical
[ ] distill semantic writes proposals only
[ ] promote requires actor and source evidence
[ ] Earesmes cannot promote semantic canonical
[ ] failure modes update health
[ ] no raw transcript stored as canonical
[ ] no secret-like files committed
[ ] repo clean after final commit
```

---

# 14. Antigravity No-Brainer Execution Prompt

Use this as the execution prompt.

```text
You are executing AIRO Second Brain PRD v0.4.1 No-Brainer Execution Edition.

Repo:
/home/egitaristorandas/AI_WORKSPACES/airo-second-brain

Project repo:
/home/egitaristorandas/vortex-ai-skill-lab

Do not redesign the architecture.
Do not add new modules.
Do not implement v2 features.
Do not migrate repos into monorepo.
Do not introduce browser extension or AIRO Gateway.
Do not promote semantic canonical updates automatically.
Do not let Earesmes promote canonical knowledge.

Execute phases in order:

Phase 0: Canonicalize PRD and execution docs.
Phase 1: Registry & inventory.
Phase 2: Capture & health.
Phase 3: Sync & preflight.
Phase 4: Bootstrap & organize.
Phase 5: Distill & promote.
Phase 6: Stabilization & abuse testing.

After each phase:
1. Run validation.
2. Produce PASS/FAIL report.
3. Commit only if PASS.
4. Push only after secret guard PASS.
5. Stop on conflict, secret hit, registry corruption, or unexpected dirty critical repo.

Required rule:
Bootstrap must call preflight automatically.
Consumers must not be expected to remember preflight.

Required health output:
state/system-health.md

Required registry:
registry/repos.yaml

Required scripts:
scripts/airo-inventory
scripts/airo-bootstrap
scripts/airo-preflight
scripts/airo-capture
scripts/airo-sync
scripts/airo-organize
scripts/airo-distill
scripts/airo-promote
scripts/airo-health

Each script must support:
--help
--dry-run where relevant
--json where relevant

Final result must include:
- clean git status
- pushed GitHub state
- validation checklist PASS
- no secret-like files committed
- system-health.md generated
- bootstrap/preflight working
- sync dry-run safe
- promote gated
```

---

# 15. Roadmap & Estimate

| Stage                                    |  Estimate |
| ---------------------------------------- | --------: |
| Phase 0 — Canonical PRD + execution docs |   0.5 day |
| Phase 1 — Registry & inventory           | 0.5–1 day |
| Phase 2 — Capture & health               |     1 day |
| Phase 3 — Sync & preflight               |  1–2 days |
| Phase 4 — Bootstrap & organize           |     1 day |
| Phase 5 — Distill & promote              |     1 day |
| Phase 6 — Stabilization                  |  1–2 days |

## Practical Estimate

```text
MVP manual: 1–2 days
Auto-sync usable: 2–4 days
v0.4.1 complete: 4–5 days
Stable and tested: around 1 week
```

---

# 16. Before / After

## Before

```text
Second Brain exists but is passive.
AI consumers start inconsistently.
Owner repeats context.
Progress may disappear.
Repo changes may not be pushed.
Second Brain can become stale silently.
Raw logs can become garbage.
Canonical files can be rewritten incorrectly.
```

## After v0.4.1

```text
All WSL repos are inventoried.
Consumers start through bootstrap.
Bootstrap automatically runs preflight.
Truth status is known before work.
Progress is captured locally.
Safe changes are synced to GitHub.
Raw data is organized through lifecycle.
Semantic knowledge becomes proposal first.
Canonical memory changes only through promote gate.
Health report tells the system when it is healthy, stale, degraded, or blocked.
```

---

# 17. Anti-Requirements

Do not:

```text
dump all workspace files into Second Brain
store raw chat transcript as canonical
commit every chat message
auto-promote semantic decisions
let Earesmes rewrite canonical docs
force push conflicts
auto-commit project source code without guard
treat CURRENT.md as truth if repo/live state disagrees
implement browser extension in v0.4.1
implement AIRO Gateway in v0.4.1
migrate to monorepo in v0.4.1
add new core module beyond the locked 9
```

---

# 18. Final Acceptance Criteria

AIRO Second Brain v0.4.1 is accepted when:

```text
1. PRD and execution docs are canonical in repo.
2. Registry detects governed, observe-only, and unknown repos.
3. Bootstrap works as session entry point.
4. Bootstrap automatically calls preflight.
5. Health report exists and is readable by consumers.
6. Capture writes safe local event logs.
7. Sync can safely dry-run and push brain-safe paths.
8. Secret guard blocks risky files/content.
9. Organize prevents raw/inbox/proposal garbage buildup.
10. Distill creates proposals, not canonical overwrites.
11. Promote enforces gate and actor rules.
12. Failure modes are tested.
13. GitHub remote is clean and pushed.
14. No secrets are committed.
15. Antigravity can continue future phases without redesigning architecture.
```

---

# 19. Final Statement

AIRO Second Brain v0.4.1 is not a note app and not a raw archive.

It is the local-first governance layer for AIRO workspaces.

Its job is to make AI consumers safer and more consistent by ensuring:

```text
capture happens before memory loss
preflight happens before execution
sync happens before local progress disappears
organize happens before logs become garbage
distill happens before raw evidence becomes useful knowledge
promote happens before proposal becomes canonical truth
health happens before consumers work blind
```

This is the approved no-brainer execution baseline.
