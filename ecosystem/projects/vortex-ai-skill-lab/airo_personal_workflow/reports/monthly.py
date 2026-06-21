from pathlib import Path

from airo_personal_workflow.db.repository import monthly_summary

REPORT_DIR = Path("reports/personal-workflow")

def money(value: int | float | None) -> str:
    value = int(value or 0)
    return "Rp" + f"{value:,}".replace(",", ".")

def generate_monthly_markdown(period: str) -> str:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    summary = monthly_summary(period)

    trx = summary["transactions"]
    inst = summary["installment_payments"]

    lines = [
        f"# Airo Personal Finance Report - {period}",
        "",
        "## Ringkasan Utama",
        "",
        f"- Total transaksi harian: {money(trx.get('total'))}",
        f"- Jumlah transaksi harian: {trx.get('count', 0)}",
        f"- Total pembayaran cicilan: {money(inst.get('total'))}",
        f"- Jumlah pembayaran cicilan: {inst.get('count', 0)}",
        "",
        "## Transaksi Berdasarkan Kategori",
        "",
        "| Kategori | Total | Jumlah |",
        "|---|---:|---:|",
    ]

    for row in summary["transactions_by_category"]:
        lines.append(f"| {row.get('category')} | {money(row.get('total'))} | {row.get('count')} |")

    lines.extend([
        "",
        "## Catatan",
        "",
        "Laporan ini dibuat dari SQLite source of truth lokal Airo.",
        "Google Sheets, Docs, dan Drive akan menjadi output layer pada fase berikutnya.",
    ])

    out = REPORT_DIR / f"monthly_report_{period}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(out)
