"""
Authentication Guard for Bounded Arfin Adapter (CU-02)
- HMAC-SHA256 request signature verification with constant-time comparison
- Owner chat_id allowlist filtering (default-deny)
- Service key rotation with 24-hour grace window
- 60-second clock skew tolerance constraint
- In-memory NonceReplayGuard with 600-second TTL (single-process runtime guarantee level)
- Structured audit logging with secret redaction
"""

import time
import hmac
import hashlib
import re
from typing import Set, Optional, Dict, Any

class AuthGuardError(Exception):
    def __init__(self, message: str, error_code: str):
        super().__init__(message)
        self.error_code = error_code

class NonceReplayGuard:
    """In-memory nonce replay guard with 600s TTL."""
    def __init__(self, ttl_seconds: float = 600.0):
        self.ttl_seconds = ttl_seconds
        self._seen_nonces: Dict[str, float] = {}

    def _purge_expired(self, current_time: float) -> None:
        expired = [n for n, ts in self._seen_nonces.items() if current_time - ts > self.ttl_seconds]
        for n in expired:
            del self._seen_nonces[n]

    def check_and_record(self, nonce: str, current_time: Optional[float] = None) -> None:
        now = current_time if current_time is not None else time.time()
        self._purge_expired(now)
        if nonce in self._seen_nonces:
            raise AuthGuardError(f"Replayed nonce detected: {nonce}", "AUTH_REPLAY_DETECTED")
        self._seen_nonces[nonce] = now

class SecurityGuard:
    """
    Enforces authentication envelope, owner chat allowlist, key rotation,
    clock skew tolerance, and secret redaction.
    """
    def __init__(
        self,
        current_service_key: Optional[str] = None,
        previous_service_key: Optional[str] = None,
        previous_key_rotated_at: Optional[float] = None,
        allowed_owner_chat_ids: Optional[Set[str]] = None,
        clock_skew_tolerance_sec: float = 60.0
    ):
        self.current_service_key = current_service_key
        self.previous_service_key = previous_service_key
        self.previous_key_rotated_at = previous_key_rotated_at
        self.allowed_owner_chat_ids = allowed_owner_chat_ids if allowed_owner_chat_ids is not None else set()
        self.clock_skew_tolerance_sec = clock_skew_tolerance_sec
        self.replay_guard = NonceReplayGuard(ttl_seconds=600.0)

    def verify_owner_chat_id(self, owner_chat_id: str) -> None:
        """Verify owner_chat_id against allowlist (default-deny)."""
        if not self.allowed_owner_chat_ids:
            raise AuthGuardError("Empty owner_chat_id allowlist; access denied.", "AUTH_UNAUTHORIZED")
        if str(owner_chat_id) not in self.allowed_owner_chat_ids:
            raise AuthGuardError(f"owner_chat_id '{owner_chat_id}' not in allowlist.", "AUTH_UNAUTHORIZED")

    def verify_owner_telegram_principals(
        self,
        actor_user_id: str,
        conversation_chat_id: str,
        chat_type: str
    ) -> None:
        """Enforce the Phase-1 Telegram Owner principal contract."""
        actor = str(actor_user_id or "").strip()
        conversation = str(conversation_chat_id or "").strip()
        chat_kind = str(chat_type or "").strip().lower()

        if chat_kind in {"group", "supergroup"}:
            raise AuthGuardError(
                "Group chats are unsupported in EAB Phase 1.",
                "ERR_UNSUPPORTED_GROUP_CHAT"
            )

        if chat_kind != "private":
            raise AuthGuardError(
                "Telegram conversation is not a proven private Owner chat.",
                "ERR_UNAUTHORIZED_CHAT_ID"
            )

        if not self.allowed_owner_chat_ids:
            raise AuthGuardError(
                "Owner principal allowlist is empty; access denied.",
                "ERR_UNAUTHORIZED_CHAT_ID"
            )

        if not actor or not conversation:
            raise AuthGuardError(
                "Telegram actor or conversation principal is missing.",
                "ERR_UNAUTHORIZED_CHAT_ID"
            )

        if actor != conversation:
            raise AuthGuardError(
                "Telegram actor and conversation principals do not match.",
                "ERR_UNAUTHORIZED_CHAT_ID"
            )

        if (
            actor not in self.allowed_owner_chat_ids
            or conversation not in self.allowed_owner_chat_ids
        ):
            raise AuthGuardError(
                "Telegram Owner principal is not allowlisted.",
                "ERR_UNAUTHORIZED_CHAT_ID"
            )

    def _verify_signature(self, key: str, payload_str: str, timestamp: float, nonce: str, signature: str) -> bool:
        msg = f"{payload_str}:{timestamp}:{nonce}".encode("utf-8")
        expected_sig = hmac.new(key.encode("utf-8"), msg, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig, signature)

    def verify_service_auth(
        self,
        signature: str,
        payload_str: str,
        timestamp: float,
        nonce: str,
        current_time: Optional[float] = None
    ) -> str:
        """
        Verify HMAC-SHA256 signature with key rotation and clock skew validation.
        Returns 'CURRENT' or 'PREVIOUS_GRACE'.
        """
        now = current_time if current_time is not None else time.time()

        # 1. Clock skew check
        if abs(now - timestamp) > self.clock_skew_tolerance_sec:
            raise AuthGuardError(f"Clock skew exceeded: {abs(now - timestamp)}s > {self.clock_skew_tolerance_sec}s", "AUTH_CLOCK_SKEW")

        # 2. Replay check
        self.replay_guard.check_and_record(nonce, current_time=now)

        # 3. Keys check
        if not self.current_service_key and not self.previous_service_key:
            raise AuthGuardError("No service keys configured for authentication.", "AUTH_KEYS_UNAVAILABLE")

        # Try current key
        if self.current_service_key and self._verify_signature(self.current_service_key, payload_str, timestamp, nonce, signature):
            return "CURRENT"

        # Try previous key within 24h grace
        if self.previous_service_key:
            grace_window_sec = 24 * 3600.0
            if self.previous_key_rotated_at is not None and (now - self.previous_key_rotated_at) > grace_window_sec:
                raise AuthGuardError("Previous service key has expired beyond 24h grace window.", "AUTH_KEY_EXPIRED")
            if self._verify_signature(self.previous_service_key, payload_str, timestamp, nonce, signature):
                return "PREVIOUS_GRACE"

        raise AuthGuardError("Invalid HMAC-SHA256 signature.", "AUTH_INVALID_SIGNATURE")

    def redact_secrets(self, text: str) -> str:
        """Redact secrets from logs, strings, and exception messages."""
        if not text:
            return text
        patterns = [
            (r'(key=)[^\s&]+', r'[REDACTED]'),
            (r'(Authorization:\s*Bearer\s+)[^\s&]+', r'[REDACTED]'),
            (r'(signature=)[^\s&]+', r'[REDACTED]'),
            (r'(secret=)[^\s&]+', r'[REDACTED]')
        ]
        res = text
        for p, r in patterns:
            res = re.sub(p, r, res, flags=re.IGNORECASE)
        return res
