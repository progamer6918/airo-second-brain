"""Transient MIME decoding and structured facts. Full bodies are never persisted."""

import base64, re
from html.parser import HTMLParser
from .intake_parser import date_in, ZONE


class PlainHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.suppress = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.suppress += 1
        if tag in ("br", "p", "div", "tr", "td", "li"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.suppress = max(0, self.suppress - 1)
        if tag in ("p", "div", "tr", "td", "li"):
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.suppress:
            self.parts.append(data)


def body(message):
    plain = []
    rich = []

    def visit(part):
        if part.get("filename"):
            return
        encoded = part.get("body", {}).get("data")
        if encoded:
            text = base64.urlsafe_b64decode(
                encoded + "=" * ((-len(encoded)) % 4)
            ).decode("utf-8", errors="replace")
            if part.get("mimeType") == "text/plain":
                plain.append(text)
            elif part.get("mimeType") == "text/html":
                h = PlainHTML()
                h.feed(text)
                rich.append("".join(h.parts))
        for child in part.get("parts", []):
            visit(child)

    visit(message.get("payload", {}))
    return "\n".join(plain or rich) or message.get("snippet", "")


def facts(text):
    result = {}
    from datetime import datetime, timezone

    clocks = list(
        re.finditer(
            r"\b([01]?\d|2[0-3])[:.]([0-5]\d)(?::([0-5]\d))?\s*(WIB|WITA|WIT)?\b",
            text,
            re.I,
        )
    )
    candidates = []
    for tm in clocks:
        nearby = text[max(0, tm.start() - 140) : tm.end() + 60]
        explicit = bool(
            re.search(
                r"(?:waktu|tanggal|jam|date|time)\s*(?:transaksi|transaction)|transaction\s*(?:date|time)|pada tanggal",
                nearby,
                re.I,
            )
        )
        date = date_in(nearby)
        # Require an explicit year: never recover a historical bank date with today's year.
        if not re.search(r"\b20\d{2}\b", nearby):
            date = None
        if not date:
            dm = re.search(r"\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b", nearby)
            if dm:
                try:
                    date = (
                        datetime(int(dm[3]), int(dm[2]), int(dm[1])).date().isoformat()
                    )
                except ValueError:
                    pass
        if date and (explicit or len(clocks) == 1):
            offset = {"WIB": "+07:00", "WITA": "+08:00", "WIT": "+09:00"}.get(
                (tm[4] or "WIB").upper(), "+07:00"
            )
            candidates.append(
                (
                    f'{date}T{int(tm[1]):02}:{tm[2]}:{tm[3] or "00"}{offset}',
                    "SECOND" if tm[3] else "MINUTE",
                    explicit or bool(tm[4]),
                )
            )
    distinct = {(x[0], x[1]) for x in candidates}
    if len(distinct) == 1:
        stamp, precision = next(iter(distinct))
        result.update(
            occurred_at=stamp,
            time_precision=precision,
            time_accuracy="CONFIRMED" if all(x[2] for x in candidates) else "ESTIMATED",
            time_source="BANK_RECEIPT",
        )
    elif len(distinct) > 1:
        result["temporal_issue"] = "MULTIPLE_BANK_TIMES"
    ref = re.search(
        r"(?:nomor referensi|no\.? referensi|reference|id transaksi|nomor transaksi)\s*[:\-]?\s*([A-Z0-9\-]{5,50})",
        text,
        re.I,
    )
    if ref:
        result["bank_reference"] = ref[1]
    merchant = re.search(
        r"(?:nama merchant|merchant|nama penerima|penerima|tujuan|transaksi di)\s*[:\-]?\s*([^\n]{3,100})",
        text,
        re.I,
    )
    if merchant:
        result["merchant"] = merchant[1].strip()
        result["note"] = result["merchant"]
    amt = re.search(
        r"(?:nominal transaksi|jumlah transaksi|nominal pembayaran|total pembayaran|total transaksi)\s*[:\-]?\s*(?:rp|idr)\.?\s*([\d.,]+)",
        text,
        re.I,
    )
    if amt:
        try:
            result["amount"] = float(amt[1].replace(".", "").replace(",", "."))
        except ValueError:
            pass
    return result
