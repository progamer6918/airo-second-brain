- Council Deep increases evidence depth rather than verbosity by default;
- automatic Council requires Owner confirmation before execution;
- declined automatic suggestions are not repeatedly offered without material context change;
- AIRO source priority remains authoritative;
- Council output does not disclose private chain-of-thought.

## V1 Change Policy

Council Mode v1 should remain small.

Do not add new lenses, triggers, output ceremonies, or automatic behavior merely because additional possibilities can be imagined.

Change v1 only from:

- concrete Owner usage evidence;
- a proven material blind spot;
- a material change in the surrounding AIRO operating model.

<!-- SOURCE_END state/operating-rules/AIRO_COUNCIL_MODE.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_CODE_CHANGE_CONTRACT.md -->

# Source: docs/contracts/AIRO_CODE_CHANGE_CONTRACT.md

# AIRO Senior Engineer Code Change Contract

## Status

Owner-approved canonical engineering contract.

## Purpose

This contract defines the default engineering discipline for AI-generated changes that can alter executable behavior in the AIRO ecosystem.

The objective is:

**the smallest correct, safe, clear, maintainable change that solves the real requirement.**

The objective is not minimum line count.

This contract is informed by senior-engineering minimal-change principles, including ideas popularized by tools such as Ponytail, but ASB remains the canonical authority.

No external tool or upstream ruleset may silently redefine this contract.

## Applicability

This contract applies when a task changes or can materially affect:

- executable application code;
- scripts;
- automation logic;
- runtime behavior;
- parsers;
- integrations;
- deployment logic;
- data mutation logic;
- configuration whose value changes executable/runtime behavior.

It does not need to be invoked as a heavyweight review process for ordinary:

- documentation edits;
- notes;
- PR/deferred-work text;
- navigation text;
- purely editorial SOP wording;
- formatting-only changes.

Existing specialized safety and project contracts still apply where relevant.

This contract does not replace them.

## 1. Understand Before Editing

Do not patch code from the symptom description alone.

Before implementation:

1. identify the real execution path affected;
2. inspect the smallest relevant caller/callee set;
3. determine the current ownership point for the behavior;
4. identify the expected behavior;
5. identify the actual failure or requirement gap.

Do not perform a broad repository audit when the relevant flow is already bounded.

Understanding must be proportional to the task.

## 2. Root Cause Over Symptom

Prefer fixing the responsible ownership point rather than layering a workaround at the visible symptom.

A symptom-level patch is acceptable only when:

- the true root cannot safely be changed within scope; or
- the symptom boundary is itself the correct ownership point.

Do not expand scope merely to pursue a theoretically purer architecture.

## 3. Need-to-Exist Test

Before creating new code, ask:

`Does this need to exist at all?`

Valid outcomes include:

- no code change required;
- configuration change only;
- reuse existing behavior;
- delete obsolete behavior;
- small direct implementation.

A verified no-change outcome is a valid engineering success.

## 4. Reuse Ladder

Before writing a new abstraction or dependency, evaluate in this order:

1. Does equivalent functionality already exist in the repository?
2. Can the standard library solve it clearly?
3. Can the native platform/runtime solve it clearly?
4. Can an already-approved existing dependency solve it without abuse?
5. Can a small local implementation solve it cleanly?
6. Only then consider a new abstraction or dependency.

Do not skip earlier steps merely because generating new code is easy.

## 5. Minimum Correct Diff

Prefer the smallest diff that fully satisfies:

- requirement;
- correctness;
- safety;
- readability;
- maintainability;
- relevant canonical contracts.

Smallest diff does not mean smallest character count.

Do not code-golf.

Four obvious lines are better than one clever line when the four-line version is materially clearer.

The target is:

**minimum unnecessary complexity.**

## 6. No Premature Abstraction

Do not introduce abstractions without concrete need.

Examples that require justification include:

- manager classes;
- factories;
- new service layers;
- repository layers;
- generic frameworks;
- plugin systems;
- wrapper hierarchies;
- generalized configuration systems;
- helper stacks created for one trivial call site.

One concrete use case does not automatically require a generalized abstraction.

Abstraction should remove proven duplication or encode a stable boundary, not anticipate hypothetical future requirements.

## 7. Dependency Discipline

A new dependency requires explicit technical justification.

Do not add a package merely to save a few trivial lines of code.

Before adding a dependency, verify that:

- stdlib/native capability is materially inadequate;
- existing approved dependencies are materially inadequate;
- the new dependency meaningfully improves correctness, safety, interoperability, or maintainability;
- lifecycle/security cost is acceptable.

Tool availability alone is not justification.

## 8. No Opportunistic Refactor

Do not combine the requested change with unrelated cleanup.

If the task is to repair A, do not automatically refactor B, rename C, reorganize D, and modernize E.

Adjacent change is allowed only when it is materially required for the correctness, safety, or testability of the requested objective.

Potential improvements outside scope should remain outside the patch unless separately approved.

## 9. Preserve Existing Architecture Where Reasonable

Prefer the repository's existing stable patterns over introducing a personal preferred architecture.

Do not replace a working local pattern solely because another pattern is more fashionable.

Architecture change requires a material reason such as:

- correctness;
- security;
- maintainability at actual scale;
- proven duplication;
- required capability;
- removal of a known structural defect.

## 10. Safety Is Non-Negotiable

Minimalism must never be used to remove required safeguards.

Do not eliminate materially necessary:

- trust-boundary validation;
- authentication or authorization controls;
- input validation;
- data-loss prevention;
- financial correctness;
- concurrency correctness;
- idempotency;
- rollback/recovery protections;
- required error handling;
- required auditability;
- required observability;
- accessibility where applicable.

A smaller unsafe patch is worse engineering.

## 11. Error Handling Must Be Proportional

Handle failures that can materially occur at the relevant boundary.

Do not add speculative error frameworks for impossible or already-contained conditions.

Do not suppress meaningful errors merely to keep code short.

Errors should fail at the narrowest useful boundary with enough information for deterministic diagnosis while preserving security/privacy rules.

## 12. Testing Must Be Proportional

Testing should prove the changed behavior at the smallest durable level that can catch regression.

For non-trivial logic changes, prefer a regression check that would fail if the repaired behavior breaks again.

Do not create a large new test framework for a trivial deterministic change when an existing test surface is sufficient.

Do not treat test count as a quality metric.

The relevant question is:

`Would the available evidence detect regression of this behavior?`

## 13. Diff-Scoped Senior Review

Before final acceptance of an executable-code change, perform one bounded review of the actual task diff.

This is not a second project, second session, or broad repository audit.

Check:

- Can anything unnecessary be deleted?
- Is any new code duplicating existing functionality?
- Was the reuse ladder followed?
- Is any abstraction premature?
- Was a new dependency actually necessary?
- Did the change address the real ownership point/root cause?
- Did the diff touch unrelated scope?
- Did simplification remove any safety property?
- Is the result clear and boring enough for another maintainer to understand quickly?
- Is the regression evidence proportional and meaningful?

If the diff already passes these questions, continue.

Do not invent another review milestone merely to satisfy this contract.

## 14. Architecture Escalation

If implementation discovers a genuine strategic or architectural decision that was not already resolved, stop treating it as ordinary execution.

Return the decision to the intelligence/planning layer.

Council Mode may be suggested when the decision meets its materiality threshold, but Council is not a mandatory coding gate.

Antigravity must not resolve material architecture trade-offs independently.

## 15. External Tool Independence

External tools such as Ponytail may be used as optional implementation or review aids when explicitly approved.

They are not canonical authorities.

An upstream tool update must not automatically change AIRO engineering behavior.

Do not install or maintain an external code-review tool unless there is a demonstrated benefit that the canonical contract and existing executor workflow cannot reasonably provide.

## 16. Executor Behavior

For approved implementation work, the executor should generally follow:

`UNDERSTAND → IMPLEMENT MINIMUM CORRECT CHANGE → TEST → DIFF-SCOPED SENIOR REVIEW → FINAL VERIFY`

Do not turn this sequence into multiple artificial project gates when no Owner decision is required.

Do not repeatedly rescan unchanged repository areas.

Do not rerun expensive verification without a concrete reason.

## 17. Completion Invariants

An executable-code change is engineering-complete only when:

- the relevant behavior/root cause is understood;
- the resulting diff is scoped to the objective;
- unnecessary new code and abstractions have been avoided;
- new dependencies, if any, have explicit justification;
- required safety properties remain intact;
- appropriate regression evidence passes;
- the final diff has undergone bounded senior review;
- no known directly related defect remains hidden behind a green script result.

A larger diff can be correct.

A smaller diff can be wrong.

The contract optimizes for **minimum justified complexity**, not minimum size.

<!-- SOURCE_END docs/contracts/AIRO_CODE_CHANGE_CONTRACT.md -->

<!-- SOURCE_BEGIN docs/contracts/AIRO_AGY_EXECUTION_GATEWAY_CONTRACT.md -->

# Source: docs/contracts/AIRO_AGY_EXECUTION_GATEWAY_CONTRACT.md

last_updated: 2026-09-01
updated_by: Antigravity / AIRO Workflow Contract Hardening
status: APPROVED / CANONICAL
confidence: owner-confirmed
authority: OPTION_C_APPROVED — Hybrid Two-Tier Execution Model
source: AIRO_WORKFLOW_CONTRACT_HARDENING

# AIRO AGY Execution Gateway Contract

## 1. Purpose

This contract defines the mandatory two-tier execution model for Antigravity (AGY) terminal
operations within the AIRO ecosystem on the native VPS runtime.

It closes the enforcement gap identified in `AIRO_WORKFLOW_CONTRACT_HARDENING`: the existing
clipboard, tee-capture, and receipt delivery mandates (AGENTS.md §Default Command-Output Clipboard
Copy Rule; AIRO_DIRECT_WSL_EXECUTION_CONTRACT §9–10; AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT) were
contractually required but had no binding entry-point mechanism for AGY executions.

Existing scripts are reused unchanged. No new execution logic is introduced.

---

## 2. Two-Tier Execution Model

### Tier 1 — Inspection Execution

**Definition**: Read-only, non-mutating, diagnostic or evidence-gathering commands that produce no
Owner-facing deliverable requiring clipboard transport.

**Allowed execution method**: Direct `run_command`. No wrapper required.

**Tier 1 examples** (non-exhaustive):
- `ls`, `find`, `stat`, `file`
- `cat`, `head`, `tail`, `less`
- `grep`, `rg`, `awk`, `sed` (read-only pipelines)
- `git status`, `git log`, `git diff`, `git show`
- `echo`, `which`, `type`, `env`, `printenv`
- `python3 <script> --dry-run` or `--help`
- Health and preflight checks: `scripts/airo-health`, `scripts/airo-preflight`
- `wc`, `sort`, `uniq`, `diff` (read-only)

**Tier 1 is NOT permitted when**:
- The output is intended as Owner-facing delivery to clipboard.
- The command mutates any file, index, or repository state.
- The classification is ambiguous (default to Tier 2; see §4).

---

### Tier 2 — Controlled Execution (Gateway Required)

**Definition**: Any command that mutates state, executes a project script with side effects,
performs a git operation that changes history or remote state, or produces Owner-facing output
that must be delivered via the canonical receipt flow.

**Required execution method**: `scripts/airo-vps-exec` gateway.

**Tier 2 examples** (non-exhaustive):
- Any `git commit`, `git push`, `git merge`, `git rebase`, `git stash`
- Any file write, create, or delete operation via shell
- Running project scripts (`scripts/airo-sync`, `scripts/airo-capture`, `scripts/airo-promote`, etc.)
- Test suite execution where results are Owner-facing evidence
- `python3 <script>` without `--dry-run` where the script has known side effects
- Any command whose output constitutes the deliverable for an AIRO task receipt
- Deployment, migration, or service restart operations

**Tier 2 mandatory invocation template**:

```bash
/home/ubuntu/AI_WORKSPACES/airo-second-brain/scripts/airo-vps-exec \
  --task <PROJECT_SLUG>_<TASK_SLUG> \
  -- <command> [args...]
```

**Working directory requirement**: AGY must invoke `airo-vps-exec` from the repo root
`/home/ubuntu/AI_WORKSPACES/airo-second-brain/` OR use the absolute path to the script.
The wrapper resolves sibling scripts (`airo-clipboard-receipt`, `airo-remote-clipboard`,
`airo-receipt-publish`) relative to its own `SCRIPT_DIR/../`, which requires the repo
root to be resolvable.

**Task slug rules** (enforced by wrapper):
- Format: `[A-Za-z0-9._-]+`
- Convention: `<project-short>_<verb>_<object>` (e.g. `airo_deploy_gateway_contract`)
- Maximum practical length: 60 characters

---

## 3. Execution Flow (Tier 2)

```text
AGY (run_command)
  └─▶ scripts/airo-vps-exec --task <slug> -- <command>
        ├─▶ command executes (argv, no eval)
        ├─▶ stdout+stderr captured via tee → /tmp/airo_<slug>_<ts>.txt
        ├─▶ scripts/airo-clipboard-receipt (Windows/clip.exe path, if available)
        ├─▶ scripts/airo-remote-clipboard (OSC52 fallback, if Windows path unverified)
        ├─▶ AIRO_LAST_RECEIPT.txt written → /home/ubuntu/AIRO_LAST_RECEIPT.txt
        ├─▶ scripts/airo-receipt-publish → .airo/receipts/latest.md + archive/
        └─▶ exit code = underlying command exit code
```

Satisfies:
- `AGENTS.md §Default Command-Output Clipboard Copy Rule` (tee + clipboard-receipt mandatory)
- `AIRO_DIRECT_WSL_EXECUTION_CONTRACT §9–10` (tee to /tmp, clipboard delivery)
- `AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT` (AUTO_COPY_REQUIRED=true, PRIMARY_METHOD=OSC52)
- `AIRO_EXECUTION_EVIDENCE_CONTRACT §8` (verified readback mandatory)

---

## 4. Classification Rules

### Default
When tier classification is ambiguous, **default to Tier 2**.

### Override conditions
A command is Tier 2 regardless of surface form if **any** of the following apply:
1. It writes, creates, deletes, or renames any file.
2. It executes a non-`--dry-run` project script with known side effects.
3. It performs any git operation that changes refs, index, or remote state.
4. Its output is the primary evidence artifact for an AIRO task verdict.
5. The Owner prompt specifies it as a delivery step.

### Classification is NOT affected by:
- Whether the command is wrapped in `bash -c`.
- Whether the command is a pipeline.
- Whether exit code is expected to be nonzero.

---

## 5. AGY Execution Checklist (Tier 2)

Before each Tier 2 execution, AGY MUST:

