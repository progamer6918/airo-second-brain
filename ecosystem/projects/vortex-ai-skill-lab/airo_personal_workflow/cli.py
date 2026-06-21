import argparse
import json
from datetime import date

from airo_personal_workflow.db.init_db import init_db
from airo_personal_workflow.db.repository import (
    check_installment,
    monthly_summary,
    record_from_text,
)
from airo_personal_workflow.exports.exporter import (
    export_installments_csv,
    export_summary_json,
    export_transactions_csv,
)
from airo_personal_workflow.reports.monthly import generate_monthly_markdown
from airo_personal_workflow.adapters.google.workspace_dry_run import generate_google_workspace_plan
from airo_personal_workflow.intents.parser import parse_user_message

def print_json(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))

def main() -> None:
    parser = argparse.ArgumentParser(description="Airo Personal Workflow CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init")

    p_parse = sub.add_parser("parse")
    p_parse.add_argument("text")

    p_record = sub.add_parser("record")
    p_record.add_argument("text")

    p_check = sub.add_parser("check-installment")
    p_check.add_argument("name")

    p_summary = sub.add_parser("summary")
    p_summary.add_argument("--period", default=date.today().strftime("%Y-%m"))

    p_export = sub.add_parser("export")
    p_export.add_argument("--period", default=date.today().strftime("%Y-%m"))

    p_report = sub.add_parser("report")
    p_report.add_argument("--period", default=date.today().strftime("%Y-%m"))

    p_google = sub.add_parser("google-dry-run")
    p_google.add_argument("--period", default=date.today().strftime("%Y-%m"))

    args = parser.parse_args()

    if args.command == "init":
        init_db()
        return

    if args.command == "parse":
        print_json(parse_user_message(args.text))
        return

    if args.command == "record":
        print_json(record_from_text(args.text))
        return

    if args.command == "check-installment":
        print_json(check_installment(args.name))
        return

    if args.command == "summary":
        print_json(monthly_summary(args.period))
        return

    if args.command == "export":
        summary = monthly_summary(args.period)
        print_json({
            "period": args.period,
            "transactions_csv": export_transactions_csv(args.period),
            "installments_csv": export_installments_csv(args.period),
            "summary_json": export_summary_json(summary, args.period),
        })
        return

    if args.command == "report":
        print_json({
            "period": args.period,
            "monthly_report": generate_monthly_markdown(args.period),
        })
        return

    if args.command == "google-dry-run":
        print_json(generate_google_workspace_plan(args.period))
        return

if __name__ == "__main__":
    main()
