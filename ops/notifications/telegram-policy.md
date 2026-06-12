# Telegram Notification Policy

This policy governs the anti-spam rules and operation logic for Telegram notifications within the AIRO Second Brain runtime.

## Core Rules

1. **No news = no Telegram.**
   - Do not send notifications if there are no significant events, state changes, or queue processing activities.
2. **No-op sync = silent.**
   - Regular periodic syncs that result in no changes (dry-run or real) must not trigger notifications.
3. **Repeated same warning = cooldown.**
   - If the system is in a degraded state and the same warning is generated consecutively, apply a cooldown period to avoid spamming the owner.
4. **State change = notify.**
   - Transitions between states (e.g., healthy to degraded, degraded to blocked, blocked to healthy) must always generate a notification.
5. **Recovery = notify.**
   - Send an immediate notification upon system recovery.
6. **Startup = notify once per PC/session boot.**
   - Send a startup heartbeat notification when the system boots and starts the runtime runner for the first time in the session.

## Configuration Fallbacks

- If the Telegram credentials (bot token or chat ID) are missing, improperly configured, or blocked, the system must fallback to:
  `telegram_status: log_only_unconfigured`
- The runtime runner is explicitly designed to **function perfectly without Telegram**. No dependencies will crash or halt due to missing Telegram capabilities; it will merely degrade gracefully to local logging.
