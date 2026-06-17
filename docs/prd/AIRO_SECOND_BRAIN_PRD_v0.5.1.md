# AIRO SECOND BRAIN PRD v0.5.1

## No-Brainer Execution Specification

### Obsidian LLM Wiki, Pending Jobs, Resident AIRO Sync, Hybrid Promotion

**Status:** FINAL — OWNER APPROVED
**Default shorthand:** `ASB` or `asb` means `AIRO Second Brain`.
**Supersedes:** PRD v0.5
**Depends on:** AIRO Second Brain v0.4.1
**Repository:** `https://github.com/progamer6918/airo-second-brain`
**Local repository:** `/home/egitaristorandas/AI_WORKSPACES/airo-second-brain`
**Canonical PRD path:** `docs/prd/AIRO_SECOND_BRAIN_PRD_v0.5.1.md`
**Owner:** Egit Aristo Randas
**Resident orchestrator:** Earesmes / Hermes as AIRO Sync
**Reasoning consumers:** ChatGPT and Claude
**Technical executor:** Antigravity
**Human interface:** Obsidian

---

# 1. Purpose

AIRO Second Brain v0.5.1 upgrades the existing shared-memory and synchronization foundation into an active knowledge, continuity, and orchestration system.

Required operating loop:

```text
Project activity or source appears
→ captured as evidence or raw source
→ synchronized safely
→ classified deterministically
→ routine work handled by Earesmes
→ reasoning work becomes a consultation job
→ ChatGPT or Claude discusses it with the owner
→ approved technical work becomes an execution job
→ Antigravity executes it
→ execution evidence returns to AIRO Second Brain
→ knowledge is distilled
→ approved semantic knowledge becomes canonical
→ Obsidian displays the same repository
```

This PRD must not create a second knowledge repository.

Obsidian opens the existing `airo-second-brain` repository directly.

---

# 2. Locked Owner Decisions

## 2.1 Source intake

Accepted channels:

```text
local files
Telegram through Earesmes
Obsidian Web Clipper
ChatGPT or Claude session outputs
Antigravity output
terminal and Git evidence
manual paste or upload
```

Accepted source origins:

```text
external source
AI session source
execution evidence
owner-created source
```

## 2.2 Work routing

```text
routine deterministic work
→ Earesmes

light single-source draft
→ Earesmes free-tier model

heavy reasoning
→ consultation job for ChatGPT or Claude

technical execution
→ Antigravity after consultation

semantic decision
→ owner approval
```

## 2.3 Project workflow

```text
ChatGPT or Claude consultation
→ owner decision
→ execution job
→ Antigravity execution
→ Earesmes capture, health, sync, and orchestration
```

Antigravity must not receive an unresolved vague problem when consultation is still required.

## 2.4 Schedule

```text
capture:
when meaningful activity occurs

safe sync:
target every 10 minutes while WSL is active

mini closeout:
at explicit session close or qualifying inactivity timeout

nightly processing:
22:00 local time while WSL is available

offline catch-up:
on the next WSL startup
```

## 2.5 Obsidian

Vault path:

```text
/home/egitaristorandas/AI_WORKSPACES/airo-second-brain
```

No duplicate vault may be created.

## 2.6 Promotion

Hybrid promotion:

```text
machine facts
→ automatic

operational facts with evidence
→ controlled automatic update

semantic knowledge or strategic decisions
→ explicit owner approval
```

## 2.7 Retention

```text
original sources
→ retained or stably referenced

execution evidence
→ retained according to project needs

technical telemetry and repetitive logs
→ rotate or archive after 30–90 days

rejected proposals
→ archive with rejection reason
```

---

# 3. Truth Hierarchy

When information conflicts:

```text
1. Live runtime evidence
2. Actual project repository
3. Direct machine and Git evidence
4. Verified AIRO registry state
5. Canonical AIRO Second Brain knowledge
6. Approved decisions and reviews
7. Distillation proposals
8. Raw sources and inbox
9. Chat memory
```

Examples:

```text
CURRENT.md says a deployment passed,
but runtime verification fails.
→ runtime evidence wins

A project note says three files changed,
but Git diff shows five.
→ Git evidence wins

A chat says a task completed,
but no execution evidence exists.
→ task remains unverified
```

Chat history is never authoritative by itself.

---

# 4. System Roles

## 4.1 Owner

The owner:

```text
sets direction
chooses between options
approves semantic conclusions
approves architecture changes
approves destructive actions
declares major milestones complete
```

Natural approval phrases may include:

```text
setuju
gas
kunci keputusan ini
pakai opsi ini
lanjut dengan opsi B
```

A phrase becomes durable approval only after it is stored using the approval protocol.

## 4.2 ChatGPT and Claude

They operate as AIRO Sync reasoning consumers.

Responsibilities:

```text
consultation
analysis
architecture
PRD drafting
comparison
semantic synthesis
risk assessment
execution planning
owner-decision recording
```

They must not claim technical execution without direct evidence.

## 4.3 Antigravity

Antigravity handles:

```text
repository inspection
source-code changes
script changes
scheduler installation
runtime repair
testing
deployment
Git commit and push
execution evidence
```

Antigravity must not silently redesign the architecture.

## 4.4 Earesmes / Hermes

Earesmes is the resident AIRO Sync persona on the owner’s machine.

Responsibilities:

```text
source intake
event capture
job creation
job routing
job status tracking
safe synchronization
health monitoring
scheduler operation
nightly organization
light draft processing
approved promotion execution
notifications
startup catch-up
verified project-status reporting
```

Earesmes is not merely an administrator.

Earesmes is the local resident orchestrator and continuity agent.

Its reasoning capability remains limited by the free-tier model available. Difficult reasoning must be escalated rather than improvised.

## 4.5 Obsidian

Obsidian is:

```text
human reading interface
Markdown editor
graph visualization
navigation cockpit
review interface
```

Obsidian does not independently create semantic relationships.

Agents or humans create Markdown links. Obsidian displays them.

---

# 5. Required Logical Repository Structure

Existing compatible paths must be reused where possible.

```text
airo-second-brain/
├── BOOT.md
├── CURRENT.md
├── HOME.md
├── AGENTS.md
├── SECURITY.md
│
├── docs/
│   ├── prd/
│   │   └── AIRO_SECOND_BRAIN_PRD_v0.5.1.md
│   └── implementation/
│
├── config/
│   ├── airo-v051.yml
│   ├── routing-policy.yml
│   ├── retention-policy.yml
│   ├── consumer-policy.yml
│   └── obsidian-profile.md
│
├── state/
│   ├── active-context.md
│   ├── system-health.md
│   ├── bootstrap-summary.md
│   ├── bootstrap-manifest.json
│   ├── runtime-status.json
│   └── scheduler-status.json
│
├── jobs/
│   ├── pending/
│   │   ├── consultation/
│   │   ├── execution/
│   │   └── owner/
│   ├── claimed/
│   ├── in-progress/
│   ├── completed/
│   ├── failed/
│   ├── cancelled/
│   ├── stale/
│   ├── templates/
│   ├── locks/
│   └── _index.md
│
├── inbox/
│   ├── raw/
│   │   ├── local/
│   │   ├── telegram/
│   │   └── web/
│   ├── ai-sessions/
│   ├── execution-evidence/
│   ├── session-closeouts/
│   └── quarantine/
│
├── knowledge/
│   ├── _index.md
│   ├── concepts/
│   ├── tools/
│   ├── methods/
│   ├── sources/
│   └── comparisons/
│
├── distill/
│   ├── proposals/
│   ├── approved/
│   ├── rejected/
│   └── superseded/
│
├── reviews/
│   ├── owner-approvals/
│   ├── owner-decisions/
│   ├── owner-review-queue.md
│   └── owner-approval-index.md
│
├── events/
│   ├── raw/
│   └── normalized/
│
├── logs/
│   ├── sync/
│   ├── capture/
│   ├── nightly/
│   ├── health/
│   └── audit/
│
├── archive/
│
├── templates/
│   ├── source-record.md
│   ├── consultation-job.md
│   ├── execution-job.md
│   ├── owner-job.md
│   ├── approval-record.md
│   ├── source-summary.md
│   ├── concept-note.md
│   └── session-closeout.md
│
├── bin/
│   ├── airo-bootstrap
│   ├── airo-preflight
│   ├── airo-capture
│   ├── airo-job
│   ├── airo-session
│   ├── airo-sync
│   ├── airo-nightly
│   ├── airo-promote
│   ├── airo-lint
│   └── airo-health
│
└── .private-local/
```

Equivalent existing structures may be retained when documented in the implementation manifest.

---

# 6. BOOT.md Contract

`BOOT.md` is the stable entry point for every AI consumer.

Its static instructions must remain usable even if dynamic bootstrap generation has never run or has failed.

## 6.1 Ownership

```text
Static instructions
→ maintained through approved repository changes

Dynamic bootstrap block
→ generated by bin/airo-bootstrap

Runtime evidence
→ generated from verified repository and machine state
```

Automated changes are allowed only between:

```markdown
<!-- AIRO:GENERATED-BOOTSTRAP:START -->
<!-- AIRO:GENERATED-BOOTSTRAP:END -->
```

Content outside those markers must not be changed automatically.

## 6.2 Required static sections

`BOOT.md` must contain:

```text
AIRO Sync persona contract
repository purpose
truth hierarchy
consumer behavior
required read order
recovery behavior
command-output contract
security restrictions
dynamic bootstrap pointer
```

## 6.3 Required read order

```text
1. BOOT.md
2. state/bootstrap-summary.md
3. CURRENT.md
4. state/active-context.md
5. state/system-health.md
6. jobs/_index.md
7. reviews/owner-review-queue.md
8. relevant active-project file
9. relevant pending job
```

Startup prompts must not depend on permanently hardcoded dated review files.

## 6.4 Bootstrap states

Allowed states:

```text
NEVER_RUN
FRESH
STALE
FAILED
```

Definitions:

```text
NEVER_RUN
= bootstrap has never completed successfully

FRESH
= generated state passes all freshness checks

STALE
= prior generated state exists but is no longer current

FAILED
= latest bootstrap attempt failed
```

## 6.5 Initial committed state

Before the first bootstrap run:

```yaml
bootstrap_status: NEVER_RUN
generated_at: null
expires_at: null
generated_against_head: null
warning: Dynamic bootstrap state has not been generated.
```

`state/bootstrap-manifest.json` must also contain valid `NEVER_RUN` state.

No fake placeholder values are allowed.

## 6.6 Required dynamic fields

```yaml
kernel_version:
bootstrap_status:
generated_at:
expires_at:
freshness_threshold_minutes: 30
generated_against_head:
generated_by:
repository_head:
repository_branch:
repository_clean:
last_successful_sync:
last_health_check:
scheduler_state:
active_project_ids:
active_context_path:
health_path:
pending_consultation_count:
pending_execution_count:
pending_owner_count:
owner_review_queue_path:
highest_priority_jobs:
runtime_warnings:
last_attempt_at:
last_attempt_status:
```

## 6.7 Freshness

Default maximum freshness:

```text
30 minutes
```

Generated state is `FRESH` only when:

```text
current time <= expires_at
current HEAD == generated_against_head
required pointer targets exist
bootstrap completed successfully
health data passes its own freshness check
manifest and generated BOOT block agree
```

Immediate stale conditions:

```text
repository HEAD changed
required pointer disappeared
active-project pointer is invalid
referenced job moved, completed, or disappeared
manifest and BOOT block disagree
health state is stale
```

## 6.8 Failed generation

On failure:

```text
set bootstrap_status to FAILED
record sanitized failure reason
retain last-known values only when explicitly labeled
do not replace verified data with partial or invented data
```

## 6.9 Consumer behavior

When `FRESH`:

```text
use generated pointers
continue applying truth hierarchy
```

When `STALE`:

```text
show BOOTSTRAP_STALE
do not trust generated counts or runtime state as current
verify files directly where possible
request bootstrap refresh or manual bundle
state the limitation
```

When `NEVER_RUN`:

```text
show BOOTSTRAP_NEVER_RUN
follow static recovery instructions
do not assume dynamic pointers are valid
request initial bootstrap run or manual bundle
```

When `FAILED`:

```text
show BOOTSTRAP_FAILED
do not silently treat last-known data as current
request repair or manual evidence
```

---

# 7. Public Repository Security

The repository is public.

Automated intake and sync must not begin until safety controls pass.

## 7.1 Required Git ignore rules

At minimum:

```gitignore
.private-local/
.env
.env.*
*.pem
*.key
*.p12
*.pfx
credentials*
secrets*
token*
```

Existing valid rules must be preserved.

## 7.2 Local-only paths

```text
.private-local/raw/
.private-local/attachments/
.private-local/drafts/
.private-local/quarantine/
```

## 7.3 Automation denylist

All automated scanners and processors must exclude:

```text
.private-local/
.git/
logs/
jobs/locks/
temporary files
secret-pattern matches
```

## 7.4 Pre-commit and pre-push guard

Before automated commit or push:

```text
scan staged filenames
scan staged text
block known secret patterns
block .private-local
block unsupported binary sources
block sensitive account details
```

On detection:

```text
stop commit
quarantine unsafe intake where appropriate
create sanitized security incident
notify owner
do not print the secret
```

Fake-secret acceptance tests are mandatory.

---

# 8. Preflight Bootstrap

## 8.1 Capability matrix

Phase 0A must inspect:

```text
airo-bootstrap
airo-preflight
airo-capture
airo-job
airo-session
airo-sync
airo-nightly
airo-promote
airo-lint
airo-health
```

For each capability record:

```text
required capability
existing implementation
existing path
status: PRESENT | PARTIAL | MISSING | CONFLICTING
reuse action
required phase
```

## 8.2 airo-preflight ownership

```text
PRESENT
→ validate and use

PARTIAL
→ patch in Phase 0B

MISSING
→ create in Phase 0B

CONFLICTING
→ stop and create consultation job
```

## 8.3 BOOTSTRAP_SAFETY_PATCH

Because preflight itself may not exist, one bounded exception is allowed:

```text
BOOTSTRAP_SAFETY_PATCH
```

Allowed scope:

```text
create or repair airo-preflight
repair .gitignore
create .private-local enforcement
create minimum secret guard
```

Authorization is valid when:

```text
PRD is stored at canonical path
status is FINAL — OWNER APPROVED
PRD is committed
PRD commit hash or file hash is recorded
change remains inside safety scope
```

No separate owner approval is required.

The exception does not authorize:

```text
scheduler installation
runtime changes
source-intake automation
Obsidian rollout
LLM Wiki processing
changes to other project repositories
```

After preflight passes, the exception expires.

---

# 9. Deterministic Work Classification

Routing policy must exist in:

```text
config/routing-policy.yml
```

Rules are evaluated in order.

## Rule 1 — Owner or destructive decision

Examples:

```text
delete canonical knowledge
delete project data
approve semantic knowledge
change security rules
change project direction
declare project complete
authorize material-risk deployment
expose sensitive information
```

Route:

```text
Class 5 → owner job
```

## Rule 2 — Technical mutation

Examples:

```text
source code
project repository
scheduler
service
deployment
runtime configuration
Git history
system package
database
workbook
```

Route:

```text
Class 4
→ consultation first unless already approved
→ execution job for Antigravity
```

## Rule 3 — Heavy reasoning

Examples:

```text
compare multiple sources
reconcile conflicting evidence
change multiple canonical pages
make architecture recommendation
write or revise PRD
infer long-term patterns
detect nuanced contradictions
perform semantic promotion
```

Route:

```text
Class 3 → consultation job
```

## Rule 4 — Deterministic operation

Examples:

```text
checksum
timestamp
filename
Git branch
commit hash
job count
exact duplicate detection
known-folder move
status transition
sync
health command
```

Route:

```text
Class 1 → Earesmes executes
```

## Rule 5 — Light single-source draft

All conditions must be true:

```text
one source only
within configured size limit
no code modification
no deployment
no security decision
no semantic promotion
draft-only output
no multi-source comparison
no direct multi-page canonical update
```

Route:

```text
Class 2 → Earesmes may draft
```

Otherwise escalate to Class 3.

Uncertainty rule:

```text
When uncertain, escalate one class upward.
```

---

# 10. Pending Jobs

Pending jobs are the free-tier bridge between consumers.

Earesmes does not directly call ChatGPT or Claude web.

## 10.1 Job types

```text
consultation
execution
owner-decision
maintenance
```

## 10.2 IDs

```text
CONSULT-YYYYMMDD-NNN
EXEC-YYYYMMDD-NNN
OWNER-YYYYMMDD-NNN
MAINT-YYYYMMDD-NNN
```

## 10.3 Universal frontmatter

```yaml
---
schema_version: "1.0"
job_id:
job_type:
status:
project_id:
title:
created_at:
created_by:
priority: low | normal | high | critical
source_refs: []
derived_from: []
recommended_worker:
claimed_by:
claimed_at:
claim_expires_at:
owner_approval_required:
risk_level: low | medium | high | critical
idempotency_key:
last_updated_at:
---
```

## 10.4 Statuses

```text
pending
claimed
in-progress
blocked
completed
failed
cancelled
stale
```

## 10.5 Job claim

Before work:

```text
create atomic job lock
verify job is pending
set claim actor and timestamps
move job to claimed
release transition lock
```

Job lock:

```text
jobs/locks/<job_id>.lock
```

Default expiry:

```text
consultation: 12 hours
execution: 4 hours
owner: no automatic expiry
maintenance: 2 hours
```

## 10.6 Idempotency key

Format:

```text
v1:<job_type>:<project_id>:<fingerprint>
```

Canonical fingerprint payload:

```text
job_type=<lowercase>
project_id=<lowercase canonical id>
objective=<case-preserved normalized text>
source_refs=<sorted normalized refs>
scope=<case-preserved normalized text>
```

Normalization:

```text
Unicode NFKC
line endings to LF
trim outer whitespace
collapse repeated whitespace
preserve objective and scope case
```

Fingerprint:

```text
first 16 lowercase hexadecimal characters of SHA-256
```

A duplicate active key in `pending`, `claimed`, `in-progress`, or `blocked` must be rejected.

Explicit reruns require:

```yaml
rerun_of:
rerun_reason:
force_rerun: true
```

## 10.7 Required job body

Consultation job:

```text
Problem
Verified facts
Evidence
Questions
Expected output
Constraints
Risks
Unknowns
Owner decisions required
```

Execution job:

```text
Objective
Approved decision source
Verified current state
Exact scope
Allowed files and systems
Prohibited files and systems
Preconditions
Allowed execution modes
Execution steps
Validation
PASS criteria
FAIL conditions
Stop conditions
Rollback
Required evidence
Required final report
```

Owner job:

```text
Decision required
Reason
Options
Recommendation
Impact
Safe default
Deadline
```

---

# 11. Session and Closeout

A session is a bounded period of meaningful work under one main project or job.

## 11.1 Session start

A session starts when:

```text
owner starts or continues a project
consumer claims a job
Antigravity starts an execution job
Earesmes receives session-start
terminal task launches with a registered job ID
```

## 11.2 Meaningful event

A session qualifies for closeout when:

```text
file changes
job state changes
decision occurs
command produces evidence
source is ingested
blocker is found
test or deployment is attempted
```

Casual conversation does not require project closeout.

## 11.3 Explicit closeout

Triggers:

```text
owner says closeout
owner switches project
execution completes or fails
consumer creates handoff
Antigravity produces final report
Earesmes receives session-end
```

## 11.4 Inactivity draft

After 45 minutes of inactivity, when meaningful activity exists:

```text
status: closeout-draft
closeout_reason: inactivity-timeout
```

This does not mark the session permanently complete.

## 11.5 Browser limitation

Earesmes cannot reliably detect the end of a ChatGPT or Claude browser session.

Closing a browser tab is not verified closeout.

## 11.6 Closeout fields

```text
objective
work performed
files or knowledge changed
decisions
owner approvals
validation
failures
blockers
pending jobs
next exact action
evidence refs
repository HEAD
```

---

# 12. Owner Approval Protocol

## 12.1 Storage

```text
reviews/owner-approvals/APPROVAL-YYYYMMDD-NNN.md
```

Permanent catalog:

```text
reviews/owner-approval-index.md
```

## 12.2 Schema

```yaml
---
schema_version: "1.0"
approval_id:
decision: approved | rejected | changes-requested
proposal_id:
job_id:
project_id:
approved_at:
owner:
recorded_by:
source_type:
source_ref:
approval_phrase:
scope:
content_hash:
---
```

## 12.3 Responsibility

```text
Owner
→ makes decision

ChatGPT or Claude
→ formulates receipt

Earesmes
→ may store receipt mechanically

Antigravity
→ may store receipt during approved repository work
```

No agent may invent approval.

## 12.4 Web fallback

When a web consumer cannot write the repo:

```text
APPROVAL_RECEIPT
approval_id:
proposal_id:
decision:
approval_phrase:
scope:
source_session:
recorded_at:
END_APPROVAL_RECEIPT
```

Promotion remains blocked until this exists in the repository.

## 12.5 Hash binding

Approval is bound to the exact approved proposal content.

Semantic changes require new approval.

## 12.6 Promotion gate

All must pass:

```text
approval file exists
decision is approved
proposal ID matches
content hash matches
scope permits destination
security checks pass
no unresolved contradictory evidence
```

---

# 13. Review Queue versus Approval Records

`reviews/owner-review-queue.md` is a derived view of unresolved owner actions.

It may include:

```text
pending owner decisions
semantic proposals awaiting approval
changes-requested proposals
conflicts needing owner resolution
destructive actions awaiting authorization
```

It is not approval evidence.

`reviews/owner-approvals/` stores immutable receipts.

`reviews/owner-approval-index.md` stores the permanent catalog.

Lifecycle:

```text
proposal or owner job created
→ enters review queue

owner answers
→ approval receipt created

receipt validates
→ queue item resolves

proposal changes
→ new hash
→ new approval required
```

The queue must be regenerable from source records.

---

# 14. Consumer Bootstrap Protocol

## ChatGPT or Claude

At session start:

```text
adopt AIRO Sync persona
read BOOT.md
validate bootstrap status
follow only valid pointers
read bootstrap summary
read CURRENT.md
read active context
read system health
read jobs index
read owner review queue
read relevant project
read relevant pending job
report freshness or access limitations
only then analyze
```

If access fails:

```text
do not silently rely on memory
state the failure
request latest bootstrap bundle
label advice as fallback-context advice
```

Fallback bundle:

```text
BOOT.md
bootstrap summary
CURRENT.md
active context
system health
relevant job
relevant project file
```

Consultation output must contain:

```text
verified state
analysis
options
recommendation
owner decision required
execution implications
job update
next exact action
```

After approval:

```text
approval receipt
execution job
session closeout
```

---

# 15. Antigravity Execution Protocol

Before modification, read:

```text
BOOT.md
this PRD
bootstrap summary
system health
jobs index
exact execution job
Git status
recent Git log
```

Allowed modes:

```text
READ_ONLY_AUDIT
BOOTSTRAP_SAFETY_PATCH
LOCAL_SOURCE_PATCH
LOCAL_CONFIG_PATCH
RUNTIME_INSTALL
CONTROLLED_VALIDATION
COMMIT_AND_PUSH
```

A job must explicitly authorize its mode.

Before editing, record:

```text
repository path
branch
HEAD
Git status
relevant hashes
runtime state
job ID
approval source
backup path
```

Execution rules:

```text
smallest bounded change
no unrelated formatting
no unrelated cleanup
reuse compatible components
validate before commit
stop when guard fails
```

Final report:

```text
job ID
mode
PASS | FAIL | BLOCKED
files changed
before and after hashes
commands
validation
runtime evidence
commit
push result
rollback status
remaining risks
next exact action
```

Every owner-facing terminal command must:

```text
use set -euo pipefail where suitable
tee output to /tmp/<descriptive-name>.txt
copy final output with clip.exe
print repo and mode
avoid hidden destructive behavior
```

---

# 16. Phase 0 Runtime Acceptance

Official starting status:

```text
implementation baseline: may exist
runtime acceptance: NOT YET PROVEN
scheduler liveness: UNKNOWN
startup catch-up liveness: UNKNOWN
health freshness: requires direct audit
```

## 16.1 Phase 0A — READ_ONLY_AUDIT

Inspect:

```text
repository tree
v0.4.1 scripts
services and timers
Git state and history
security rules
equivalent existing paths
capability matrix
writer-lock implementation
Earesmes integration references
```

Required artifact after audit approval:

```text
docs/implementation/v051-existing-system-inventory.md
```

The initial audit command itself must not mutate the repository.

## 16.2 Phase 0B — Safety baseline

Using `BOOTSTRAP_SAFETY_PATCH` only when necessary:

```text
enforce .private-local ignore
create or repair preflight
create minimum secret guard
verify public-repo safety
run fake-secret tests
```

## 16.3 Phase 0C — Runtime acceptance

Verify:

```text
sync implementation
active scheduler mechanism
health freshness
advancing sync logs
catch-up behavior
repository safety
```

WARN is not PASS.

## 16.4 Failure path

If WARN or FAIL:

```text
stop feature implementation
create runtime-repair consultation job
record failed checks
ChatGPT or Claude prepares repair plan
owner approves material changes
Antigravity repairs
rerun full Phase 0C
continue only after PASS
```

---

# 17. Git Writer Concurrency

## 17.1 Single automated writer

Only one automated writer may mutate the worktree at one time.

Automated writers include:

```text
Earesmes
airo-sync
airo-nightly
airo-bootstrap write mode
airo-promote
Antigravity
other automation
```

## 17.2 Writer lock

Required lock:

```text
.git/airo-automation-write.lock
```

Recommended WSL mechanism:

```text
flock
```

Scheduled Earesmes operation:

```text
non-blocking
locked → BUSY
no mutation
retry next cycle
```

Antigravity:

```text
wait maximum 60 seconds
then BLOCKED
do not delete or bypass lock
```

Correctness depends on advisory lock state, not file existence alone.

Phase 0A and controlled tests must verify:

```text
normal process exit
forced termination
orphan lock file
WSL restart where safely possible
```

If unverified:

```text
WRITER_LOCK_UNVERIFIED
concurrent automation disabled
one controlled writer only
```

## 17.3 Dirty worktree

Automation must not use:

```text
git add .
git add -A
```

Only explicit allowlisted paths may be staged.

Unrelated Obsidian or owner edits must not be staged, reset, stashed, checked out, or discarded.

Same-file overlap causes STOP.

## 17.4 Remote freshness

Before commit and push:

```text
acquire lock
run preflight
inspect scope
git fetch origin
compare local HEAD and origin/main
```

Rules:

```text
same HEAD
→ bounded commit and push

remote ahead, no local commits
→ fast-forward only if safe
→ rerun preflight

local ahead, remote ancestor
→ guarded push

diverged
→ STOP
→ no auto-merge
→ no auto-rebase
→ no force-push

remote ahead with conflicting dirty changes
→ STOP
→ no pull
→ no automatic stash
```

## 17.5 Push rejection

```text
no force-push
no infinite retry
fetch once
classify state
network failure → log and retry later
divergence → GIT_CONFLICT_PAUSED
```

## 17.6 Conflict workflow

```text
conflict detected
→ stop automation
→ create sanitized incident
→ create consultation job
→ ChatGPT or Claude analyzes
→ owner approves strategy
→ Antigravity executes resolution
→ validate
→ preflight PASS
→ resume automation
```

Owner approves the strategy. Antigravity handles technical conflict resolution.

During `GIT_CONFLICT_PAUSED`:

```text
automated push stops
local capture may continue
no semantic promotion
no destructive cleanup
no force-push
```

---

# 18. Scheduler Semantics

A WSL scheduler cannot run while WSL or the host is unavailable.

The system must distinguish:

```text
scheduled time
actual execution time
catch-up time
```

## 18.1 Sync

Target:

```text
every 10 minutes while WSL is active
```

No safe changes:

```text
successful no-op
no empty commit
```

## 18.2 Nightly

Target:

```text
22:00 local time
```

If missed:

```text
run once during next startup catch-up
record scheduled and actual times
```

## 18.3 Startup catch-up

```text
check last successful sync
check last nightly run
process safe unsynced capture
run overdue nightly exactly once
refresh health
update bootstrap
```

Persistent run IDs must prevent duplicate catch-up.

## 18.4 Windows bridge

Windows Task Scheduler is optional and requires a separate approved execution job.

Without it:

```text
LIMITED_OFFLINE_MODE
```

No processing occurs while the machine is unavailable. Safe overdue work runs at startup.

---

# 19. Source Intake

Source record:

```yaml
---
schema_version: "1.0"
source_id:
source_type:
origin:
captured_at:
captured_by:
project_id:
topic:
status:
sensitivity:
source_url:
local_path:
checksum:
duplicate_of:
---
```

Simple owner commands:

```text
Simpan sumber ini.
Project:
Topik:
```

```text
Ingest sumber ini.
Project:
Tujuan:
Fokus:
Output yang dibutuhkan:
```

```text
Buat consultation job dari sumber ini.
Project:
Pertanyaan utama:
Bandingkan dengan:
Keputusan yang ingin diambil:
```

Pipeline:

```text
receive
→ security check
→ checksum
→ duplicate check
→ source record
→ sensitivity routing
→ classification
→ raw storage or safe reference
→ optional draft or job
```

Raw sources remain unchanged or stably referenced.

AI-session output is labeled as AI-session material and is not automatically factual evidence.

Execution evidence remains separate from AI opinion.

---

# 20. Nightly Processing

Allowed:

```text
scan inbox
verify metadata
detect exact duplicates
normalize filenames
classify work
update job indexes
create consultation jobs
run broken-link checks
identify orphan notes
update health
update bootstrap
safe sync
```

Class 2 AI output remains draft-only.

Prohibited:

```text
semantic approval
architecture rewrite
canonical deletion
deployment
project-repository mutation
automatic conflict merge
strategic decision
```

Progress after 22:00 remains captured and synced, then organized during closeout or the next nightly run.

---

# 21. LLM Wiki Lifecycle

```text
raw source
→ source record
→ source-summary proposal
→ concept or entity proposal
→ consultation or lint
→ owner approval when semantic
→ canonical knowledge
```

Raw sources remain immutable.

LLM interpretation enters:

```text
distill/proposals/
```

Canonical knowledge remains in existing canonical domains:

```text
projects/
systems/
agents/
knowledge/
identity/
decisions/
```

Semantic links may be added to proposals.

Direct canonical links are allowed only when:

```text
both pages exist
relationship is directly evidenced
no strategic interpretation is required
```

Lint checks:

```text
broken links
orphan pages
duplicate concepts
conflicts
stale claims
missing references
unprocessed proposals
invalid approval hashes
job-index drift
```

Lint reports findings. It does not silently rewrite strategic knowledge.

---

# 22. Hybrid Promotion

## Level A — Machine facts

Automatic:

```text
branch
HEAD
Git status
timestamps
file-change count
job counts
last sync
scheduler state
validation exit code
```

## Level B — Operational facts

Automatic only with evidence:

```text
test result
job completion
deployment identifier
files changed
validated bug fix
runtime state
```

Required evidence:

```text
command output
commit or diff
validation
runtime evidence when applicable
```

## Level C — Semantic knowledge

Owner approval required:

```text
architecture decisions
strategic conclusions
personal preferences
roadmap changes
project completion
cross-source interpretation
```

Earesmes may mechanically validate and promote approved material.

Earesmes may not approve its own proposal, alter approved meaning, invent approval, or expand scope.

---

# 23. Obsidian Integration

Vault:

```text
/home/egitaristorandas/AI_WORKSPACES/airo-second-brain
```

No second vault.

Recommended local ignores:

```gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache/
.obsidian/plugins/
```

`HOME.md` must expose:

```text
system health
active project
recent progress
pending consultation jobs
pending execution jobs
pending owner actions
recent sources
recent canonical knowledge
unprocessed proposals
last sync
last nightly run
```

Normal Graph View excludes:

```text
logs/
jobs/locks/
jobs/completed/
jobs/failed/
events/raw/
archive/
.private-local/
```

```text
HOME.md → human entry point
BOOT.md → AI entry point
```

---

# 24. Required CLI Contracts

Existing v0.4.1 components must be reused or extended.

## airo-bootstrap

```text
inspect repo
inspect health and scheduler
index jobs
generate summary and manifest
update only generated BOOT block
```

Required options:

```text
--dry-run
--json
--no-write
```

## airo-preflight

```text
repository guard
secret guard
job guard
runtime guard
mode authorization
writer-lock awareness
```

## airo-capture

```text
capture source
capture event
capture execution evidence
capture AI closeout
```

## airo-job

```text
create
list
show
claim
start
block
complete
fail
cancel
requeue-stale
validate
```

## airo-session

```text
start
event
status
close
draft-closeout
resume
```

## airo-sync

```text
writer lock
secret scan
repository check
remote freshness
bounded staging
commit
push
retry policy
log
health update
```

## airo-nightly

```text
catch-up
inbox organization
routing
job generation
lint
index update
bootstrap update
safe sync
```

## airo-promote

```text
validate proposal
validate approval
validate hash
mechanical promotion
index update
promotion record
```

## airo-health

```text
runtime health
scheduler health
repository health
writer-lock health
job health
bootstrap freshness
sync freshness
```

---

# 25. Implementation Phases

Each phase must be validated and committed separately.

## Phase 0A — Read-only inventory

Mode:

```text
READ_ONLY_AUDIT
```

Inspect:

```text
repository
scripts
timers and services
Git state
security rules
existing structures
capability matrix
writer lock
Earesmes references
```

No mutation.

## Phase 0B — Safety baseline

```text
.private-local enforcement
preflight creation or repair
minimum secret guard
fake-secret tests
```

## Phase 0C — Runtime acceptance

```text
sync runtime
health freshness
scheduler
logs
catch-up
```

Failure means stop feature work and create repair flow.

## Phase 1 — BOOT and bootstrap

```text
static BOOT contract
generated markers
manifest
NEVER_RUN/FRESH/STALE/FAILED
freshness checks
UNKNOWN behavior
```

## Phase 2 — Jobs

```text
folders
templates
IDs
idempotency
claim locks
expiry
stale handling
index
```

## Phase 3 — Approval and review queue

```text
approval template
approval index
hash binding
promotion gate
derived review queue
```

## Phase 4 — Sessions

```text
start
events
explicit closeout
inactivity draft
resume
closeout template
```

## Phase 5 — Routing

```text
routing-policy.yml
ordered decision tree
matched-rule record
uncertainty escalation
```

## Phase 6 — Capture channels

Implement separately:

```text
local
Telegram
Web Clipper
AI session
execution evidence
```

## Phase 7 — Scheduler

```text
10-minute sync
22:00 nightly
persistent catch-up
no-op sync
startup refresh
```

## Phase 8 — Obsidian

```text
open existing repo
HOME.md
graph exclusions
profile documentation
Git-diff verification
```

## Phase 9 — LLM Wiki

```text
one-source ingest
source summary
concept proposal
link proposal
index
log
lint
promotion
```

No bulk ingest during acceptance.

## Phase 10 — End-to-end loop

```text
Earesmes captures issue
→ consultation job
→ ChatGPT or Claude
→ owner approval
→ execution job
→ Antigravity
→ evidence
→ Earesmes closeout and sync
→ proposal
→ owner approval
→ promotion
→ Obsidian display
```

## Phase 11 — Failure tests

Test:

```text
fake secret
duplicate source
duplicate job
double claim
stale claim
wrong approval hash
unauthorized promotion
bad AI summary
runtime conflict
WSL offline
post-22:00 progress
sync failure
push rejection
Git divergence
writer-lock contention
forced termination
orphan lock file
broken link
orphan note
```

---

# 26. Commit and Rollback

One bounded commit per phase or coherent subphase.

No unrelated cleanup.

Before runtime change:

```text
record current config
backup service or timer files
record enabled state
record HEAD
define rollback
```

Rollback restores previous files, scheduler state, service state, and repository consistency.

---

# 27. Acceptance Criteria

v0.5.1 is complete only when:

```text
[ ] v0.4.1 runtime acceptance is PASS.
[ ] Public-repository safety passes.
[ ] .private-local is excluded.
[ ] PRD hash is recorded.
[ ] airo-preflight passes.
[ ] BOOT lifecycle works.
[ ] Stale data is never presented as current.
[ ] Job lifecycle works.
[ ] Idempotency works.
[ ] Double claiming is blocked.
[ ] Approval records are durable and hash-bound.
[ ] Review queue is regenerable.
[ ] Unauthorized promotion fails.
[ ] Session lifecycle is deterministic.
[ ] Routing follows the decision tree.
[ ] Uncertain work escalates.
[ ] Capture channels enforce safety.
[ ] Writer lock blocks concurrent mutation.
[ ] Forced termination releases advisory lock.
[ ] Orphan lock file does not cause permanent blocking.
[ ] Unrelated owner edits are not staged.
[ ] Divergence does not cause automatic merge or force-push.
[ ] Sync targets every 10 minutes while available.
[ ] Nightly targets 22:00.
[ ] Missed work catches up once.
[ ] Post-22:00 progress is preserved.
[ ] Obsidian opens the existing repo.
[ ] HOME.md is operationally useful.
[ ] Graph excludes technical noise.
[ ] One-source ingest passes.
[ ] Full consultation-to-execution loop passes.
[ ] Semantic promotion with valid approval passes.
[ ] Abuse and failure tests pass.
```

---

# 28. Final Execution Report

Antigravity must report:

```text
PRD version
repository
starting HEAD
ending HEAD
phases completed
phases blocked
files created
files modified
services or timers changed
security tests
job tests
approval tests
writer-lock tests
scheduler tests
Obsidian tests
end-to-end tests
remaining limitations
rollback status
commits
push result
final status
```

Allowed final statuses:

```text
PASS
PASS_WITH_LIMITATIONS
BLOCKED
FAIL
```

---

# 29. No-Brainer Runbook

## ChatGPT or Claude

```text
read BOOT.md
validate bootstrap freshness
read active context and jobs
verify project
consult with owner
record decision
produce approval receipt
produce execution job
produce closeout
do not claim execution
```

## Antigravity

```text
read BOOT and PRD
read exact execution job
run preflight
check mode
acquire writer lock
capture before state
make bounded changes
validate
stop on failure
commit after PASS
push without force
store evidence
update job
```

## Earesmes

```text
monitor intake
capture events
classify deterministically
handle Class 1
draft Class 2
queue Class 3
track Class 4
create owner jobs for Class 5
sync
health
nightly processing
approved promotion
notifications
```

---

# 30. Non-Goals

v0.5.1 does not include:

```text
paid ChatGPT or Claude API integration
browser automation controlling web AI
processing while PC is powered off
automatic semantic approval
unrestricted AI write access
moving project code into Second Brain
capturing every browser or chat activity
bulk ingestion before single-source PASS
creating a second Obsidian vault
```

---

# 31. Final Execution Gate

Implementation may start only after:

```text
PRD exists at canonical path
owner-approved status is preserved
PRD hash or commit is recorded
Phase 0A declares READ_ONLY_AUDIT
```

The first implementation action is evidence collection.

No phase may be skipped silently.

No system may be declared operational without direct evidence.

---

# 32. Final Operating Model

```text
ChatGPT and Claude reason and consult.

The owner decides and approves.

Antigravity executes and proves.

Earesmes captures, routes, orchestrates,
synchronizes, monitors, and maintains continuity.

AIRO Second Brain stores canonical context and evidence.

Obsidian makes the same repository readable and navigable.
```
