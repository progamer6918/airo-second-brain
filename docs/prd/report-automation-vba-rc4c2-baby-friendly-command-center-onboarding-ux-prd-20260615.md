# PRD Addendum RC4C2 — Baby-Friendly Command Center Onboarding UX

Subtitle: Controlled Reopening, RC4C UX Status Correction, Stale Roadmap Label Correction, and No-Brainer Procedure Cards

Date: 2026-06-15  
Project: Honda Report Automation VBA / Command Center  
Execution target: Antigravity  
Document type: PRD Addendum + Procedure Annex  
Status: Approved for controlled documentation commit  
Final target classification: `RC4C2_BABY_FRIENDLY_COMMAND_CENTER_UX_ACCEPTED`

---

## 1. Document Treatment

This document is not a replacement of the original Report Automation VBA PRD.

This document is:

1. PRD Addendum.
2. Canonical Status Correction.
3. Owner-approved Controlled Reopening.
4. Stale Roadmap Label Correction.
5. No-Brainer Toolchain & Procedure Annex.

This document does not roll back RC3S.

RC3S remains the accepted 3-report operator-safe baseline.

Accepted reports remain:

- RPT001 Monitoring Dealer.
- RPT002 Report Per Type.
- RPT003 Result VE.

Existing do-not-regress rules remain active:

- Do not remove `CC_MASTER_DATA_MD` from `03_Report_Templates\Result VE.xlsm`.
- Do not overwrite patched `Result VE.xlsm` with an old template.
- Do not reintroduce multiple macro retry loop into `AIRO_LOCAL_RUNNER.ps1`.
- Do not use hardcoded `Report_Registry`.
- Use `CC_REPORT_REGISTRY`.
- Do not restart Result VE debugging unless new evidence invalidates RC3S.

---

## 2. Canonical Status Correction

RC4C technical onboarding entrypoint remains accepted.

RC4C baby-friendly UX claim is revised to:

`PARTIAL / NOT PASS`

Reason:

The existing onboarding/admin flow still exposes technical registry fields such as:

- SourceKey
- ReportID
- Family
- AuditClass
- RunMode
- HeaderProfile
- DateRule
- UsedByReports

These are internal engine fields, not baby-friendly user-facing fields.

RC4C2 supersedes only the RC4C baby-friendly UX acceptance claim.

RC4C2 does not invalidate:

- RC3S final freeze.
- RPT001/RPT002/RPT003 accepted runtime.
- BBN optional source acceptance.
- RC4E no fake RPT004 guardrail.
- Existing Command Center architecture.

---

## 3. Controlled Reopening Rule

Previous handover mode remains the default:

`stop patching; use SOP and intake form`

RC4C2 is an explicit owner-approved controlled reopening.

Allowed scope:

1. Step 0 Second Brain documentation package.
2. Step 1 workbook SHA check and UX reality audit.
3. Step 2 generic standard template engine proof.
4. Step 3 baby-friendly onboarding wrapper only if Gate 2 allows.
5. Step 4 regression and QA cleanup.
6. Step 5 freeze cleaned candidate.

Forbidden scope:

- Open-ended patching.
- One-off report debugging.
- Runtime patching without proof.
- Editing original workbook directly.
- Creating fake RPT004.
- Promoting QA reports as production reports.
- Rewriting original PRD.
- Rewriting old roadmap.
- Updating `decisions/decision-log.md`.
- Renaming existing workbook sheets without owner approval.

---

## 4. Stale Roadmap Label Correction

The historical roadmap file:

`docs/roadmap/report-automation-vba-rc4-self-service-onboarding-roadmap.md`

defines RC4B-RC4E differently from the executed/frozen 2026-06-14 RC4 tracks.

Historical roadmap definitions:

- RC4B = Registry Schema V2.
- RC4C = Onboarding Wizard.
- RC4D = Template Audit Engine.
- RC4E = Mapping Compiler.

Executed/frozen 2026-06-14 definitions:

- RC4B = No-Reseed Product Ready Freeze.
- RC4C = Onboarding UX Product Ready / `CC_ONBOARDING` entrypoint.
- RC4D = BBN Real Onboarding Accepted.
- RC4E = No Valid New Report Target / Guardrail / No Fake RPT004.

Decision:

The old roadmap is historical/superseded for RC4B-RC4E letter naming.

RC4C2 refers only to the executed/frozen RC4C onboarding UX baseline from 2026-06-14.

RC4C2 does not refer to the old roadmap's RC4C "Onboarding Wizard" scope.

---

## 5. No-Brainer Execution Rule

Every step is one separate Antigravity session.

At the end of every step:

1. Write evidence.
2. Write final classification.
3. Stop completely.

Do not continue to the next step automatically, even if PASS.

The next step starts only after explicit Owner instruction, for example:

`lanjut Step 2`

No gate chaining is allowed.

---

## 6. Step / Gate Map

| Step | Gate | Name | Session Rule |
|---|---|---|---|
| Step 0 | None | Second Brain documentation only | Stop after docs commit |
| Step 1 | Gate 1 | Workbook SHA check + UX reality audit | Stop after audit evidence |
| Step 2 | Gate 2 | Generic standard template engine proof | Stop after proof evidence |
| Step 3 | Gate 3 | Baby-friendly UX wrapper | Stop after UX evidence |
| Step 4 | Regression | RPT001/RPT002/RPT003 + QA cleanup | Stop after regression evidence |
| Step 5 | Freeze | Final cleaned candidate freeze | Stop after freeze evidence |

---

## 7. Global Paths

Project root:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package`

Original workbook:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package\00_Command_Center\Command_Center_LATEST_USE_THIS.xlsm`

Expected original workbook SHA256:

`B13C581F1CA9B37EB6E5F92144028F818490026E07A89A85C88625FCE8B2058A`

RC4C2 local work root:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package\04_Working_Output\RC4C2`

RC4C2 log root:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package\05_Log\RC4C2`

Persistent candidate workbook:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package\04_Working_Output\RC4C2\Command_Center_RC4C2_CANDIDATE.xlsm`

Candidate state file:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package\04_Working_Output\RC4C2\CANDIDATE_STATE.json`

QA template folder:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package\04_Working_Output\RC4C2\qa_templates`

QA source folder:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package\04_Working_Output\RC4C2\qa_sources`

QA output folder:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package\04_Working_Output\RC4C2\qa_output`

QA archive folder:

`D:\Randas\Others\Honda_Report_Automation_Pilot_Package\04_Working_Output\RC4C2\archive`

Second Brain validation summary folder:

`docs/validation`

Second Brain blocker folder:

`inbox`

---

## 8. Global Stop Artifact

Every STOP must write:

`inbox/report-automation-vba-rc4c2-blocker-step<N>-<timestamp>.md`

Required blocker content:

```md
# RC4C2 Blocker

step:
gate:
timestamp:
final_classification:
reason:
expected:
actual:
files_touched:
files_not_touched:
candidate_sha256_before:
candidate_sha256_after:
recommended_owner_decision:
After blocker is written:

Stop.
Do not patch workbook.
Do not continue gate.
Do not make additional changes.
Report final classification in chat.

No Telegram or gateway notification is required.

Owner checks inbox/chat manually.

9. Global Evidence Schema

Each step must create local evidence:

05_Log\RC4C2\AIRO_RC4C2_STEP<N>_<timestamp>.txt

05_Log\RC4C2\AIRO_RC4C2_STEP<N>_<timestamp>.json

Each step must create Second Brain summary:

docs/validation/report-automation-vba-rc4c2-step<N>-<timestamp>.md

Minimum evidence fields:

{
  "step": "",
  "gate": "",
  "timestamp": "",
  "classification": "",
  "original_workbook_path": "",
  "original_workbook_sha256": "",
  "candidate_workbook_path": "",
  "candidate_sha256_before": "",
  "candidate_sha256_after": "",
  "files_created": [],
  "files_modified": [],
  "files_forbidden_but_checked": [],
  "macros_called": [],
  "excel_process_count_before": 0,
  "excel_process_count_after": 0,
  "stop_reason": "",
  "next_allowed_step": ""
}
10. Excel COM Rule

Every step that opens Excel must verify no Excel process before and after the gate.

If Excel exists before the gate:

RC4C2_BLOCKED_EXCEL_ALREADY_OPEN

If Excel remains after the gate:

RC4C2_BLOCKED_EXCEL_ORPHAN_AFTER_GATE

Do not kill Excel automatically.

Write blocker.

STEP 0 — Second Brain Documentation Only
Purpose

Record RC4C2 PRD addendum and canonical status correction before any workbook work.

Session Rule

Step 0 is one Antigravity session.

Stop after commit or blocker.

Do not open Excel.

Do not touch workbook.

Do not check workbook SHA.

Allowed Files To Create
docs/prd/report-automation-vba-rc4c2-baby-friendly-command-center-onboarding-ux-prd-20260615.md
decisions/report-automation-vba-rc4c2-controlled-reopening-and-ux-status-correction-20260615.md
updates/report-automation-vba-rc4c2-baby-friendly-ux-prd-approved-20260615.md
docs/validation/report-automation-vba-rc4c2-step0-documentation-<timestamp>.md
Allowed Append-Only Files
projects/report-automation-vba.md
CURRENT.md
state/active-context.md

Owner pre-approves append-only updates to these three files only for RC4C2 pointers.

Forbidden Files
decisions/decision-log.md
docs/roadmap/report-automation-vba-rc4-self-service-onboarding-roadmap.md
00_Command_Center\Command_Center_LATEST_USE_THIS.xlsm
03_Report_Templates\*
04_Working_Output\*
tools\airosync\AIRO_LOCAL_RUNNER.ps1
Step 0 Pass Criteria
PRD addendum file exists.
Decision file exists.
Update file exists.
Step 0 validation summary exists.
Three canonical files are append-only updated.
No workbook file touched.
No roadmap rewrite.
No decision-log.md update.
Git push succeeds.

Final classification:

SECOND_BRAIN_RC4C2_DOCUMENTATION_PACKAGE_COMMITTED

STEP 1 / GATE 1 — Workbook SHA Check + UX Reality Audit

Step 1 is one Antigravity session.

Toolchain:

PowerShell + Excel COM Interop.

Open workbook read-only.

No VBA import.

No macro execution.

No workbook save.

First action:

Verify original workbook SHA256 equals:

B13C581F1CA9B37EB6E5F92144028F818490026E07A89A85C88625FCE8B2058A

If mismatch:

RC4C2_BLOCKED_WORKBOOK_SHA_MISMATCH

Audit required:

Workbook path.
Workbook SHA256.
Workbook opened read-only status.
All sheet names.
Sheet visible / hidden / very hidden status.
Sheet protection status.
UsedRange row count and column count per sheet.
Shapes/buttons on MULAI DI SINI.
Button text/caption.
Assigned macro for each button.
Exact button related to Bersihkan Data Lama or equivalent.
Shapes/buttons on PENGATURAN SISTEM.
Current CC_ONBOARDING fields.
Current CC_SOURCE_REGISTRY headers.
Current CC_REPORT_REGISTRY headers.
Whether CC_REPORT_REGISTRY has ReportID.
Whether CC_REPORT_REGISTRY has Enabled.
Whether CC_SOURCE_REGISTRY supports absolute folder/path values.
Whether CC_CheckInputs appears per-report or global.
Whether required macros exist:
CC_OnboardAddReport
CC_OnboardAddSource
CC_SetupCommandCenter
CC_CheckInputs
CC_RunSelectedReports
CC_CreateProcessSummary

If Step 1 cannot prove whether CC_CheckInputs is per-report or global, assume global.

Step 1 success:

WORKBOOK_UX_REALITY_AUDIT_COMPLETE

STEP 2 / GATE 2 — Generic Standard Template Engine Proof

Purpose:

Prove or disprove whether current Command Center can execute a new standard raw -> pivot -> final report template without runtime patching.

Gate 2 does not build new engine.

Gate 2 does not patch VBA.

Gate 2 does not touch original workbook.

Toolchain:

PowerShell + Excel COM Interop.

Use persistent candidate workbook only.

Allowed macros:

CC_OnboardAddReport
CC_OnboardAddSource
CC_SetupCommandCenter
CC_CheckInputs
CC_RunSelectedReports
CC_CreateProcessSummary

Candidate workbook:

04_Working_Output\RC4C2\Command_Center_RC4C2_CANDIDATE.xlsm

Copy source:

00_Command_Center\Command_Center_LATEST_USE_THIS.xlsm

Do not save original.

Do not write original.

Do not patch original.

QA IDs:

Test A = RPT901 / SRC901
Test B = RPT902 / SRC902A / SRC902B

If any ID already exists:

RC4C2_BLOCKED_QA_ID_COLLISION

QA source folder must be isolated:

04_Working_Output\RC4C2\qa_sources\

Do not use production Today folder.

If isolated QA folder is unsupported:

GENERIC_STANDARD_TEMPLATE_ENGINE_NOT_YET_PROVEN_QA_SOURCE_ISOLATION_UNSUPPORTED

QA Template A:

File: 04_Working_Output\RC4C2\qa_templates\QA_RPT901_SINGLE_BLOCK.xlsx
Source: 04_Working_Output\RC4C2\qa_sources\SRC901_DATA.xlsx
Sheets: DATA_MENTAH, PIVOT_TEST, LAPORAN_FINAL
Headers: Tanggal, Item, Qty
Pivot rows: Item
Pivot values: Sum of Qty
Area Tempel Hasil Pivot: LAPORAN_FINAL!A5
Named range: RC4C2_AREA_PIVOT_1
OutputPrefix: QA_RPT901

QA Template B:

File: 04_Working_Output\RC4C2\qa_templates\QA_RPT902_MULTI_BLOCK.xlsx
Sources:
SRC902A_DATA.xlsx
SRC902B_DATA.xlsx
Sheets:
DATA_MENTAH_A
PIVOT_A
DATA_MENTAH_B
PIVOT_B
LAPORAN_FINAL
Block 1 Area Tempel Hasil Pivot: LAPORAN_FINAL!A5
Named range: RC4C2_AREA_PIVOT_1
Block 2 Area Tempel Hasil Pivot: LAPORAN_FINAL!A20
Named range: RC4C2_AREA_PIVOT_2
OutputPrefix: QA_RPT902

Toggle rule:

Assume CC_CheckInputs is global unless Step 1 proves otherwise.

During Test A:

RPT001 = OFF
RPT002 = OFF
RPT003 = OFF
RPT901 = ON
RPT902 = OFF

During Test B:

RPT001 = OFF
RPT002 = OFF
RPT003 = OFF
RPT901 = OFF
RPT902 = ON

Toggle method:

Edit Enabled column in CC_REPORT_REGISTRY inside candidate workbook only.

QA output must be moved to:

04_Working_Output\RC4C2\qa_output\

Gate 2 success if both Test A and Test B pass:

GENERIC_STANDARD_TEMPLATE_ENGINE_PROVEN

Gate 2 engine not proven:

GENERIC_STANDARD_TEMPLATE_ENGINE_NOT_YET_PROVEN

STEP 3 / GATE 3 — Baby-Friendly UX Wrapper

Use same persistent candidate workbook.

Do not create a new candidate.

If Gate 2 = GENERIC_STANDARD_TEMPLATE_ENGINE_PROVEN, Gate 3 may build full baby-friendly onboarding wrapper.

If Gate 2 = GENERIC_STANDARD_TEMPLATE_ENGINE_NOT_YET_PROVEN, Gate 3 may build intake/audit wrapper only and must not claim automatic new-report execution.

Required user-facing sheet:

TAMBAH REPORT / DATA

Existing sheet roles:

MULAI DI SINI = daily user
PENGATURAN SISTEM = admin/reviewer/advanced
CC_* sheets = internal/advanced

Use user-facing terms:

Halaman laporan final
Data wajib
Data tambahan
Blok Proses Pivot
Area Tempel Hasil Pivot
Cek Template
Coba Jalankan
Kirim untuk Disetujui
Status Onboarding

Do not expose:

SourceKey
ReportID
Family
EngineProfile
AuditClass
RunMode
HeaderProfile
DateRule
UsedByReports

Step 3 success if engine proven:

BABY_FRIENDLY_ONBOARDING_WRAPPER_READY

Step 3 success if engine not proven:

BABY_FRIENDLY_INTAKE_WRAPPER_READY_ENGINE_NOT_PROVEN

STEP 4 — Regression + QA Cleanup

Use same persistent candidate workbook.

Archive candidate before cleanup:

04_Working_Output\RC4C2\archive\Command_Center_RC4C2_CANDIDATE_BEFORE_QA_CLEANUP_<timestamp>.xlsm

Clean main candidate:

Remove or disable RPT901.
Remove or disable RPT902.
Remove or disable SRC901.
Remove or disable SRC902A.
Remove or disable SRC902B.
Confirm RPT001 ON.
Confirm RPT002 ON.
Confirm RPT003 ON.
Confirm no QA output remains in root 04_Working_Output.
Confirm QA templates/sources remain only under 04_Working_Output\RC4C2.

If QA rows remain active before freeze:

RC4C2_BLOCKED_QA_ROWS_STILL_PRESENT_BEFORE_FREEZE

Regression reports:

RPT001.
RPT002.
RPT003.

Allowed macros:

CC_SetupCommandCenter
CC_CheckInputs
CC_RunSelectedReports
CC_CreateProcessSummary

Step 4 success:

RC4C2_REGRESSION_AND_QA_CLEANUP_ACCEPTED

STEP 5 — Freeze

Start condition:

Step 4 final classification must be:

RC4C2_REGRESSION_AND_QA_CLEANUP_ACCEPTED

Freeze folder:

99_ACCEPTED_FREEZE\AIRO_RC4C2_BABY_FRIENDLY_COMMAND_CENTER_UX_<timestamp>

Zip:

99_ACCEPTED_FREEZE\AIRO_RC4C2_BABY_FRIENDLY_COMMAND_CENTER_UX_<timestamp>.zip

Freeze contents:

Cleaned candidate workbook.
Step 0 validation summary.
Step 1 audit evidence.
Step 2 engine proof evidence.
Step 3 UX wrapper evidence.
Step 4 regression and cleanup evidence.
Step 5 freeze manifest.
QA archive folder as evidence only.
No active QA rows in final candidate.

Step 5 success:

RC4C2_BABY_FRIENDLY_COMMAND_CENTER_UX_ACCEPTED

Human-Language Product Contract

The final user-facing Command Center must support three user levels.

Daily user:

Uses MULAI DI SINI.
Opens folder data hari ini.
Clears folder data hari ini.
Checks input.
Runs report.
Opens output.
Does not edit registry.

Onboarding user:

Uses TAMBAH REPORT / DATA.
Adds data/report using simple form.
Selects template file.
Selects sheets from dropdown.
Defines Blok Proses Pivot.
Runs Cek Template / Coba Jalankan.
Does not see registry fields.

Admin/reviewer:

Uses PENGATURAN SISTEM.
Approves, rejects, or asks user to complete.
Can access advanced details only when needed.
Does not manually fill technical registry fields during normal onboarding.
Blok Proses Pivot Definition

Use this exact definition:

1 Blok Proses Pivot =
1 data sumber
-> 1 sheet data mentah
-> 1 sheet pivot
-> 1 Area Tempel Hasil Pivot di halaman laporan final

A report may have 1 to N Blok Proses Pivot.

Test A proves 1-block report support.

Test B proves multi-block report support.

This does not mean future reports must have 2 blocks.

Final No-Go Rules

Do not:

Rewrite original PRD.
Rewrite old roadmap.
Touch workbook in Step 0.
Save original workbook in any step.
Patch VBA in Gate 2.
Use fake RPT004.
Promote QA report as production.
Put QA sources in production Today folder.
Leave active QA rows before freeze.
Continue gate automatically.
Kill Excel automatically.
Update decisions/decision-log.md.
Hide failed evidence.
Claim generic automation before Gate 2 proof.
Final Classification Map

Step 0 success:

SECOND_BRAIN_RC4C2_DOCUMENTATION_PACKAGE_COMMITTED

Step 1 success:

WORKBOOK_UX_REALITY_AUDIT_COMPLETE

Step 2 success:

GENERIC_STANDARD_TEMPLATE_ENGINE_PROVEN

Step 2 engine not proven:

GENERIC_STANDARD_TEMPLATE_ENGINE_NOT_YET_PROVEN

Step 3 success if engine proven:

BABY_FRIENDLY_ONBOARDING_WRAPPER_READY

Step 3 success if engine not proven:

BABY_FRIENDLY_INTAKE_WRAPPER_READY_ENGINE_NOT_PROVEN

Step 4 success:

RC4C2_REGRESSION_AND_QA_CLEANUP_ACCEPTED

Step 5 success:

RC4C2_BABY_FRIENDLY_COMMAND_CENTER_UX_ACCEPTED

Documentation package ready:

FINAL_CLASSIFICATION=RC4C2_FINAL_PRD_NO_BRAINER_PROCEDURE_READY

First Antigravity Instruction

Antigravity must start only with Step 0.

Do not open Excel.

Do not audit workbook.

Do not patch workbook.

Do not create candidate workbook.

Commit documentation package first.

After Step 0 is complete, stop and wait for Owner to explicitly say:

lanjut Step 1

Final Step 0 target:

SECOND_BRAIN_RC4C2_DOCUMENTATION_PACKAGE_COMMITTED
