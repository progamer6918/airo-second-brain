# Birthday latest-data private migration V3

AIRO_AGENT_IDENTITY_GUARD=FAIL (dedicated reminder identity remains unverified)
MUTATION_ALLOWED=PRIVATE_DATA_PREPARATION_ONLY

```json
{
  "TASK": "AIRO_BIRTHDAY_LATEST_DATA_PRIVATE_MIGRATION_V3",
  "EARNSART_UNTOUCHED": "PASS \u2014 18 monitored paths unchanged; approved engine unchanged",
  "DATA_MIGRATION": "PASS_PRIVATE_PREPARATION_ONLY",
  "DATA_VALIDATION": "PASS_WITH_QUARANTINE \u2014 68 eligible rows, 6 excluded review rows",
  "DATA_AUTHORITY": "PASS \u2014 exact latest source designated by Owner V3; not old 69-row snapshot",
  "CONFLICT_REVIEW": "PENDING \u2014 1 date conflict quarantined without automatic choice",
  "BOT_IDENTITY": "UNVERIFIED \u2014 dedicated credential reference unresolved",
  "RECIPIENT_VERIFIED": "NO",
  "SOURCE_REPAIR": "NOT_PERFORMED \u2014 conditional production repair gate remains closed",
  "DUPLICATE_PREVENTION": "NOT_IMPLEMENTED_IN_SENDER; extraction preserves and flags possible duplicates, current dataset has 0",
  "TELEGRAM_SMOKE_TEST": "NOT_SENT",
  "SCHEDULER_PERSISTENCE": "NOT_CONFIGURED_BY_THIS_TASK",
  "NEXT_ACTION": "Review 1 quarantined date conflict privately and supply an approved dedicated bot secret-store/recipient reference",
  "FINAL_VERDICT": "TERHAMBAT \u2014 private data preparation complete; production notification recovery blocked",
  "DATA_REPORT": {
    "schema": 1,
    "SOURCE_FETCH": "PASS",
    "SOURCE_FILE_ID": "1l8d5rgppbpVlvAylpJjOG_nDCjwZybEx",
    "SOURCE_MODIFIED_TIME": "2026-10-12T02:00:44.432Z",
    "SOURCE_SHA256": "cee51dba658815d2df4e84b5e0d9e9e5aeec663564619eb75a1c9a94f4b47e70",
    "BIRTHDAY_TAB": "Ultah",
    "HEADER_ROW": 3,
    "TOTAL_SOURCE_ROWS": 74,
    "VALID_BIRTHDAY_ROWS": 68,
    "MISSING_NAME_ROWS": 5,
    "MISSING_DATE_ROWS": 5,
    "MISSING_BOTH_DATE_ROWS": 4,
    "MISSING_DEALER_ROWS": 0,
    "INVALID_DATE_ROWS": 0,
    "CONFLICT_ROWS": 1,
    "UNKNOWN_BIRTH_YEAR_ROWS": 8,
    "NORMALIZED_ONLY_ROWS": 1,
    "POSSIBLE_DUPLICATE_ROWS": 0,
    "REVIEW_ROWS": 6,
    "DATA_AUTHORITY": "OWNER_DESIGNATED_LATEST_SOURCE",
    "ACTIVATED": false,
    "policy": {
      "placeholder_primary_birth_years": [
        1900,
        2024
      ],
      "normalized_column_never_supplies_birth_year": true,
      "conflicts_quarantined": true,
      "possible_duplicates_preserved": true,
      "missing_primary_date_uses_valid_normalized_day_month_only": true
    },
    "parser_versions": {
      "openpyxl": "3.1.5"
    },
    "PRIVATE_CSV_CREATED": true,
    "PRIVATE_CSV_SHA256": "56f0448d2a4e99f30ac1f78e148285a85d11f7fb01847d327abc03414cb59b9c",
    "EXTRACTOR_SHA256": "a8349fa596a0f0dad54d13ee172403672419d3630d02b921251292067fc806d8",
    "PRIVATE_DATASET_DIR": "/home/ubuntu/.local/share/airo-birthday-reminder/datasets/cee51dba658815d2-a8349fa596a0"
  },
  "TESTS": {
    "synthetic_tests_passed": 11,
    "synthetic_tests_failed": 0,
    "test_file_sha256": "17928415ac62ac1a3b833f684e1f1ebdfaf13a7861f3d98d642c56c47f538648",
    "known_source_conflict_privately_verified": true,
    "valid_unknown_year_rows": 8,
    "no_notifications_sent": true
  },
  "BLOCKER_IF_ANY": "Dedicated earnsai_reminder_bot secret-store reference and intended recipient are unresolved; one date-conflict row awaits Owner review in the private quarantine",
  "PARALLEL_SESSION": "0f4865d0-a942-47cd-b1c3-e8fa7c554052",
  "dataset_pointer": "/home/ubuntu/.local/share/airo-birthday-reminder/prepared-dataset.json",
  "activation": false,
  "privacy": "Personal workbook, CSV, provenance and review records remain outside public Git in private VPS storage; directories 0700, files 0600",
  "source_retrieval": "Authorized Drive connector raw XLSX; source metadata rechecked unchanged after download",
  "count_definitions": {
    "TOTAL_SOURCE_ROWS": "Nonempty rows under the four required birthday headers; fully empty rows excluded",
    "MISSING_NAME_ROWS": "Missing, blank or dash placeholder names",
    "MISSING_DATE_ROWS": "Primary TANGGAL LAHIR missing: 5; of these 1 has usable normalized-only date and 4 have neither date",
    "UNKNOWN_BIRTH_YEAR_ROWS": "8 unknown-year records; source placeholder years are not used for age",
    "VALID_BIRTHDAY_ROWS": "68 retained rows after excluding 5 missing-name records and 1 conflicting-date record"
  },
  "source_mutations": false,
  "scheduler_mutations": false,
  "telegram_messages_sent": 0,
  "clipboard_verified": false
}
```

## Reproduction and bounded review

Install scripts/requirements-birthday-data.txt only into the dedicated private tools environment. Run scripts/airo_birthday_private_extract.py with the immutable private source XLSX, exact file ID and modified time, and a mode-0700 private output root. Immutable generation directories bind the source and extractor hashes; manifest, CSV, row-level provenance and quarantine are mode 0600. prepared-dataset.json points to the tested generation and explicitly marks PREPARED_NOT_ACTIVATED. The original workbook is never saved or modified.

Use normalized day/month and explicit unknown-year fields in future authorized sender repair. Never use placeholder years to calculate age or silently promote quarantined dates. Possible duplicates are flagged and retained, including synthetic coverage for distinct dealers and matching identities. The previous 69-row snapshot is not selected or modified.

All 11 synthetic tests passed, covering exact/ambiguous worksheet selection, provenance, unknown years, normalized-only dates, conflicting fields, duplicate preservation, conflicting identities, incomplete records, private permissions, deterministic retry, unchanged source, symlinks and leap dates. Bounded code review confirmed no new framework, no network/scheduler/Telegram calls in the extractor, and one isolated pinned parser dependency appropriate for XLSX formatting and dates. The approved parallel engine and existing birthday runner were not modified.

No personal rows, credentials, bearer download links, or private review payloads are committed. The birthday session remains ACTIVE with an explicit blocker.
