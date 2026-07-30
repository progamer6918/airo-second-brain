# EAB G1.2 Audit and Redaction Contract

- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Keyed HMAC Audit Pseudonymization

To prevent reverse lookup of raw owner Chat IDs while ensuring safe audit correlation, `owner_chat_id` pseudonymization uses **Keyed HMAC-SHA256**:

```text
owner_chat_id_pseudonym = HMAC-SHA256(EAB_AUDIT_PSEUDONYMIZATION_KEY, normalized_owner_chat_id_string)
```

- `EAB_AUDIT_PSEUDONYMIZATION_KEY` is a dedicated secret key separate from service authentication keys.
- Raw `owner_chat_id` and simple `SHA256(raw owner_chat_id)` without key are **STRICTLY FORBIDDEN** in audit logs.

---

## 2. Mandatory Audit Fields

Every API invocation generates an audit event containing:
- `request_id`
- `audit_correlation_id`
- `operation_id`
- `owner_chat_id_pseudonym`
- `authentication_result` (`PASS` / `FAIL`)
- `authorization_result` (`PASS` / `FAIL`)
- `validation_result` (`PASS` / `FAIL`)
- `pending_id` (if applicable)
- `application_status`
- `retry_classification`
