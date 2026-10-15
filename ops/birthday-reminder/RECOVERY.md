# Birthday sender V4 — READY_NOT_ACTIVE

This is an offline-reviewed source candidate, not an installed sender or enabled timer.
The approved production checkout and all EARNSART resources remain untouched.

## Private Owner input (no AI conversation secrets)

In an Owner-controlled VPS terminal, create or edit this dedicated private file:

```sh
install -d -m 700 "$HOME/.config/airo-birthday-reminder"
(umask 077; nano "$HOME/.config/airo-birthday-reminder/credentials.env")
chmod 600 "$HOME/.config/airo-birthday-reminder/credentials.env"
```

Put `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` assignments in that file, using only
credentials and the intended destination for `@earnsai_reminder_bot`. The Owner's
purpose-specific private input is the credential/destination authority reference.
Do not paste values into chat, command arguments, public Git, logs or shell history.
Do not retrieve, reuse, or substitute another integration's credentials. Report
only that the dedicated file is ready; no additional architectural approval is needed.
An existing approved private secret-store reference is an alternative to this file.

## Conditional activation procedure

After the dedicated authority reference is present, the authorized executor must:

1. Load only the dedicated private configuration through the approved runtime;
   never print its contents. Read-only `getMe` must return `is_bot=true`, username
   `earnsai_reminder_bot`; record its numeric bot ID privately. Read-only `getChat`
   must resolve the exact Owner-designated numeric destination. API visibility
   alone does not establish Owner authority for a recipient. No webhook or polling
   changes are part of this workflow.
2. Reuse `prepared-dataset.json` and its checksum-bound 68-row V3 CSV; do not load
   `review.private.json` as a send source. Six records remain quarantined. No
   redownload, extraction, isolation regression, or new birthday session is needed.
3. Create mode-0600 `activation.json` in the existing private birthday root only
   after actual verification. Required fields: `status=VERIFIED`,
   `scope=BIRTHDAY_REMINDER_ONLY`, `bot_username`, actual numeric `bot_id`,
   `recipient_sha256` of the canonical numeric chat ID, `dataset_sha256`, and
   `authority_ref` for the actual Owner input/approved secret-store record. Record
   actual verification evidence separately. This is not permission to fabricate
   identity evidence or self-approve a different bot/destination.
4. Install only the reviewed sender and runner under the dedicated
   `/home/ubuntu/.local/lib/airo-birthday-reminder` release directory; create a
   mode-0700 `/home/ubuntu/.local/share/airo-birthday-reminder/sender-state`.
   No sender files are installed by the offline preparation task.
5. Run `--check` (never prints birthday records), then `--smoke` once through the
   dedicated runtime. Its stable ledger key is `smoke:recovery-v2`, independent of
   the current date. Required text is the previously approved recovery message.
   Verify the returned Telegram message ID. Never replay a failed/uncertain smoke.
6. After identity/destination/runtime verification and successful smoke, install
   only the two prepared dedicated systemd units, reload the system unit manager,
   and enable only `airo-birthday-reminder.timer`. Do not restart any unrelated
   unit. Verify its enabled state, next run in Jakarta time and persistent config.
   If activation fails, contain only this workflow and preserve its send ledger.

## Deduplication and failures

The private SQLite send ledger stores hashes, intent time, status and message ID;
no names, birthdays, message bodies, tokens or raw recipients are stored there.
A process-wide `flock` spans the claim/send/commit sequence. SQLite FULL synchronous
commits make the `SENDING` claim durable before an API call. A key identifies one
birthday notification per Jakarta calendar day, even if the dataset changes.

`SENT` returns `ALREADY_SENT`. `SENDING` or `UNKNOWN` returns an explicit uncertain
outcome and never sends again. This includes a crash before the API call, a lost
response after delivery, or failure to persist the final acknowledgement. Known
API rejection is also held conservatively. No automatic reset command is supplied.
Reconcile against actual private delivery evidence first; a confirmed unsent
outcome requires explicitly authorized operational recovery, not ledger deletion.
A changed recipient is blocked, rather than silently creating a new same-day send.

The timer targets 08:00 Asia/Jakarta. `Persistent=true` catches a missed activation;
the sender evaluates only the current Jakarta date and does not replay historical
birthdays. Its existing daily key prevents repeated current-day delivery across
restart/catch-up. Oversized messages fail before a send attempt and require review.
There is no hidden date override, printed dry-run message, or legacy CSV fallback.

## Evidence and rollback boundaries

Synthetic regressions include separate-process restart/overlap and interrupted
send/commit cases. These establish offline behavior, not real Telegram delivery.
No actual reboot/power loss is induced. Preserve the V3 private source, CSV,
quarantine, pointer and any future delivery state through rollback. Disable only a
new birthday timer if subsequently activated; never stop EARNSART/Earesmes/Arfin,
reset their sessions, modify their files, or rewrite shared Git history.

## H-1 enhancement (2026-10-15)

The deployed CLI defaults to both day and eve reminders at the existing 08:00 Jakarta timer. `--reminder day` or `--reminder eve` selects one kind; `--check` evaluates both without sending. Eve uses tomorrow calendar arithmetic and a separate `birthday-eve:YYYY-MM-DD` key for the target birthday. The `birthday:YYYY-MM-DD` key and stable smoke key remain backward compatible. Current source and active status are recorded in docs/validation/AIRO_BIRTHDAY_H1_REMINDER_20261015.md.
