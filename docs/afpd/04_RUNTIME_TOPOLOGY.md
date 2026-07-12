# 04_RUNTIME_TOPOLOGY.md

<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 68-75
source_heading: Layer 1 - Input Sources
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 76-89
source_heading: 2.1 Telegram Input
migration_status: CURRENT
conflict_id: none
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 90-107
source_heading: 2.2 Email Notification Input
migration_status: CURRENT
conflict_id: EMAIL_DEFAULT_OFF_VS_ACTIVE_RUNTIME
-->
<!-- AFPD_PROVENANCE
source_path: ecosystem/projects/vortex-ai-skill-lab/docs/AIRO_FINANCE_COMMAND_CENTER_FINAL_KITAB.md
source_lines: 108-121
source_heading: 2.3 Future Bank Mutation Input
migration_status: CURRENT
conflict_id: none
-->

## Apps Script Source Inventory
- **Active Handler File**: `AIRO_Finance_Multitab_Final_v1.js` is the sole entry point handling doPost.
- **Neutralized Compatible Source**: `Kode.js` contains a neutralized legacy doPost redirecting to the active handler to maintain compatibility.
- **Active doPost count in Kode.js**: 0.

## Webhook and Poller Topology
- **Telegram Webhook**: Registers bot tokens and dispatches user texts.
- **Gmail Ingestion Poller**: Triggered hourly to query Gmail messages.
- **State Storage**: Chat states are stored in properties with key prefix `AIRO_PENDING_CLARIFICATION_<chat_id>`.

## Timezone Normalization Issue
- The script manifest `appsscript.json` specifies `Asia/Bangkok`, while internal script logic calculates times using `Asia/Jakarta`. This remains a known discrepancy.
