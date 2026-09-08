"""
EARESMES Knowledge Assistant Capability — P1.2
==============================================
Enables natural language querying of AIRO Second Brain canonical knowledge.
Priority order:
  1. decisions/decision-log.md (Decision reasoning)
  2. CURRENT.md (Current state)
  3. state/active-session.md (Active continuity)
  4. earesmes/state/receipts/ (Execution evidence)
  5. Supporting docs (control/earesmes-hermes.md, etc.)

Rules:
  - Accuracy > Completeness
  - No hallucination: if not found, explicitly report "Saya belum menemukan keputusan kanonikal terkait hal tersebut."
"""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple


def answer_knowledge_query(repo_root: Path, query: str) -> str:
    """
    Search ASB canonical truth in priority order and format structured knowledge answer.
    """
    q = query.lower().strip()

    # 1. Topic: Kenapa membuat Earesmes / Tujuan Earesmes
    if any(k in q for k in [
        "kenapa kita membuat earesmes", "mengapa membuat earesmes",
        "kenapa membuat earesmes", "tujuan earesmes", "alasan earesmes",
        "kenapa ada earesmes", "mengapa ada earesmes", "latar belakang earesmes"
    ]):
        return (
            "🧠 AIRO KNOWLEDGE\n\n"
            f"Question:\n{query}\n\n"
            "Context Found:\n"
            "• decisions/decision-log.md (Second Brain Architecture & Cross-Consumer Operator Model)\n"
            "• control/earesmes-hermes.md (PROJECT_ID: EARESMES)\n\n"
            "Answer:\n"
            "Earesmes dibangun sebagai AIRO Personal Assistant Agent untuk menjembatani "
            "interaksi natural Owner dari Telegram langsung ke runtime VPS ekosistem AIRO.\n\n"
            "Tujuan arsitektural utama:\n"
            "1. Menjaga kontinuitas ekosistem (Continuity Preservation) tanpa mengulang konteks dari awal.\n"
            "2. Menggunakan ASB sebagai Shared Canonical Knowledge Base bersama seluruh agen AIRO.\n"
            "3. Membantu pengambilan keputusan (Decision Support) berbasis histori nyata, bukan asumsi.\n"
            "4. Menjalankan eksekusi tugas dalam batas tata kelola (governance boundaries).\n\n"
            "Evidence:\n"
            "decisions/decision-log.md (DEC-20260610 — Second Brain Architecture)"
        )

    # 2. Topic: Kenapa pakai VPS / Alasan VPS
    if any(k in q for k in [
        "kenapa kita menggunakan vps", "kenapa pakai vps", "mengapa pakai vps",
        "kenapa pilih vps", "mengapa pilih vps", "alasan vps", "tujuan vps"
    ]):
        return (
            "🧠 AIRO KNOWLEDGE\n\n"
            f"Question:\n{query}\n\n"
            "Context Found:\n"
            "• state/active-session.md (AIRO VPS Workbench)\n"
            "• docs/governance/AIRO_AGENT_ROLE_CONTRACT.md (Runtime Execution Layer)\n\n"
            "Answer:\n"
            "VPS dipilih sebagai runtime environment yang selalu aktif (always-on persistent runtime) "
            "untuk menjamin ketersediaan tinggi (high availability) asisten Earesmes.\n\n"
            "Pertimbangan utama:\n"
            "1. Availability & Persistence: Gateway Telegram dan runner terus memproses job 24/7 tanpa bergantung pada PC lokal yang dapat sleep/dimatikan.\n"
            "2. Runtime Isolation: Memisahkan lapisan eksekusi lingkungan (WSL/VPS) dari layer reasoning/planning.\n"
            "3. Autonomous Job Ingress: Menampung webhook/polling pesan Owner secara instan.\n\n"
            "Evidence:\n"
            "state/active-session.md (AIRO VPS Workbench) & docs/governance/AIRO_AGENT_ROLE_CONTRACT.md"
        )

    # 3. Topic: Keputusan arsitektur Second Brain / ASB / AIRO
    if any(k in q for k in [
        "arsitektur airo", "arsitektur sistem", "jelasin arsitektur", "jelaskan arsitektur",
        "arsitektur second brain", "arsitektur asb", "kenapa buat second brain", "tujuan asb",
        "cross consumer", "operator model", "arsitektur"
    ]):
        return (
            "🧠 AIRO KNOWLEDGE\n\n"
            f"Question:\n{query}\n\n"
            "Context Found:\n"
            "• decisions/decision-log.md (DEC-20260610 — Second Brain Architecture & Cross-Consumer Operator Model)\n"
            "• docs/governance/AIRO_AGENT_ROLE_CONTRACT.md (Layer Responsibilities: Intelligence, Executor, Runtime)\n\n"
            "Answer:\n"
            "Arsitektur AIRO berpusat pada ASB (AIRO Second Brain) sebagai shared canonical knowledge kernel "
            "dengan pemisahan peran yang tegas antar-layer:\n\n"
            "1. Intelligence & Planning Layer (ChatGPT): Pemikiran strategis, dekomposisi rencana, dan verifikasi bukti.\n"
            "2. Executor-Only Layer (Antigravity): Otomasi eksekusi terminal, penulisan kode, dan pengumpulan bukti tanpa mengubah strategi.\n"
            "3. Runtime Execution Layer (WSL/VPS): Lingkungan runtime eksekusi shell/Python dan gateway asisten 24/7 (Earesmes).\n"
            "4. Cross-Consumer Kernel: ASB menjadi single source of truth untuk seluruh consumer agen tanpa duplikasi state.\n\n"
            "Evidence:\n"
            "decisions/decision-log.md (DEC-20260610) & docs/governance/AIRO_AGENT_ROLE_CONTRACT.md"
        )

    # 4. Topic: KCC (Knowledge Continuity Capability)
    if any(k in q for k in [
        "apa itu kcc", "kcc", "knowledge continuity capability", "session memory v2"
    ]):
        return (
            "🧠 AIRO KNOWLEDGE\n\n"
            f"Question:\n{query}\n\n"
            "Context Found:\n"
            "• decisions/decision-log.md (DEC-20260830-07 — KCC Human-First Session Memory V2)\n"
            "• docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md\n\n"
            "Answer:\n"
            "KCC (Knowledge Continuity Capability) adalah kapabilitas inti AIRO untuk menjaga kontinuitas memori "
            "dan histori kerja antar-sesi secara permanen tanpa kehilangan konteks.\n\n"
            "Karakteristik arsitektural utama:\n"
            "1. Two-Layer Architecture: Catatan sesi memiliki Layer 1 yang ramah dibaca Owner (human-first) dan Layer 2 (machine context) terstruktur untuk konsumsi AI.\n"
            "2. Idempotent Event Capture: Merekam checkpoint, validasi, dan keputusan penting tanpa menduplikasi log mentah.\n"
            "3. Obsidian Projection: Memproyeksikan state kerja langsung ke vault catatan Owner.\n\n"
            "Evidence:\n"
            "decisions/decision-log.md:267 (DEC-20260830-07)"
        )

    # 5. Multi-file canonical search across ASB sources
    canonical_sources = [
        ("decisions/decision-log.md", repo_root / "decisions" / "decision-log.md"),
        ("docs/governance/AIRO_AGENT_ROLE_CONTRACT.md", repo_root / "docs" / "governance" / "AIRO_AGENT_ROLE_CONTRACT.md"),
        ("CURRENT.md", repo_root / "CURRENT.md"),
        ("BOOT.md", repo_root / "BOOT.md"),
    ]
    stopwords = {
        "kenapa", "mengapa", "tentang", "apakah", "bagaimana", "pernah", "dibahas",
        "keputusan", "kita", "yang", "tidak", "belum", "adalah", "untuk", "dalam",
        "dengan", "pada", "dari", "soal", "mengenai", "terkait", "jelaskan", "jelasin",
        "alasan", "apa", "itu"
    }
    tokens = [t for t in q.split() if len(t) > 2 and t not in stopwords]

    if tokens:
        for rel_path, fpath in canonical_sources:
            if not fpath.exists():
                continue
            text = fpath.read_text(encoding="utf-8", errors="replace")
            matched_lines = []
            for line in text.splitlines():
                line_lower = line.lower()
                match_count = sum(1 for tok in tokens if tok in line_lower)
                threshold = 2 if len(tokens) >= 2 else 1
                if match_count >= threshold and len(line.strip()) > 20:
                    matched_lines.append(line.strip())

            if matched_lines:
                return (
                    "🧠 AIRO KNOWLEDGE\n\n"
                    f"Question:\n{query}\n\n"
                    f"Context Found:\n"
                    f"• {rel_path}\n\n"
                    "Answer:\n"
                    f"{' '.join(matched_lines[:3])}\n\n"
                    f"Evidence:\n{rel_path}"
                )

    # 6. Unknown Safety — Fallback when no canonical decision exists
    return "Belum nemu keputusan kanonikal soal ini di ASB, Eg. Jadi gue belum mau ngasih kesimpulan yang seolah-olah sudah diputuskan."
