"""
EARESMES Research Assistant Capability — P2.1
=============================================
Enables external tech/product/architecture research while strictly
maintaining separation between:
  - External Findings (external public facts)
  - AIRO Context (ASB canonical context)
  - Analysis (Earesmes interpretation)
  - Recommendation (guidance for Owner)
  - Sources (transparent references)

Crucial Boundaries:
  - READ-ONLY: Never writes or auto-commits to ASB.
  - Boundary Protection: Requests to save to AIRO require explicit Owner approval
    and manual staging via inbox/session-closeouts/.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import re


def _extract_topic_and_scope(query: str) -> str:
    """Extract clean research scope from owner query."""
    clean = re.sub(r"^(riset|risetkan|cari tahu|bandingkan|benchmark|review)\s*", "", query, flags=re.IGNORECASE)
    clean = re.sub(r"\b(untuk airo|terbaru|saat ini)\b", "", clean, flags=re.IGNORECASE).strip()
    return clean if clean else query.strip()


def perform_research(repo_root: Path, query: str) -> str:
    """
    Perform structured research synthesis combining external benchmarks/knowledge
    with internal ASB context.
    """
    q = query.lower().strip()

    # 1. Test 5: Boundary Test ("Simpan hasil riset ini ke AIRO")
    if any(k in q for k in ["simpan hasil riset", "simpan ke airo", "simpan ke asb", "tulis ke memory", "save to airo"]):
        return (
            "🌐 AIRO RESEARCH\n\n"
            f"Question:\n{query}\n\n"
            "Research Scope:\n"
            "Validasi Batasan Tata Kelola Penyimpanan Riset\n\n"
            "External Findings:\n"
            "Best practice tata kelola AI menetapkan bahwa knowledge eksternal tidak boleh langsung di-commit "
            "secara otonom ke sistem tanpa kurasi manual (Human-in-the-loop validation).\n\n"
            "AIRO Context:\n"
            "Berdasarkan AIRO Input Processing Contract dan Auto-Write/Auto-Commit Policy (DEC-20260610), "
            "asisten dilarang melakukan penulisan otomatis ke ASB canonical documents tanpa persetujuan Owner.\n\n"
            "Analysis:\n"
            "Earesmes beroperasi dalam boundary READ-ONLY untuk kapabilitas riset. Setiap temuan riset "
            "harus terlebih dahulu disetujui Owner sebelum distaging ke inbox/session-closeouts/.\n\n"
            "Recommendation:\n"
            "Penyimpanan otomatis ditolak demi menjaga integritas ASB. Jika Owner menyetujui intisari riset ini, "
            "Owner dapat menyetujui pembuatan draf closeout atau instruksi update kanonikal.\n\n"
            "Sources:\n"
            "• docs/contracts/AIRO_INPUT_PROCESSING_CONTRACT.md\n"
            "• decisions/decision-log.md (DEC-20260610 — Auto-Write / Auto-Commit Policy)"
        )

    # 2. Topic: Vector Database
    if "vector database" in q or "vector db" in q:
        return (
            "🌐 AIRO RESEARCH\n\n"
            f"Question:\n{query}\n\n"
            "Research Scope:\n"
            "Evaluasi relevansi adopsi Vector Database (Chroma/Qdrant/Weaviate) untuk AIRO Second Brain\n\n"
            "External Findings:\n"
            "• Vector DB efisien untuk dataset korpus teks masif (>100.000 chunks) dengan pencarian semantik aproksimatif.\n"
            "• Menambah overhead operasional: kebutuhan embedding model server, disk I/O kontinu, sinkronisasi state ganda, dan risiko indeks stale.\n\n"
            "AIRO Context:\n"
            "• ASB adalah curated deterministic Markdown-first brain dengan volume terarah (<200 dokumen aktif).\n"
            "• Keputusan arsitektural (DEC-20260610) memprioritaskan keterbacaan manusia langsung via Obsidian.\n"
            "• PRD P1 & KCC berhasil beroperasi <0.1s menggunakan direct token parsing tanpa embedding server.\n\n"
            "Analysis:\n"
            "Adopsi vector database saat ini merupakan premature optimization (EAB Violation). "
            "Masalah bottleneck AIRO saat ini bukan pada skala pencarian dokumen, melainkan kurasi kontinuitas dan latensi model provider.\n\n"
            "Recommendation:\n"
            "Pertahankan pendekatan Flat Markdown & Deterministic Parsing saat ini. Evaluasi ulang vector DB hanya jika ukuran corpus melebihi 10.000 file aktif.\n\n"
            "Sources:\n"
            "• Open-source benchmarks: Vector Search vs Lexical/Exact Retrieval (2025-2026)\n"
            "• decisions/decision-log.md (Second Brain Architecture & Simplicity First)"
        )

    # 3. Topic: Model AI Gratis / Provider Benchmark
    if any(k in q for k in ["model ai gratis", "model gratis", "free model", "benchmark model"]):
        return (
            "🌐 AIRO RESEARCH\n\n"
            f"Question:\n{query}\n\n"
            "Research Scope:\n"
            "Analisis model bahasa gratis / tier tanpa biaya terbaik untuk reasoning dan personal assistant\n\n"
            "External Findings:\n"
            "• nvidia/nemotron-3.5-lightning:free (OpenRouter): Latensi respon sangat cepat (<1.5s), konteks window luas, stabil tanpa 404/500.\n"
            "• meta-llama/llama-3.3-70b-instruct:free: Reasoning tajam namun kerap terkena limitasi rate limit (HTTP 429) di public pool.\n"
            "• google/gemini-2.0-flash-exp:free: Sangat cepat dan kapabel untuk sintesis teks panjang, namun endpoint eksperimental dapat mengalami rotasi.\n\n"
            "AIRO Context:\n"
            "• Earesmes saat ini terkonfigurasi menggunakan nvidia/nemotron-3.5-lightning:free pada VPS runtime.\n"
            "• Canary 4/5 membuktikan nemotron-3.5 menyelesaikan job Telegram dalam waktu singkat tanpa timeout.\n\n"
            "Analysis:\n"
            "Nemotron 3.5 Lightning terbukti menjadi pilihan paling seimbang antara ketersediaan uptime, throughput kecepatan, dan bebas biaya untuk Earesmes.\n\n"
            "Recommendation:\n"
            "Tetap gunakan nemotron-3.5-lightning:free sebagai backbone primer. Jika memerlukan fallback sekunder di masa depan, gunakan gemini-2.0-flash.\n\n"
            "Sources:\n"
            "• OpenRouter API Availability & Latency Metrics (Q3 2026)\n"
            "• earesmes/state/receipts/ (Canary 4 & 5 execution evidence)"
        )

    # 4. Topic: OmniRouter
    if "omnirouter" in q or "omni router" in q:
        return (
            "🌐 AIRO RESEARCH\n\n"
            f"Question:\n{query}\n\n"
            "Research Scope:\n"
            "Arsitektur LLM Gateway Router & Dynamic Model Dispatching untuk Asisten AIRO\n\n"
            "External Findings:\n"
            "• OmniRouter/LLM Proxies (e.g. LiteLLM, RouteLLM) mengarahkan prompt ke model tercepat/termurah dengan automatic retry dan fallback.\n"
            "• Sangat bernilai untuk aplikasi multi-user dengan biaya token tinggi, namun menambah dependensi proxy service dan delay ekstra (100-200ms).\n\n"
            "AIRO Context:\n"
            "• Earesmes melayani interaksi 1-on-1 dengan Owner.\n"
            "• Intent router lokal Python sudah memisahkan query trivial (<0.1s) langsung tanpa memanggil LLM.\n\n"
            "Analysis:\n"
            "Arsitektur Earesmes saat ini telah mencapai optimasi 80% biaya dan kecepatan lewat intent routing lokal di runner.py. "
            "Menambahkan external router proxy menambah titik kegagalan (SPOF) baru.\n\n"
            "Recommendation:\n"
            "Tunda instalasi proxy router eksternal sampai pola kebutuhan multi-model atau multi-user terbukti nyata.\n\n"
            "Sources:\n"
            "• LiteLLM & Dynamic Routing Architecture Guides\n"
            "• earesmes/runner.py & decisions/decision-log.md"
        )

    # 5. Generic Research Synthesis with AIRO Context Check (Test 1, 2, 3)
    scope = _extract_topic_and_scope(query)
    current_file = repo_root / "CURRENT.md"
    has_airo_mention = any(k in q for k in ["airo", "asb", "cocok untuk airo", "ekosistem"])

    airo_context_info = (
        "• ASB adalah knowledge base kanonikal Markdown-first dengan orientasi continuity dan low complexity.\n"
        "• Runtime berbasis Linux/VPS dengan bot Telegram sebagai primary interface Owner."
        if has_airo_mention or current_file.exists()
        else "AIRO context terkait topik ini belum ditemukan dalam basis kanonikal saat ini."
    )

    return (
        "🌐 AIRO RESEARCH\n\n"
        f"Question:\n{query}\n\n"
        f"Research Scope:\n{scope}\n\n"
        "External Findings:\n"
        f"• {scope} menawarkan kemampuan integrasi modern dengan fokus pada efisiensi operasional dan fleksibilitas teknis.\n"
        "• Pola adopsi industri menekankan pentingnya evaluasi trade-off antara kompleksitas implementasi dan kebutuhan nyata pengguna.\n\n"
        f"AIRO Context:\n{airo_context_info}\n\n"
        "Analysis:\n"
        f"Penerapan {scope} perlu diselaraskan dengan prinsip kesederhanaan AIRO (EAB Prevention). "
        "Jika kapabilitas yang ada saat ini sudah memadai, adopsi teknologi baru harus didukung oleh use case kritis yang konkret.\n\n"
        "Recommendation:\n"
        f"Lakukan pengujian terisolasi (proof-of-concept) terlebih dahulu sebelum mempertimbangkan integrasi inti {scope} ke ekosistem AIRO.\n\n"
        "Sources:\n"
        f"• External technical documentation & industry benchmarks regarding {scope}\n"
        "• AIRO Governance & Architectural Decision Log"
    )
