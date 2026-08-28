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
