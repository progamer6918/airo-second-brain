# Windows interface and VPS runtime migration

Status: migration acceptance verified, 2026-10-06; draft source review remains separate. Owning ASB session:
`ab3f74fb-0535-4ab4-8751-c68af186164a`.

## Verified behavior

- The Windows relay uses native pinned SSH/SCP and no executable WSL command.
  Its scheduled task runs the canonical Windows script and has a logon trigger.
  A real queue action completed and produced a new 3200x1080 local screenshot;
  the test did not transmit the screenshot. The old WSL relay is disabled.
- Earesmes is isolated on the VPS from the existing Hermes Plus profile and core.
  The legacy worker policy and custom Google tools are preserved in its private
  runtime. Gateway/worker paths are selected by environment variables. This
  private runtime is not identical to the older public worker revision.
- Earesmes cutover stopped source polling, drained the queue, copied 277 current
  state files with matching hashes, and snapshotted three SQLite databases.
  Target startup passed fresh-heartbeat and zero-restart checks. The WSL worker
  and gateway are disabled/inactive; the new VPS units are enabled/active.
- Owner's inbound Telegram test returned exactly `EARESMES_VPS_OK`, recorded as
  done after one attempt with the reply successfully sent.
- Existing Google OAuth refresh, private custom tool imports, and a model canary
  passed. Google write operations were not exercised.
- Browser navigation, title and accessibility text checks passed with official
  Chrome and Ubuntu sandbox protection enabled. No `--no-sandbox` workaround was
  used. Dummy confirmation tests rejected wrong-chat, expired and repeated actions.
- Owner retired the obsolete finance Sheets timer and hourly paper-trading cron.
  Original units/crontab, credentials and data remain in private rollback backups.
- The broken plaintext Drive backup task was replaced, by Owner choice, with a
  native encrypted Windows backup. Its full scheduler execution passed, including
  authenticated decryption, all 3,927 file hashes, restored Git integrity, and VPS
  ciphertext checksum. A subsequent full restore to a new private directory passed.

## Native encrypted backup

`bin/airo-native-private-backup.py` needs native Windows Python with `cryptography`,
Git, OpenSSH, the existing private recovery key, and pinned VPS host identity.
Its configured source roots are the Windows ASB vault, recovery staging, and clip
inbox. It excludes rebuildable dependency/cache directories and does not follow
links. SQLite files use online snapshots; changed ordinary files fail the backup.

The daily task runs at 03:00 with catch-up when the PC and interactive account are
available. `--scheduled` skips a verified backup less than 23 hours old. It performs
free-space checks, retains prior backups, and does not prune or delete old data.
Insufficient disk space or failed connectivity produces failure rather than a
success claim. Monitor the private latest receipt and task result. This is a
Windows-interface data backup and cannot run while the PC is offline.

Format `AIROGCM1`: 8-byte magic, 32-byte random salt, 12-byte nonce, gzip tar
ciphertext, 16-byte tag. AES-256-GCM authenticates the header. PBKDF2-HMAC-SHA256
uses 600,000 iterations and the exact bytes of the existing recovery key file.
Each archive contains a SHA256 manifest. Full verification authenticates the
entire stream and compares every archived file hash before claiming success.

For recovery, run the script with `--restore-file` and `--restore-directory`.
The destination must be a new directory under the configured private backup
root. Restoration stages data privately, validates authentication and all hashes,
then moves it to that new directory. It never restores over the live vault.
Review recovered files before replacing live data.

The key stays on the PC and is not sent to the VPS. Offsite ciphertext alone
cannot recover data if the only key copy is lost. Separate key escrow remains an
Owner decision.

## Original migration backup and rollback

The original large encrypted backup requires both its SQLite snapshot supplement
and Windows rollback supplement. The snapshot supplement corrected an exclusion
pattern that also omitted the staged SQLite files from the main archive. All ten
SQLite snapshots restored with matching hashes and integrity checks; restored
Git passed integrity checks. All three VPS ciphertext checksums match.

Original scheduled-task XML, relay source, service configuration, crontab and
private credentials are preserved. Earesmes has a separate final-state encrypted
archive and target pre-handoff rollback snapshot. To reverse runtime ownership,
stop the target poller first, reconcile current queue/offset/state, then start the
source. Do not run two pollers for the same bot token.

Keep the Windows relay in UTF-8 with BOM for Windows PowerShell 5. Normalize remote
Bash payload line endings to LF before encoding/transmitting them.

## WSL on-demand acceptance and observed RAM

Owner retired the distinct paper-control bot. Before and final encrypted backups
restored all 186 files with matching hashes; graceful process exit and absent tmux
session were verified. Both offhost ciphertext checksums match. No source/data
was deleted, and no automatic launcher was found for that bot.

WSL was shut down after the final workload retired. Native SSH/SCP, the actual
Windows Obsidian executable and Windows vault read, a fresh 3200x1080 relay queue
capture, and a full scheduled encrypted backup worked while no distro or VM
process was running. The backup exited 0 and verified restore and VPS checksum.
The old Windows WSL listener/sync wrappers are disabled. Enabled AIRO startup
entries point to native executables. The named Ubuntu Obsidian shortcut remains
an explicit optional WSL launcher; use the registered native Windows Obsidian
shortcut for ordinary interface use.

The first post-shutdown queue test exposed an already-hung native SSH process:
Running task state alone was insufficient evidence. The relay now bounds the
whole SSH process to 20 seconds, retains strict host checking, and reads stdout
and stderr asynchronously. A deliberate finite slow command hit the deadline at
20.03 seconds. The real Windows PowerShell 5 relay then completed a fresh capture.
The first four-second restart observation rolled back conservatively; subsequent
deployment waited for actual scheduler stop/new-process state and passed.
Ancient in-progress queue items were preserved, not replayed or deleted.

Three samples on each side of shutdown, two seconds apart with five seconds of
settling, used identical tracked application process IDs. Median WSL working set
fell from 280,248,320 bytes (267.27 MiB) to zero. Free physical RAM rose from
3,846,389,760 to 4,497,838,080 bytes, an observed increase of 621.27 MiB. Tracked
application working set changed by about 17 MiB. This short comparison does not
prove historical peak usage, leaks, or that every freed byte belongs to WSL.

Rollback for on-demand Linux is explicit `wsl.exe -d Ubuntu`; the distro and data
remain installed. Retired jobs remain disabled when Linux is started.

## Practical limits

Real logoff/reboot recovery and the complete relay actuator suite were not
exercised. Verification covers the configured startup paths, duplicate-trigger
handling, native transport, real queue/capture, native vault launch/read, and
scheduled backup. Offsite ciphertext requires the recovery key retained on the
PC; independent key escrow remains an Owner decision. No paid capacity, account
access changes, WSL unregister/uninstall, or old-data deletion were performed.

This source review remains a draft PR; it does not promote main or unrelated
preexisting dirty legacy source. Runtime-specific private configuration, state,
and rollback source are preserved in the approved private archives.
