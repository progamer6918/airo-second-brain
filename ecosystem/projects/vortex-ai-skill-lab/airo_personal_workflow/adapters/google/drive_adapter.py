"""Google Drive adapter placeholder.

No real upload is performed in this phase.
"""

class GoogleDriveAdapter:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def upload_attachment(self, local_path: str) -> dict:
        return {"adapter": "drive", "local_path": local_path, "dry_run": self.dry_run, "status": "planned"}
