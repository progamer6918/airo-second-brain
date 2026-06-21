from pathlib import Path

from airo_personal_workflow.db.repository import monthly_summary
from airo_personal_workflow.exports.exporter import (
    export_installments_csv,
    export_summary_json,
    export_transactions_csv,
)
from airo_personal_workflow.reports.monthly import generate_monthly_markdown


def _meta(path: str) -> dict:
    p = Path(path)
    return {
        "path": path,
        "exists": p.exists(),
        "size": p.stat().st_size if p.exists() else 0,
    }


def generate_google_workspace_plan(period: str) -> dict:
    summary = monthly_summary(period)

    transactions_csv = export_transactions_csv(period)
    installments_csv = export_installments_csv(period)
    summary_json = export_summary_json(summary, period)
    monthly_report_md = generate_monthly_markdown(period)

    return {
        "period": period,
        "dry_run": True,
        "targets": {
            "sheets": [
                {
                    "name": f"Airo Transactions {period}",
                    "source": transactions_csv,
                    "mode": "planned_replace_tab",
                },
                {
                    "name": f"Airo Installment Payments {period}",
                    "source": installments_csv,
                    "mode": "planned_replace_tab",
                },
            ],
            "docs": [
                {
                    "name": f"Airo Monthly Report {period}",
                    "source": monthly_report_md,
                    "mode": "planned_create_or_update_doc",
                }
            ],
            "drive": [
                {
                    "name": "Airo Receipts Folder",
                    "mode": "planned_only_no_upload",
                }
            ],
            "calendar": [
                {
                    "name": "Due Date Reminders",
                    "mode": "planned_only_no_write",
                }
            ],
        },
        "files": {
            "transactions_csv": _meta(transactions_csv),
            "installments_csv": _meta(installments_csv),
            "summary_json": _meta(summary_json),
            "monthly_report_md": _meta(monthly_report_md),
        },
        "safety": {
            "oauth_used": False,
            "google_api_called": False,
            "token_required": False,
            "drive_upload": False,
            "calendar_write": False,
            "gmail_access": False,
        },
    }
