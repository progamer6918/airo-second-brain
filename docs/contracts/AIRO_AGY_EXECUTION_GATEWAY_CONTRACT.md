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

1. **Classify** the command as Tier 2 per §2 and §4.
2. **Derive task slug**: `<project-short>_<verb>_<object>` — safe characters only.
3. **Confirm working directory** or use absolute wrapper path.
4. **Invoke wrapper**: `scripts/airo-vps-exec --task <slug> -- <command>`.
5. **Verify receipt fields** in output: `RESULT=`, `EXIT_CODE=`, `COPIED_TO_CLIPBOARD=`.
6. **Report receipt** in AGY response (do not fabricate fields not present in output).

---

## 6. Compliance & Enforcement

- Violation: AGY running a Tier 2 command without `airo-vps-exec` constitutes a
  **governance breach** under `AIRO_AGENT_ROLE_CONTRACT §4` and invalidates the session receipt.
- Tier 1 misclassification of a Tier 2 command: treated as governance breach.
- Wrapper failure (non-zero exit from wrapper itself, not from the wrapped command):
  AGY must stop, report the wrapper error, and not proceed as if delivery succeeded.
- Clipboard FAIL is NOT a Tier 2 blocker — wrapper exit code follows the underlying command.
  But `COPIED_TO_CLIPBOARD=NO` must be faithfully reported in the AGY receipt.

---

## 7. Relationship to Existing Contracts

| Contract | Relationship |
|---|---|
| `AIRO_AGENT_ROLE_CONTRACT.md §2.2` | This contract operationalizes Antigravity's "Evidence Collection" responsibility. |
| `AIRO_DIRECT_WSL_EXECUTION_CONTRACT §9–10` | This contract names the binding mechanism (airo-vps-exec) that satisfies those rules. |
| `AIRO_TERMINAL_RECEIPT_DELIVERY_CONTRACT` | Tier 2 flow is the enforcement mechanism for AUTO_COPY_REQUIRED=true. |
| `AIRO_EXECUTION_EVIDENCE_CONTRACT §8` | Tier 2 receipt provides the verifiable clipboard evidence chain. |
| `AIRO_CODE_CHANGE_CONTRACT` | Applies when implementing changes approved under this contract. |
| `scripts/airo-vps-exec` | Canonical Tier 2 entry point. Must not be modified to satisfy this contract. |

---

## 8. Scope Exclusions

This contract governs AGY (Antigravity) terminal execution only.

- **Earesmes / Hermes**: Not governed by this contract. Earesmes uses its own adapter chain.
- **ChatGPT direct WSL**: Governed by `AIRO_DIRECT_WSL_EXECUTION_CONTRACT` directly.
- **Automated background services** (telegram-gateway, etc.): Not governed by this contract.
- **airo-vps-exec internal logic**: This contract does not modify or extend the wrapper script.
