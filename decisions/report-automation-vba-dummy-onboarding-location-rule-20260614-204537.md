# Decision - Dummy Onboarding QA Location Rule

Date: 2026-06-14

Decision: root-dependent macro QA workbook must be placed in 00_Command_Center or another CCP_ProjectRoot-compatible location.

Earlier failed V2-V5 tests used nested QA workbook paths under:
D:\Randas\Others\Honda_Report_Automation_Pilot_Package\98_QA_SANDBOX\DUMMY_ONBOARDING_TEST_...

That location is too deep for CCP_ProjectRoot().

Passing V6 location:
D:\Randas\Others\Honda_Report_Automation_Pilot_Package\00_Command_Center

Scope: this is QA workbook placement rule only. It does not change final operator handover product and does not prove arbitrary new report runtime support.
