#!/usr/bin/env python3
"""
AIRO Google Sheets client v1.1.2.

Authentication priority:
1. OAuth Desktop Client:
   - AIRO_GOOGLE_OAUTH_CLIENT_SECRET_PATH
   - AIRO_GOOGLE_OAUTH_TOKEN_PATH
2. Service account fallback:
   - AIRO_GOOGLE_SERVICE_ACCOUNT_JSON_PATH
   - AIRO_GOOGLE_SERVICE_ACCOUNT_JSON

No approval phrase.
No secrets are stored in repo.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


@dataclass(frozen=True)
class SheetKeyTarget:
    tab_name: str
    header_row: int
    key_header: str
    hash_header: str | None = None
    snapshot_key: str | None = None


KEY_TARGETS = [
    SheetKeyTarget("💸 Transactions", 1, "duplicate_key", "sync_hash"),
    SheetKeyTarget("💳 Credit Card", 3, "linked_txn_id", None),
    SheetKeyTarget("🧾 Review Queue", 1, "queue_id", "sync_hash"),
    SheetKeyTarget("🏠 Cicilan Rumah", 11, "payment_id", None),
    SheetKeyTarget("🔄 Sync Log", 2, "sync_id", None),
    SheetKeyTarget("🥇 Aset", 3, "savings_event_id", "sync_hash", "🥇 Aset::savings_transfer_ledger"),
    SheetKeyTarget("🥇 Aset", 24, "gold_event_id", "sync_hash", "🥇 Aset::gold_ledger"),
]


def quote_sheet_name(tab_name: str) -> str:
    escaped = tab_name.replace("'", "''")
    return f"'{escaped}'"


def column_letter(index_1_based: int) -> str:
    if index_1_based < 1:
        raise ValueError("column index must be >= 1")

    out = ""
    n = index_1_based

    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out

    return out


class GoogleSheetsClient:
    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self._tmp_credential_path: str | None = None
        self.service = self._build_service()

    def _build_service(self):
        try:
            from googleapiclient.discovery import build
        except Exception as exc:
            raise RuntimeError(
                "Missing Google API dependency. Use AIRO venv and install google-api-python-client."
            ) from exc

        credentials = self._build_oauth_credentials_or_service_account()

        return build("sheets", "v4", credentials=credentials, cache_discovery=False)

    def _build_oauth_credentials_or_service_account(self):
        oauth_secret_path = os.environ.get("AIRO_GOOGLE_OAUTH_CLIENT_SECRET_PATH", "").strip()
        oauth_token_path = os.environ.get("AIRO_GOOGLE_OAUTH_TOKEN_PATH", "").strip()

        if oauth_secret_path:
            return self._build_oauth_credentials(
                Path(oauth_secret_path).expanduser(),
                Path(oauth_token_path or "~/.config/airo-personal-workflow/oauth-token.json").expanduser(),
            )

        return self._build_service_account_credentials()

    def _build_oauth_credentials(self, client_secret_path: Path, token_path: Path):
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
        except Exception as exc:
            raise RuntimeError(
                "Missing OAuth dependency. Install inside venv: "
                "python -m pip install google-auth-oauthlib"
            ) from exc

        if not client_secret_path.is_file():
            raise RuntimeError(f"OAuth client secret file not found: {client_secret_path}")

        token_path.parent.mkdir(parents=True, exist_ok=True)

        credentials = None

        if token_path.is_file():
            credentials = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if credentials and credentials.valid:
            return credentials

        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            token_path.write_text(credentials.to_json(), encoding="utf-8")
            token_path.chmod(0o600)
            return credentials

        flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_path), SCOPES)

        print("AIRO_OAUTH_LOGIN_REQUIRED=true")
        print("A browser authorization flow will start. If no browser opens, copy the URL shown by Google auth into your browser.")

        credentials = flow.run_local_server(
            host="localhost",
            port=0,
            open_browser=False,
            authorization_prompt_message=(
                "\nOpen this URL in your browser, approve access, then return here:\n{url}\n"
            ),
            success_message="AIRO OAuth login complete. You can close this browser tab.",
        )

        token_path.write_text(credentials.to_json(), encoding="utf-8")
        token_path.chmod(0o600)
        print(f"AIRO_OAUTH_TOKEN_WRITTEN={token_path}")
        return credentials

    def _service_account_credential_path(self) -> str:
        path = os.environ.get("AIRO_GOOGLE_SERVICE_ACCOUNT_JSON_PATH", "").strip()
        inline = os.environ.get("AIRO_GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()

        if path:
            return str(Path(path).expanduser())

        if inline:
            json.loads(inline)
            tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
            tmp.write(inline)
            tmp.close()
            self._tmp_credential_path = tmp.name
            return tmp.name

        raise RuntimeError(
            "Google credentials missing. Set OAuth env vars "
            "(AIRO_GOOGLE_OAUTH_CLIENT_SECRET_PATH and AIRO_GOOGLE_OAUTH_TOKEN_PATH) "
            "or service account env vars."
        )

    def _build_service_account_credentials(self):
        try:
            from google.oauth2 import service_account
        except Exception as exc:
            raise RuntimeError("Missing service account dependency: google-auth") from exc

        return service_account.Credentials.from_service_account_file(
            self._service_account_credential_path(),
            scopes=SCOPES,
        )

    def get_values(self, a1_range: str) -> list[list[Any]]:
        response = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheet_id, range=a1_range)
            .execute()
        )
        return response.get("values", [])

    def append_values(self, tab_name: str, values: list[Any]) -> dict[str, Any]:
        return (
            self.service.spreadsheets()
            .values()
            .append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{quote_sheet_name(tab_name)}!A1",
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body={"values": [values]},
            )
            .execute()
        )

    def append_values_to_range(self, tab_name: str, a1_range: str, values: list[Any]) -> dict[str, Any]:
        return (
            self.service.spreadsheets()
            .values()
            .append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{quote_sheet_name(tab_name)}!{a1_range}",
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body={"values": [values]},
            )
            .execute()
        )

    def update_values(self, tab_name: str, row_number: int, values: list[Any]) -> dict[str, Any]:
        end_col = column_letter(len(values))
        a1_range = f"{quote_sheet_name(tab_name)}!A{row_number}:{end_col}{row_number}"

        return (
            self.service.spreadsheets()
            .values()
            .update(
                spreadsheetId=self.spreadsheet_id,
                range=a1_range,
                valueInputOption="USER_ENTERED",
                body={"values": [values]},
            )
            .execute()
        )

    def update_values_to_range(self, tab_name: str, a1_range: str, values: list[Any]) -> dict[str, Any]:
        return (
            self.service.spreadsheets()
            .values()
            .update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{quote_sheet_name(tab_name)}!{a1_range}",
                valueInputOption="USER_ENTERED",
                body={"values": [values]},
            )
            .execute()
        )

    def export_sheet_keys(self) -> dict[str, Any]:
        tabs: dict[str, list[dict[str, Any]]] = {}

        for target in KEY_TARGETS:
            tabs[target.snapshot_key or target.tab_name] = self._export_tab_keys(target)

        return {
            "title": "AIRO FINANCE SHEET KEYS SNAPSHOT",
            "version": "v1.1.2",
            "mode": "live_google_read",
            "google_write_performed": False,
            "tabs": tabs,
        }

    def _export_tab_keys(self, target: SheetKeyTarget) -> list[dict[str, Any]]:
        values = self.get_values(f"{quote_sheet_name(target.tab_name)}!1:3000")

        if len(values) < target.header_row:
            return []

        headers = [str(v or "").strip() for v in values[target.header_row - 1]]
        key_idx = headers.index(target.key_header) if target.key_header in headers else -1
        hash_idx = headers.index(target.hash_header) if target.hash_header and target.hash_header in headers else -1

        if key_idx < 0:
            return []

        out: list[dict[str, Any]] = []

        for offset, row in enumerate(values[target.header_row:], start=target.header_row + 1):
            key = str(row[key_idx] if key_idx < len(row) else "").strip()

            if not key:
                continue

            sync_hash = ""
            if hash_idx >= 0 and hash_idx < len(row):
                sync_hash = str(row[hash_idx] or "").strip()

            out.append(
                {
                    "row_number": offset,
                    "duplicate_key": key,
                    "sync_hash": sync_hash,
                }
            )

        return out


def build_client_from_env() -> GoogleSheetsClient:
    spreadsheet_id = os.environ.get("AIRO_SPREADSHEET_ID", "").strip()

    if not spreadsheet_id:
        raise RuntimeError("AIRO_SPREADSHEET_ID is required.")

    return GoogleSheetsClient(spreadsheet_id)
