# AIRO Manual Sync Queue Policy

`inbox/manual-sync-queue.md` is staging, not canonical.

Entries must be processed into canonical/deferred files by explicit owner request.

Runtime may detect and report pending captures, but must not auto-promote.

Organize may move processed blocks to Processed Captures only after writing processed output.
