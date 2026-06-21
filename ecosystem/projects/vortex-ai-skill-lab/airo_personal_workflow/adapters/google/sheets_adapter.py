"""Google Sheets adapter placeholder.

No OAuth token, secret, cookie, or credential is stored here.
This adapter will export SQLite data to Google Sheets in a later phase.
"""

class GoogleSheetsAdapter:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def export_transactions(self, period: str) -> dict:
        return {"adapter": "sheets", "period": period, "dry_run": self.dry_run, "status": "planned"}
