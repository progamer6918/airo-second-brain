# EAB G1.2 Service Authentication Contract

- **CALLER**: Hermes Worker / Earesmes Gateway
- **RECEIVER**: Arfin Bounded Adapter API
- **STATUS**: `REMEDIATED_DESIGN_COMPLETE`

---

## 1. Authentication Wire Contract

Service authentication is transported **STRICTLY IN HTTP HEADERS**. The `authentication_proof` object is **REMOVED** from application JSON envelopes.

### HTTP Header Specification:
- `X-EAB-Key-ID`: Key identifier for credential lookup (e.g. `key_2026_01`).
- `X-EAB-Timestamp`: UNIX timestamp in seconds (integer).
- `X-EAB-Nonce`: Cryptographic unique 64-bit random hex string (replay protection).
- `X-EAB-Signature`: HMAC-SHA256 hex digest of the canonical signing string.

---

## 2. Canonical Signing Material

The `X-EAB-Signature` is computed over the canonical string:

```text
v=1.0&op={operation_id}&req_id={request_id}&ts={timestamp}&nonce={nonce}&body_sha256={body_sha256}
```

Where:
- `body_sha256` = SHA-256 hex digest of the exact raw HTTP request body bytes.
- Signature computed via `HMAC-SHA256(EAB_SERVICE_SECRET, canonical_signing_string)`.

---

## 3. Verification Protocol & Security Guards

1. **Header Validation**: Verify `X-EAB-Key-ID`, `X-EAB-Timestamp`, `X-EAB-Nonce`, and `X-EAB-Signature` are present. Missing headers fail with `401 Unauthorized` (`ERR_MISSING_AUTH`).
2. **Key Lookup**: Look up secret by `X-EAB-Key-ID`. Unknown key fails with `401 Unauthorized` (`ERR_INVALID_AUTH_KEY`). Supports dual active keys (`K_CURRENT`, `K_PREVIOUS`) during rotation.
3. **Timestamp Window Check**: Ensure `|current_time - X-EAB-Timestamp| <= 300` seconds (5 minutes). Stale timestamp fails with `401 Unauthorized` (`ERR_EXPIRED_AUTH_TIMESTAMP`).
4. **Nonce Replay Guard**: Query durable nonce store for `(key_id, nonce)`. If present, fail with `401 Unauthorized` (`ERR_NONCE_REPLAYED`).
5. **Body Digest Verification**: Compute SHA-256 digest of request body and compare with `body_sha256`. Mismatch fails with `401 Unauthorized` (`ERR_BODY_TAMPERED`).
6. **Constant-Time Signature Verification**: Verify signature using `constant_time_compare(computed_sig, X-EAB-Signature)`. Mismatch fails with `401 Unauthorized` (`ERR_INVALID_SIGNATURE`).
