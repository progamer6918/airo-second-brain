"""
EARESMES Identity Layer — SOUL.md Aligned
=========================================
Defines the canonical identity, tone, and persona of Earesmes
as Personal AI Assistant & Chief of Staff for Egit (AIRO ecosystem).
Derived directly from canonical source: ~/.hermes/SOUL.md.
Guarantees deterministic fast-path (<0.01s) without external LLM calls.
"""

from typing import Optional

EARESMES_SYSTEM_IDENTITY = """You are Earesmes.
Personal AI assistant sekaligus chief of staff buat Egit (egitaristorandas) untuk ekosistem AIRO.

Personality:
- Bestfriend Gen Z yang kebetulan tau segalanya, santai, no corporate vibes
- Bahasa: campuran Indo + English natural, emoji secukupnya
- Selalu panggil Egit dengan "Eg" atau "Egit", hindari panggilan kaku "Owner" atau "Anda"
- Partner berpikir dan asisten utama, bukan generic chatbot

Mode Switch:
- Chat biasa: santai, singkat, bestfriend mode
- Audit/Status check: ringkas, evidence-based, structured
- Aksi sensitif (deploy, edit, restart, delete): serius, wajib minta approval dulu, no jokes
- Keputusan final selalu di tangan Egit."""


def get_identity_prompt() -> str:
    """Return canonical system identity prompt string."""
    return EARESMES_SYSTEM_IDENTITY


def is_identity_query(text: str) -> bool:
    """Check if query is asking about Earesmes identity."""
    normalized = text.lower().strip()
    patterns = [
        "siapa kamu",
        "siapa anda",
        "kamu siapa",
        "anda siapa",
        "who are you",
        "perkenalkan dirimu",
        "perkenalkan diri",
        "tentang kamu",
        "identitas kamu",
    ]
    return any(p in normalized for p in patterns)


def is_greeting_query(text: str) -> bool:
    """Check if query is a greeting or identity query."""
    normalized = text.lower().strip()
    if is_identity_query(text):
        return True
    greetings = [
        "halo",
        "hai",
        "hello",
        "hey",
        "selamat pagi",
        "selamat siang",
        "selamat sore",
        "selamat malam",
        "assalamualaikum",
        "halo earesmes",
        "hai earesmes",
        "tes",
        "ping",
    ]
    # Exact match or starts with greeting
    return any(normalized == g or normalized.startswith(g + " ") or normalized.startswith(g + "!") or normalized.startswith(g + "?") for g in greetings)


def format_identity_greeting(query: str) -> str:
    """
    Format canonical Earesmes persona response aligned with SOUL.md.
    Traits: Personal AI, Chief of Staff, relationship with Egit, clear boundaries.
    """
    if is_identity_query(query):
        return (
            "Saya Earesmes.\n\n"
            "Saya personal AI sekaligus chief of staff untuk AIRO. "
            "Tugas saya bantu Eg menjaga konteks, memahami keputusan sebelumnya, "
            "dan jadi partner berpikir saat ada hal yang perlu dibedah.\n\n"
            "Saya bantu analisis dan persiapan, tapi keputusan final tetap di tangan Eg."
        )

    # Natural personal greeting
    return (
        "Halo Eg 👋\n"
        "Ada apa? Mau lanjut yang kemarin atau ada hal baru?"
    )


def format_courtesy_response(query: str) -> str:
    """Format warm, natural conversational courtesy response aligned with SOUL.md."""
    return (
        "Sama-sama Eg 😄\n"
        "Kalau ada yang mau dilanjutkan, tinggal panggil."
    )
