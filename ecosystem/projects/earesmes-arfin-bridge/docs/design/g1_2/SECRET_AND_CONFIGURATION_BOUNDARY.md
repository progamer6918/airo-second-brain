# EAB G1.2 Secret and Configuration Boundary

- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Configuration Declarations

```ini
EAB_SERVICE_AUTH_KEY_ID=key_2026_01
EAB_OWNER_CHAT_ID_ALLOWLIST=123456789
EAB_SCHEMA_VERSION=1.0
EAB_ADAPTER_TIMEOUT_MS=8000
EAB_MAX_RETRY_COUNT=2
```

---

## 2. Secret Redaction Rules

1. Secrets (`EAB_SERVICE_SECRET`, `EAB_AUDIT_PSEUDONYMIZATION_KEY`, Telegram tokens) MUST be injected strictly via environment variables / Secret Manager.
2. NO secret values in Git repositories, source code files, logs, error tracebacks, URLs, Telegram messages, or user receipts.
3. Automated redaction filter replaces any detected token or signature with `[REDACTED]`.
