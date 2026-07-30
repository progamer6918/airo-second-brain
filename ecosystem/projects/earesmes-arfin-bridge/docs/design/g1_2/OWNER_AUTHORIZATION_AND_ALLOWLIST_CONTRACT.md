# EAB G1.2 Owner Authorization and Allowlist Contract

- **AUTHORIZATION_TYPE**: Owner Principal Binding Filter
- **REQUIREMENT**: `REQ-013` (AFPD-INC-011 Remediation)
- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Principal Separation

The authorization filter strictly separates:
- `ACTOR_USER_ID`: Numeric Telegram `from.id` of the message/callback sender.
- `CONVERSATION_CHAT_ID`: Numeric Telegram `chat.id` of the chat window.
- `AUTHORIZED_OWNER_PRINCIPAL`: Numeric Telegram ID specified in `EAB_OWNER_CHAT_ID_ALLOWLIST`.

---

## 2. Phase 1 Policy

```ini
PHASE_1_GROUP_POLICY=PHASE_1_UNSUPPORTED_FAIL_CLOSED
```

1. **Private Chat Requirement**: Both `ACTOR_USER_ID` and `CONVERSATION_CHAT_ID` MUST match an allowlisted `AUTHORIZED_OWNER_PRINCIPAL`.
2. **Group Chat Policy**: Group chats are **UNSUPPORTED AND FAIL-CLOSED** in Phase 1 (`ERR_UNSUPPORTED_GROUP_CHAT`).
3. **Callback Query Authorization**: Callback query sender `from.id` and message `chat.id` are evaluated separately. Callback sender must match `AUTHORIZED_OWNER_PRINCIPAL`.
4. **Display Name / Username Disregard**: Telegram `username`, `first_name`, and `last_name` are **IGNORED FOR AUTHORIZATION** (username spoofing prevention).
