"""Google Docs adapter placeholder.

No real document is created in this phase.
"""

class GoogleDocsAdapter:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def create_monthly_report(self, period: str, markdown_path: str) -> dict:
        return {
            "adapter": "docs",
            "period": period,
            "markdown_path": markdown_path,
            "dry_run": self.dry_run,
            "status": "planned",
        }
