"""
EARESMES Intent Routing Layer — P0
==================================
Classifies incoming owner requests into four P0 intent categories:
  - GREETING: Fast identity / salutation response, no heavy LLM execution.
  - KNOWLEDGE: Direct ASB state & decision retrieval.
  - REASONING: Injects Earesmes identity + ASB context into Hermes reasoning.
  - ACTION: Preserves capability boundary, approval boundary, and task execution.
"""

from enum import Enum
from typing import Tuple, Any


class IntentType(str, Enum):
    GREETING = "GREETING"
    CONVERSATIONAL_COURTESY = "CONVERSATIONAL_COURTESY"
    CASUAL_CONVERSATION = "CASUAL_CONVERSATION"
    DAILY_BRIEFING = "DAILY_BRIEFING"
    KNOWLEDGE_QUERY = "KNOWLEDGE_QUERY"
    DECISION_SUPPORT = "DECISION_SUPPORT"
    PROJECT_CONTINUITY = "PROJECT_CONTINUITY"
    RESEARCH_QUERY = "RESEARCH_QUERY"
    ACTION_REQUEST = "ACTION_REQUEST"
    ACTION = "ACTION"
    KNOWLEDGE = "KNOWLEDGE"
    REASONING = "REASONING"


class PresentationMode(str, Enum):
    CONVERSATIONAL_EXPLANATION = "CONVERSATIONAL_EXPLANATION"
    PARTNER_ASSESSMENT = "PARTNER_ASSESSMENT"
    FORMAL_REPORT = "FORMAL_REPORT"
    GOVERNED_ACTION = "GOVERNED_ACTION"


def resolve_presentation_mode(intent: Any, objective: str) -> PresentationMode:
    """
    Resolve presentation style mode from intent and objective query styling.
    Allowed modes:
      - CONVERSATIONAL_EXPLANATION
      - PARTNER_ASSESSMENT
      - FORMAL_REPORT
      - GOVERNED_ACTION
    """
    q = objective.lower().strip()
    intent_str = intent.value if hasattr(intent, "value") else str(intent)

    # 1. FORMAL_REPORT keywords
    report_keywords = ["laporan", "report", "draft", "dokumen"]
    if any(k in q for k in report_keywords):
        return PresentationMode.FORMAL_REPORT

    # 2. PARTNER_ASSESSMENT keywords
    partner_keywords = ["menurut lo", "menurut kamu", "gimana menurut lo", "menurut airo"]
    if any(k in q for k in partner_keywords):
        return PresentationMode.PARTNER_ASSESSMENT

    # 3. CONVERSATIONAL_EXPLANATION keywords
    explanation_keywords = ["jelasin", "jelaskan", "apa itu", "kenapa", "ceritain"]
    if any(k in q for k in explanation_keywords):
        return PresentationMode.CONVERSATIONAL_EXPLANATION

    # 4. GOVERNED_ACTION based on action intent
    if intent_str in ("ACTION_REQUEST", "ACTION"):
        return PresentationMode.GOVERNED_ACTION

    # 5. Default based on existing intent
    if intent_str == "DECISION_SUPPORT":
        return PresentationMode.PARTNER_ASSESSMENT
    if intent_str in ("DAILY_BRIEFING", "PROJECT_CONTINUITY"):
        return PresentationMode.FORMAL_REPORT
    if intent_str in ("KNOWLEDGE_QUERY", "KNOWLEDGE", "RESEARCH_QUERY", "GREETING", "CONVERSATIONAL_COURTESY", "CASUAL_CONVERSATION", "REASONING"):
        return PresentationMode.CONVERSATIONAL_EXPLANATION

    return PresentationMode.CONVERSATIONAL_EXPLANATION


def format_casual_response(query: str) -> str:
    """Format warm, natural casual and emotional response aligned with SOUL.md."""
    q = query.lower().strip()
    if any(k in q for k in ["capek", "cape", "stress", "pusing", "kesel", "lelah", "penat", "anjir"]):
        return (
            "Wkwk iya Eg, fase begini emang bikin capek 😅\n"
            "Tapi kalau lihat posisi sekarang, AIRO sebenarnya sudah jauh banget dari awal. "
            "Santai dulu sejenak atau ngopi, kalau mau lanjut lagi gue siap standby nemenin."
        )
    if any(k in q for k in ["gimana kabar", "kabar lo", "apa kabar"]):
        return (
            "Kabar baik Eg 😄 Masih standby nemenin AIRO.\n"
            "Gimana di sana, ada hal seru yang mau kita bahas hari ini?"
        )
    if any(k in q for k in ["lagi apa", "lagi ngapain", "ngapain"]):
        return (
            "Lagi standby monitor runtime dan nemenin Eg di Telegram 😄\n"
            "Ada yang mau dilanjutkan atau mau cek sesuatu?"
        )
    if any(k in q for k in ["wkwk", "haha", "hehe", "lol"]):
        return (
            "Wkwk santai Eg 😄\n"
            "Ada yang mau dibahas atau mau lanjut kerjaan?"
        )
    return (
        "Santai Eg 😄 Gue selalu standby nemenin AIRO. "
        "Tinggal panggil aja kalau mau lanjut!"
    )


def classify_intent(query: str) -> IntentType:
    """
    Classify owner message into P0/P1/P2 intent types.
    Strict priority:
      CONVERSATIONAL_COURTESY -> GREETING -> CASUAL_CONVERSATION -> DAILY_BRIEFING -> ...
    """
    q = query.lower().strip()

    # 1. Check CONVERSATIONAL_COURTESY (Social courtesies, acknowledgements)
    courtesy_patterns = [
        "terima kasih", "makasih", "thanks", "thank you", "matur nuwun", "hatur nuhun",
        "sip", "oke", "ok", "paham", "mantap", "siap earesmes"
    ]
    if any(q == cp or q.startswith(cp + " ") or q.endswith(" " + cp) or cp in q for cp in ["terima kasih", "makasih", "thanks", "thank you"]):
        return IntentType.CONVERSATIONAL_COURTESY
    if q in ["sip", "oke", "ok", "paham", "mantap", "siap", "noted"]:
        return IntentType.CONVERSATIONAL_COURTESY

    # Strip salutation prefixes and conversational filler for substantive matching
    salutation_prefixes = [
        "bro ", "cuy ", "gan ", "bang ", "sis ", "halo ", "hai ", "hello ", "hey ", "btw ", "eh "
    ]
    substantive_q = q
    for sp in salutation_prefixes:
        if substantive_q.startswith(sp):
            substantive_q = substantive_q[len(sp):].strip()
            break

    salutation_aliases = ["bro", "cuy", "gan", "bang", "sis"]
    simple_followups = ["gimana", "apa kabar", "kabar", "halo", "hai", "earesmes", "oi", "woy", "yo", ""]

    # Standalone salutation check: pure salutations or simple greetings (e.g. "bro", "bro gimana")
    is_standalone_salutation = q in salutation_aliases or (
        any(q.startswith(s + " ") for s in salutation_aliases) and substantive_q in simple_followups
    )
    if is_standalone_salutation:
        return IntentType.GREETING

    # 2. Check ACTION_REQUEST (P2.2: Controlled bounded actions & proposals)
    action_request_patterns = [
        "buatkan", "siapkan", "jalankan", "cek", "generate", "bantu lakukan",
        "restart", "stop service", "start service", "kill", "deploy",
        "backup", "reboot", "jalankan script", "eksekusi", "mutasi",
        "hapus", "delete", "buat laporan"
    ]
    if any(arp in q or arp in substantive_q for arp in action_request_patterns):
        return IntentType.ACTION_REQUEST

    # 3. Check DAILY_BRIEFING (P1.1)
    briefing_patterns = [
        "update airo", "update earesmes", "status airo", "kondisi airo",
        "briefing", "daily brief", "daily briefing", "briefing airo",
        "laporan harian", "update hari ini", "briefing hari ini"
    ]
    if any(bp in q or bp in substantive_q for bp in briefing_patterns):
        return IntentType.DAILY_BRIEFING

    # 4. Check KNOWLEDGE_QUERY (P1.2: Decision recall, why, explanation, history)
    knowledge_query_patterns = [
        "kenapa", "mengapa", "apa keputusan", "alasan",
        "jelaskan", "jelasin", "ingatkan saya", "bagaimana dulu", "latar belakang"
    ]
    if any(kqp in q or kqp in substantive_q for kqp in knowledge_query_patterns):
        return IntentType.KNOWLEDGE_QUERY

    # 5. Check DECISION_SUPPORT (P1.3: Decision evaluation, recommendations, trade-offs)
    decision_support_patterns = [
        "menurut kamu", "menurut lo", "menurut lu", "menurut mu", "menurutmu",
        "apakah perlu", "apakah kita perlu", "perlu dibuat",
        "sebaiknya", "lebih baik mana", "pilih yang mana", "worth it tidak",
        "apakah sekarang waktu yang tepat", "putuskan untuk saya", "solusi a atau b",
        "antara a dan b", "apakah omnirouter", "perlu omnirouter", "apakah harus",
        "haruskah", "apakah layak", "perlu beralih", "apakah kita harus"
    ]
    if any(dsp in q or dsp in substantive_q for dsp in decision_support_patterns):
        return IntentType.DECISION_SUPPORT

    # 6. Check PROJECT_CONTINUITY (P1.4: Resuming work, checkpoints, handoff)
    continuity_patterns = [
        "lanjutkan", "lanjutkan airo", "lanjutkan pekerjaan terakhir",
        "kita terakhir sampai mana", "posisi terakhir", "resume airo",
        "apa next step", "ringkas supaya chat baru paham", "checkpoint terakhir",
        "lanjutkan sesi", "kondisi terakhir", "terakhir sampai mana",
        "gimana progress", "progress kita", "progres kita", "gimana progres"
    ]
    if any(cp in q or cp in substantive_q for cp in continuity_patterns):
        return IntentType.PROJECT_CONTINUITY

    # 7. Check RESEARCH_QUERY (P2.1: External research, benchmarks, comparisons)
    research_patterns = [
        "riset", "cari tahu", "bandingkan", "benchmark", "review",
        "perkembangan terbaru", "informasi terbaru", "simpan hasil riset",
        "cocok untuk airo", "apakah teknologi", "evaluasi teknologi", "riset teknologi"
    ]
    if any(rp in q or rp in substantive_q for rp in research_patterns):
        return IntentType.RESEARCH_QUERY

    # 8. Check CASUAL_CONVERSATION (Emotional relief, casual greetings, light chats)
    casual_patterns = [
        "capek", "cape", "kesel", "stress", "pusing", "lelah", "penat",
        "gimana kabar", "kabar lo", "lagi apa", "lagi ngapain", "ngapain earesmes",
        "wkwk", "haha", "hehe", "lol", "anjir"
    ]
    if any(cp in q or cp in substantive_q for cp in casual_patterns):
        return IntentType.CASUAL_CONVERSATION

    # 9. Check GREETING / Identity / Standard Salutations
    greeting_exact = [
        "halo", "hai", "hello", "hey", "ping", "tes", "test",
        "halo earesmes", "hai earesmes", "hello earesmes",
        "assalamualaikum", "selamat pagi", "selamat siang", "selamat sore", "selamat malam"
    ]
    identity_patterns = [
        "siapa kamu", "siapa anda", "kamu siapa", "anda siapa",
        "perkenalkan diri", "perkenalkan dirimu", "identitas kamu", "who are you"
    ]
    if q in greeting_exact or substantive_q in greeting_exact or any(q.startswith(g + " ") for g in greeting_exact):
        return IntentType.GREETING
    if any(p in q for p in identity_patterns):
        return IntentType.GREETING

    # 10. Check KNOWLEDGE (ASB, decisions, roadmap)
    knowledge_patterns = [
        "apa progress", "progress airo", "status sekarang",
        "apa tugas berikutnya", "roadmap", "arsitektur asb", "keputusan asb", "decision log", "kcc"
    ]
    if any(kp in q or kp in substantive_q for kp in knowledge_patterns):
        return IntentType.KNOWLEDGE

    # 4. Check REASONING vs general
    reasoning_keywords = [
        "menurut kamu", "analisa", "bagaimana jika", "bagaimana menurutmu",
        "analisis", "evaluasi", "rekomendasi", "pertimbangan", "bandingkan",
        "lanjutkan pekerjaan terakhir", "lanjutkan sesi", "apa langkah selanjutnya"
    ]
    if any(rk in q for rk in reasoning_keywords):
        return IntentType.REASONING

    # Default for conversational / complex inputs: REASONING
    return IntentType.REASONING
