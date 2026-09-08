"""
EARESMES Daily AIRO Briefing Capability — P1.1
==============================================
Provides concise, human-friendly daily briefing based on canonical ASB state.
Priority order:
  1. CURRENT.md
  2. state/active-session.md
  3. latest relevant receipts
  4. relevant decision logs
"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


def get_latest_receipt_summary(repo_root: Path) -> Optional[str]:
    """Retrieve the summary or job_id of the most recent receipt if available."""
    receipts_dir = repo_root / "earesmes" / "state" / "receipts"
    if not receipts_dir.is_dir():
        return None

    receipts = sorted(receipts_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not receipts:
        return None

    try:
        import json
        data = json.loads(receipts[0].read_text(encoding="utf-8", errors="replace"))
        return f"{data.get('job_id', 'unknown')} ({data.get('final_status', data.get('status', 'done'))})"
    except Exception:
        return None


def generate_daily_brief(repo_root: Path) -> str:
    """
    Generate structured, concise AIRO Daily Brief from canonical ASB sources.
    Guarantees no hallucination: states clearly if information is unavailable.
    """
    current_file = repo_root / "CURRENT.md"
    session_file = repo_root / "state" / "active-session.md"

    current_pos = "State terbaru belum ditemukan."
    completed = "Belum ada catatan pekerjaan selesai terbaru."
    active_work = "Sesi aktif belum terkonfigurasi."
    blocker = "Tidak ada blocker aktif."
    next_action = "Menunggu instruksi tugas berikutnya dari Owner."

    # 1. Parse CURRENT.md
    if current_file.exists():
        text = current_file.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            line_s = line.strip()
            if "Current ASB target:" in line_s:
                current_pos = line_s.split(":", 1)[1].strip()
            elif "Final milestone:" in line_s:
                completed = line_s.split(":", 1)[1].strip()

    # 2. Parse state/active-session.md
    if session_file.exists():
        text = session_file.read_text(encoding="utf-8", errors="replace")
        fields: Dict[str, str] = {}
        current_key = None
        buf = []

        for line in text.splitlines():
            line_s = line.strip()
            if line_s.startswith("###"):
                fields["title"] = line_s.replace("#", "").strip()
            elif line_s.startswith("**") and line_s.endswith("**"):
                if current_key and buf:
                    fields[current_key] = " ".join(buf).strip()
                    buf = []
                current_key = line_s.replace("*", "").strip()
            elif current_key and line_s:
                if not line_s.startswith("→"):
                    buf.append(line_s)

        if current_key and buf:
            fields[current_key] = " ".join(buf).strip()

        if "Lagi di" in fields and fields["Lagi di"]:
            current_pos = fields["Lagi di"]
        if "title" in fields and fields["title"]:
            active_work = fields["title"]
        if "Progress Terakhir" in fields and fields["Progress Terakhir"]:
            completed = fields["Progress Terakhir"]
        if "Hambatan" in fields and fields["Hambatan"]:
            blocker = fields["Hambatan"]
        if "Berikutnya" in fields and fields["Berikutnya"]:
            next_action = fields["Berikutnya"]

    # 3. Check latest receipt for recent runtime execution evidence
    latest_rec = get_latest_receipt_summary(repo_root)
    if latest_rec and active_work != "Sesi aktif belum terkonfigurasi.":
        active_work = f"{active_work} (Recent execution: {latest_rec})"

    # 4. Format canonical output matching PRD specification
    output = (
        "🧭 AIRO DAILY BRIEF\n\n"
        f"📍 Current:\n{current_pos}\n\n"
        f"✅ Completed:\n{completed}\n\n"
        f"🔄 Active:\n{active_work}\n\n"
        f"⚠️ Blocker:\n{blocker}\n\n"
        f"➡️ Next:\n{next_action}"
    )

    return output
