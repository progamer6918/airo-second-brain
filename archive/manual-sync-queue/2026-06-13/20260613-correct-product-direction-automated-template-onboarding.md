## 2026-06-13 — Correct Product Direction: Automated Template Onboarding

Status: processed
Source: owner-confirmed correction
Confidence: high
Related workstream: Report Automation VBA
Priority: critical

### Problem

The project direction drifted repeatedly toward manually completing one report such as Result VE.

That is not the final product objective.

The owner must not be asked to manually provide:

* sheet inventories;
* hidden-sheet screenshots;
* Query and Connection screenshots;
* Power Pivot screenshots;
* named-range screenshots;
* external-link details;
* staging-sheet analysis;
* formula dependency mapping;
* technical template structure.

Those are responsibilities of the Command Center onboarding system.

Requesting the owner to manually map a new template defeats the purpose of the product.

### Correct final product objective

Build a reusable Excel/VBA Command Center platform that can onboard new report templates with minimal technical input from the owner.

The intended workflow is:

```text
put template into template folder
→ register or select template
→ click Scan Template
→ Command Center opens template read-only
→ Command Center discovers technical structure
→ Command Center creates a draft mapping
→ admin confirms only unresolved business choices
→ Command Center validates mapping
→ report becomes READY
→ operator runs report from MULAI DI SINI
→ output is validated and logged
```

The platform must reduce technical work for the owner, not move technical mapping work from VBA into screenshots or manual chat instructions.

### Owner input boundary

The owner may be asked only for business decisions that cannot be derived safely from the workbook.

Valid owner questions:

```text
Which candidate sheet is the intended final report?
Which visible date should appear on the report?
Which business source is authoritative when two candidates exist?
Should this report be active for daily production?
```

Invalid owner requests:

```text
List all hidden sheets.
Screenshot all workbook connections.
Map formula dependencies manually.
Identify staging ranges manually.
Inspect Power Pivot tables manually.
Explain the internal workbook structure.
```

Technical discovery must be performed by the Command Center or by an automated read-only scanner.

### Correct next milestone

Previous milestone wording:

```text
RPT003 Result VE read-only mapping audit
```

Correct milestone wording:

```text
Automated Template Onboarding and Mapping Engine
```

Result VE is only the first proof case.

It is not the product goal.

### Required onboarding capabilities

The Command Center must be able to inspect a registered template read-only and collect:

* workbook identity;
* file hash;
* sheet names;
* sheet visibility;
* used ranges;
* named ranges;
* Excel Tables;
* PivotTables;
* PivotCaches;
* workbook connections;
* query metadata;
* QueryTables;
* external workbook links;
* Data Model indicators;
* formula locations;
* formula errors;
* likely staging sheets;
* likely final-output sheets;
* likely report-date cells;
* source dependencies;
* current report-family compatibility;
* required validation rules.

### Required configuration structures

The onboarding layer should create or maintain generic configuration structures such as:

```text
CC_TEMPLATE_DISCOVERY
CC_MAPPING_DRAFT
CC_REPORT_SOURCE_MAP
CC_REPORT_TARGET_MAP
CC_REPORT_EXEC_RULES
CC_REPORT_VALIDATION
CC_REPORT_FAMILY
```

Exact names may change after design review, but the architecture must remain generic and reusable.

Do not hardcode onboarding logic only for RPT003.

### Required status lifecycle

A newly registered report must move through a controlled lifecycle:

```text
DISCOVERED
→ NEEDS REVIEW
→ MAPPING REQUIRED
→ MAPPING VALIDATED
→ READY
→ ACTIVE
```

Unsafe templates may become:

```text
BLOCKED
```

The system must explain:

* what was discovered;
* what is missing;
* what can be inferred safely;
* what requires owner confirmation;
* why activation is blocked;
* what action moves the report to the next state.

### Current product status correction

R8.11 is a stable operational baseline for the existing report engine.

V1 RC1 / R8.13 proves:

* operator workflow;
* dynamic source registry;
* dynamic report registry;
* RPT001 execution;
* RPT002 execution;
* readiness classification;
* runtime evidence;
* process summary;
* persistence.

However, the platform is not yet complete as a reusable onboarding product.

Current truthful status:

```text
Existing report operation = PASS
Admin readiness checker = PASS
Automated template discovery = NOT COMPLETE
Automated mapping draft = NOT COMPLETE
Generic new-report onboarding = NOT PROVEN
Reusable product platform = NOT COMPLETE
```

Do not label the full platform production-ready until a previously unsupported template is onboarded through the product workflow.

### Proof-of-product requirement

The platform may be called complete only after this flow is demonstrated:

```text
new unsupported template
→ automatic read-only discovery
→ draft mapping generated
→ minimal business confirmation
→ validated mapping stored
→ report classified READY
→ report executed through Command Center
→ output validated
→ status and evidence persisted
```

Result VE may be used as the first proof case, but implementation must remain generic.

### Development rule

Do not request manual technical evidence from the owner when the workbook is available to the Command Center.

Do not shift technical discovery work back to the owner.

Do not narrow the project to completing one report.

Do not claim the product is finished because RPT001 and RPT002 work.

Do not modify the frozen R8.11 baseline directly.

New development must use a copied candidate.

### Correct roadmap position

Completed:

```text
Existing report engine
Operator workflow
Dynamic registries
Import resilience
Runtime evidence
Admin readiness classification
```

Active:

```text
Automated Template Onboarding and Mapping Engine
```

After that:

```text
proof onboarding with an unsupported template
→ generic execution-family validation
→ final product acceptance
→ production release
```

### Canonical update requested

When this capture is processed:

1. Update `projects/report-automation-vba.md`.
2. Update the active milestone in `CURRENT.md`.
3. Update `state/active-context.md`.
4. Replace RPT003-centric wording with platform-centric onboarding wording.
5. Keep Result VE only as a proof case.
6. Record the owner-input boundary.
7. Record that the platform is not production-complete yet.
8. Preserve R8.11 as the frozen operational baseline.
9. Do not mark this capture processed until canonical readback is verified.

### AIRO operator rule

Future AIRO operators must remember:

```text
The owner supplies business intent.
The product discovers technical workbook structure.
The product generates mapping evidence.
The owner confirms only unresolved business choices.
```

Do not ask the owner to perform the product’s intended technical work.
