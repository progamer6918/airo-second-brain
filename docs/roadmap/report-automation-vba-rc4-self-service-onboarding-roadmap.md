# RC4 Roadmap - Self-Service Onboarding Engine

Baseline: RC3S_FINAL_PRODUCT_READY_PACKAGE_FROZEN

## RC4A - Hardcode Audit and Engine Boundary
Deliverables: RC4A_HARDCODE_AUDIT_REPORT, RC4A_ENGINE_BOUNDARY_MAP, RC4A_FINAL_CLASSIFICATION=RC4A_READY_FOR_ONBOARDING_SCHEMA

## RC4B - Registry Schema V2
Deliverables: CC_REPORT_REGISTRY_V2, CC_SOURCE_REGISTRY_V2, CC_MAPPING_PROFILE, CC_VALIDATION_RULES, RC4B_FINAL_CLASSIFICATION=RC4B_REGISTRY_SCHEMA_READY

## RC4C - Onboarding Wizard
Buttons: Add New Report, Audit Template, Detect Output Sheet, Register Required Sources, Build Mapping Draft, Validate Mapping, Dry Run Report, Accept Report, Freeze Package.
Final: RC4C_ONBOARDING_WIZARD_READY

## RC4D - Template Audit Engine
Audit workbook type, sheet list, hidden sheets, UsedRange, pivots, connections, formulas, merged cells, external links, named ranges, candidate output sheet, risk flags.
Final: RC4D_TEMPLATE_AUDIT_ENGINE_READY

## RC4E - Mapping Compiler
Mapping fields: ReportID, StepNo, SourceKey, TargetSheet, TargetAnchor, ImportMode, HeaderProfile, ColumnMapMode, PreserveFormulaRange, PostAction, ValidationRule.
Final: RC4E_MAPPING_COMPILER_READY

## RC4F - Generic Report Runner
Flow: read enabled reports, copy template, resolve sources, import by mapping, preserve formula ranges, refresh pivots/connections, optional adapter, save output, update registry, process summary.
Final: RC4F_GENERIC_RUNNER_READY

## RC4G - Dry Run and Acceptance Harness
Gates: registry complete, template audit pass, source readiness pass, mapping validation pass, dry run output exists, formula error check pass, pivot/connection check pass, final acceptance pass.
Final: RC4G_ONBOARDING_ACCEPTANCE_HARNESS_READY

## RC4H - Operator Launcher
Required: RUN_OPERATOR.bat, RUN_ACCEPTANCE_TEST.bat, RUN_ONBOARDING_WIZARD.bat, RUN_FREEZE_PACKAGE.bat.
Final: RC4H_OPERATOR_LAUNCHER_READY

## RC4I - Regression Pack
Verify RPT001/RPT002/RPT003 still OK, runner clean, Result VE template still has CC_MASTER_DATA_MD, registry sheet is CC_REPORT_REGISTRY, no retry loop, no Excel orphan.
Final: RC4I_REGRESSION_PACK_READY

## RC4J - Final Freeze
Final: FINAL_CLASSIFICATION=RC4_SELF_SERVICE_ONBOARDING_SYSTEM_FROZEN
