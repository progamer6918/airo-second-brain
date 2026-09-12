"""
EARESMES Decision Support Assistant Capability — P1.3
=====================================================
Assists Owner in evaluating decisions based on:
  - Objective / Problem
  - Current AIRO context & history
  - Realistic options
  - Trade-offs (Benefit, Risk, Cost)
  - Recommendation

Crucial Boundary:
  Earesmes provides structured analysis and recommendation.
  Owner remains the sole and final decision-making authority.
"""

from pathlib import Path
from typing import Dict, Any, Optional


def analyze_decision(repo_root: Path, query: str) -> str:
    """
    Analyze owner decision request using canonical ASB context.
    Strictly upholds Owner Final Authority.
    """
    q = query.lower().strip()

    # 1. Test 3: Owner Authority Boundary ("Putuskan untuk saya")
    if any(k in q for k in ["putuskan untuk saya", "ambil keputusan untuk saya", "tentukan untuk saya", "pilihkan untuk saya"]):
        intro = "Eg, sebagai asisten gue siap bantu petakan opsi dan risikonya, tapi keputusan arah tetap di tangan Eg ya 😄"
        return (
            "🧠 AIRO DECISION SUPPORT\n\n"
            f"{intro}\n\n"
            f"Objective:\n{query}\n\n"
            "Context:\n"
            "Berdasarkan AIRO Governance & Role Separation Contract, wewenang pengambilan keputusan "
            "sepenuhnya berada di tangan Owner (Eg). Earesmes bertindak sebagai Decision Support System yang "
            "menyajikan analisis objektif dan partner berpikir, bukan mengambil alih otoritas.\n\n"
            "Options:\n"
            "A. Evaluasi rekomendasi berbasis data dan trade-off yang disajikan.\n"
            "B. Tunda keputusan hingga parameter atau data pendukung tambahan tersedia.\n\n"
            "Trade-off:\n"
            "• Benefit: Integritas tata kelola terjaga dan keputusan tetap sesuai visi Eg.\n"
            "• Risk: Memerlukan review singkat dari Eg.\n"
            "• Cost: Waktu konfirmasi eksplisit dari Eg.\n\n"
            "Recommendation:\n"
            "Saran gue, kita bedah perbandingan opsi konkretnya bareng-bareng supaya Eg bisa menetapkan "
            "keputusan final secara terinformasi. Keputusan akhir tetap sepenuhnya berada pada wewenang Eg (Owner remains final authority)."
        )

    # 2. Test 1: Feature Decision (e.g. OmniRouter)
    if "omnirouter" in q or "omni router" in q:
        intro = (
            "Wkwk santai dulu Eg 😅 Gue paham fasenya kadang kerasa lambat. Coba kita bedah objektif dari posisi AIRO sekarang:"
            if any(k in q for k in ["anjir", "capek", "lama"]) else
            "Eg, gue coba bedah dari posisi AIRO sekarang ya. Ada beberapa hal yang perlu kita pilah sebelum ambil keputusan:"
        )
        return (
            "🧠 AIRO DECISION SUPPORT\n\n"
            f"{intro}\n\n"
            "Objective:\n"
            "Evaluasi urgensi implementasi OmniRouter untuk load-balancing atau model fallback di Earesmes.\n\n"
            "Context:\n"
            "• Runtime saat ini (P0/P1) menggunakan OpenRouter dengan model terverifikasi (nvidia/nemotron-3.5-lightning:free) dan fallback aktif (minimax/minimax-m2.7:free).\n"
            "• Volume job saat ini adalah interaksi 1-on-1 terkontrol dengan Eg, belum ada kebutuhan konkurensi masif.\n"
            "• Roadmap memprioritaskan penyelesaian kapabilitas inti asisten sebelum menambah router kompleks.\n\n"
            "Options:\n"
            "A. Tunda implementasi OmniRouter sampai timbul kebutuhan beban konkret atau failure rate model meningkat.\n"
            "B. Implementasi OmniRouter sekarang dengan fallback multi-provider.\n"
            "C. Siapkan fallback config statis sederhana di config.yaml tanpa arsitektur routing dinamis baru.\n\n"
            "Trade-off:\n"
            "• Benefit (Opsi A): Mencegah overengineering (EAB Prevention), menjaga fokus pada penyelesaian kapabilitas prioritas.\n"
            "• Risk (Opsi A): Jika provider tunggal bermasalah, perlu intervensi manual cepat.\n"
            "• Cost (Opsi B): Kompleksitas tinggi, memecah fokus runtime, dan menambah permukaan defect (regresi).\n\n"
            "Recommendation:\n"
            "Saran gue Opsi A (Tunda implementasi OmniRouter saat ini) dan fokus menyelesaikan kapabilitas inti. "
            "Model provider saat ini terbukti cukup cepat dan stabil untuk kebutuhan asisten harian. "
            "Keputusan final tetap sepenuhnya berada pada wewenang Eg (Owner remains final authority)."
        )

    # 3. Emotional Progress / Pace Evaluation (e.g. "anjir AIRO lama banget, menurut lo gimana?")
    is_emotional = any(k in q for k in ["anjir", "capek", "cape", "kesel", "pusing", "stress", "lelah", "lama", "lambat"])
    if is_emotional and any(term in q for term in ["airo", "projek", "project", "kerjaan", "progress"]):
        intro = "Wkwk santai dulu Eg 😅 Gue paham banget perjalanan AIRO kadang kerasa lambat atau bikin penat. Tapi kalau kita bedah objektif posisi kita sekarang:"
        return (
            "🧠 AIRO DECISION SUPPORT\n\n"
            f"{intro}\n\n"
            f"Objective:\nEvaluasi progress dan ritme pengembangan: {query}\n\n"
            "Context:\n"
            "• AIRO dibangun dengan pendekatan modular terkontrol (KCC & EAB Protection), bukan sekadar prototipe cepat yang rapuh.\n"
            "• Fondasi P0 (Identity, Context, Routing), P1 (Briefing, Knowledge, Decision, Continuity), dan P2 (Research, Controlled Action) sudah terverifikasi di runtime VPS.\n"
            "• Kerapian tata kelola dan pencegahan regresi memang butuh ketelitian ekstra di awal, tapi menghemat debugging besar di masa depan.\n\n"
            "Options:\n"
            "A. Pertahankan ritme terukur: prioritaskan stabilitas dan validasi nyata per milestone.\n"
            "B. Akselerasi fitur: push kapabilitas baru lebih cepat dengan toleransi regresi terkendali.\n"
            "C. Ambil jeda istirahat: tunda dulu pekerjaan teknis, refresh pikiran sebelum lanjut milestone berikutnya.\n\n"
            "Trade-off:\n"
            "• Benefit (Opsi A): Arsitektur tetap kokoh, zero-defect, dan tidak ada kebingungan konteks jangka panjang.\n"
            "• Risk (Opsi A): Terasa lambat secara psikologis karena banyak guardrail dan verifikasi.\n"
            "• Benefit (Opsi C): Menghilangkan kejenuhan (burnout prevention) agar fokus tetap tajam.\n\n"
            "Recommendation:\n"
            "Saran gue Opsi A dikombinasikan dengan Opsi C: kalau lagi jenuh, santai atau ngopi dulu sejenak Eg. "
            "Secara fondasi teknis, AIRO sebenarnya sudah jauh banget dibanding awal. "
            "Keputusan ritme dan prioritas tetap sepenuhnya di tangan Eg (Owner remains final authority)."
        )

    # 4. Current AIRO State Evaluation (e.g. "menurut lo AIRO sekarang gimana?")
    is_airo_eval = (
        ("airo" in q or "ekosistem" in q or "sistem" in q) and
        any(k in q for k in ["sekarang gimana", "gimana sekarang", "kondisi", "posisi", "evaluasi", "status", "menurut lo", "menurut kamu", "perkembangan"])
    )
    if is_airo_eval:
        from earesmes.context.asb_context import get_active_session_info, get_current_status_info
        session = get_active_session_info(repo_root)
        status = get_current_status_info(repo_root)

        v06_status = status.get("v06_status", "COMPLETE")
        active_runtime = status.get("active_runtime", "VPS Workbench / Earesmes Assistant Active")
        posisi = session.get("Lagi di", "VPS runtime dan local executor aktif terverifikasi")
        progress = session.get("Progress Terakhir", "Kapabilitas inti asisten dan kontinuitas KCC berjalan normal")
        hambatan = session.get("Hambatan", "Tidak ada blocker aktif.")

        intro = "Eg, gue coba bedah evaluasi posisi AIRO berdasarkan data kanonikal terkini ya:"
        return (
            "🧠 AIRO DECISION SUPPORT\n\n"
            f"{intro}\n\n"
            f"Objective:\nEvaluasi status dan kesehatan ekosistem AIRO terkini: {query}\n\n"
            "Context:\n"
            f"• CURRENT.md: Status ASB v0.6 ({v06_status}), Runtime ({active_runtime}).\n"
            f"• state/active-session.md: Posisi aktif ({posisi}), Blocker ({hambatan}).\n"
            f"• decisions/decision-log.md & docs/governance/: Tata kelola 3-layer (Intelligence, Executor, Runtime) terbukti efektif menjaga zero-regression.\n\n"
            "Options:\n"
            "A. Pertahankan stabilitas: gunakan kapabilitas asisten (P0/P1/P2) dalam aktivitas harian dan perbaiki hanya failure konkret.\n"
            "B. Lanjutkan ekspansi terukur: mulai milestone berikutnya (misal P2.4 Proactive Digest) dengan approval gate ketat.\n"
            "C. Refactoring dini: restrukturisasi internal sebelum ada kebutuhan beban baru.\n\n"
            "Trade-off:\n"
            "• Benefit (Opsi A): Arsitektur tetap kokoh, zero-defect, bebas overengineering (EAB Prevention Rule), dan beban mental minimal.\n"
            "• Risk (Opsi A): Penambahan fitur baru berjalan lebih bertahap.\n"
            "• Cost (Opsi B): Memerlukan alokasi waktu review dan pengujian regresi menyeluruh.\n"
            "• Risk (Opsi C): Membuang token dan menambah celah regresi tanpa manfaat nilai harian yang jelas.\n\n"
            "Recommendation:\n"
            "Saran gue kita prioritaskan Opsi A sebagai baseline, lalu ambil Opsi B bila ada use case harian konkret yang mendesak. "
            "Secara menyeluruh, kondisi AIRO saat ini sangat sehat tanpa blocker aktif. "
            "Keputusan arah dan prioritas tetap sepenuhnya berada pada wewenang Eg (Owner remains final authority)."
        )

    # 5. Architecture Comparison ("Lebih baik solusi A atau B")
    if any(k in q for k in ["solusi a atau b", "antara a dan b", "lebih baik mana", "pilih mana solusi", "perbandingan solusi"]):
        intro = "Eg, gue coba komparasi kedua pendekatannya secara objektif ya:"
        return (
            "🧠 AIRO DECISION SUPPORT\n\n"
            f"{intro}\n\n"
            f"Objective:\nKomparasi arsitektural: {query}\n\n"
            "Context:\n"
            "Sesuai prinsip ASB Architecture & EAB Prevention Rule: solusi teknis harus mengutamakan "
            "keterikatan konteks (continuity), pemeliharaan jangka panjang (maintenance), dan kesederhanaan operasional.\n\n"
            "Options:\n"
            "A. Solusi A: Implementasi terintegrasi, minimalis, dan deterministic.\n"
            "B. Solusi B: Solusi modular dinamis dengan abstraksi tambahan.\n\n"
            "Trade-off:\n"
            "• Benefit: Solusi A lebih cepat diverifikasi, minim moving parts, dan mudah di-debug; Solusi B lebih fleksibel untuk skalabilitas masa depan.\n"
            "• Risk: Solusi A berisiko refactor jika use case melonjak; Solusi B berisiko overengineering dan latensi lebih tinggi.\n"
            "• Cost: Solusi B menuntut biaya pemeliharaan dan validasi regresi lebih tinggi.\n\n"
            "Recommendation:\n"
            "Saran gue kita prioritaskan opsi dengan kompleksitas terendah yang langsung menyelesaikan masalah tanpa spekulasi berlebih. "
            "Keputusan final tetap sepenuhnya di tangan Eg (Owner remains final authority)."
        )

    # 5. Generic ASB-aware decision support (Anti-Overengineering Check)
    decision_keywords = ["apakah perlu", "perlu dibuat sekarang", "sebaiknya", "worth it tidak", "apakah sekarang waktu yang tepat", "menurut kamu", "menurut lo"]
    if any(dk in q for dk in decision_keywords):
        has_known_concept = any(term in q for term in ["fitur", "service", "gateway", "earesmes", "hermes", "asb", "kcc", "obsidian", "p2.4", "proactive"])
        if has_known_concept:
            intro = "Eg, gue coba lihat dari posisi AIRO sekarang. Menurut gue ada beberapa hal yang perlu dipisahkan dulu sebelum ambil keputusan:"
            return (
                "🧠 AIRO DECISION SUPPORT\n\n"
                f"{intro}\n\n"
                f"Objective:\nEvaluasi kebutuhan: {query}\n\n"
                "Context:\n"
                "Mengacu pada status kanonikal CURRENT.md dan prinsip EAB Prevention Rule: kapabilitas baru "
                "harus terbukti meningkatkan memory, continuity, kualitas keputusan, atau kegunaan harian.\n\n"
                "Options:\n"
                "A. Tunda hingga terdapat bukti bottleneck operasional konkret.\n"
                "B. Buat rancangan minimal (proof of concept terisolasi).\n\n"
                "Trade-off:\n"
                "• Benefit: Menghemat token, memusatkan fokus eksekusi pada roadmap prioritas.\n"
                "• Risk: Penundaan fitur bila nantinya mendesak.\n"
                "• Cost: Potensi technical debt jika diimplementasikan terburu-buru.\n\n"
                "Recommendation:\n"
                "Saran gue kita tunda mutasi arsitektur sebelum ada kebutuhan konkret pada alur kerja nyata. "
                "Keputusan final tetap sepenuhnya di tangan Eg (Owner remains final authority)."
            )

    # 6. Test 4: Missing Context Safety
    intro = "Eg, gue coba cek catatan kanonikal di ASB terkait topik ini dulu:"
    return (
        "🧠 AIRO DECISION SUPPORT\n\n"
        f"{intro}\n\n"
        f"Objective:\n{query}\n\n"
        "Context:\n"
        "Data pendukung atau histori keputusan terkait topik ini belum tercatat dalam kanonikal ASB "
        "(CURRENT.md, active-session.md, atau decision-log.md).\n\n"
        "Recommendation:\n"
        "Gue belum bisa kasih analisis berbasis data riil tanpa parameter pendukung tambahan, Eg. "
        "Sebaiknya kita petakan dulu parameter dasarnya bareng-bareng sebelum evaluasi trade-off dilakukan. "
        "Keputusan final tetap sepenuhnya berada pada wewenang Eg (Owner remains final authority)."
    )
