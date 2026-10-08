from .temporal import owner_accuracy
"""Extract explicit facts first. Account names never supply purchase categories."""

import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("Asia/Jakarta")
MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "mei": 5,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "agu": 8,
    "aug": 8,
    "sep": 9,
    "okt": 10,
    "oct": 10,
    "nov": 11,
    "des": 12,
    "dec": 12,
}
AMOUNT = re.compile(
    r"(?<![\w:/])(?:rp\.?\s*)?(\d+(?:[.,]\d+)*)\s*(jt|juta|rb|ribu|k)?(?![\w:/])", re.I
)
PATTERNS = [
    (
        r"makan malam|dinner|sate|geprek|gofood|grabfood",
        "Makanan & Minuman",
        "Makan Malam",
    ),
    (r"makan siang|maksi|lunch", "Makanan & Minuman", "Makan Siang"),
    (r"makan|nasgor|mie ayam|bakso", "Makanan & Minuman", None),
    (r"kopi|coffee|cafe", "Makanan & Minuman", "Kopi"),
    (r"jajan|rokok|gorengan", "Makanan & Minuman", "Jajan"),
    (r"servis|service|ganti oli|bengkel", "Transportasi", "Servis Motor"),
    (r"bensin|bbm|pertalite|pertamax", "Transportasi", "BBM"),
    (r"parkir", "Transportasi", "Parkir"),
    (r"barber|salon|potong rambut", "Personal Care", "Barber"),
    (r"pet food|petfood|makanan kucing|makanan hewan", "Pets", "Pet Food"),
    (r"listrik|token pln", "Tagihan & Utilitas", "Listrik"),
    (r"pdam", "Tagihan & Utilitas", "Air/PDAM"),
    (r"wifi|kuota|byu|by.u|internet", "Tagihan & Utilitas", "Internet"),
    (r"iuran sampah", "Tagihan & Utilitas", "Sampah"),
    (r"kpr", "Housing", "KPR Rumah"),
    (r"utang|hutang", "Obligations", "Pembayaran Utang"),
    (r"belanja bulanan|tisu", "Belanja Kebutuhan", "Belanja Bulanan"),
    (r"belanja harian|belanja", "Belanja Kebutuhan", "Belanja Harian"),
    (r"gas|galon|air minum", "Belanja Kebutuhan", "Kebutuhan Pokok"),
    (r"subscribe|subscription|netflix", "Subscriptions", "Digital"),
]


def amount(text):
    text = re.sub(
        r"\b20\d\d-\d\d-\d\d\b|\b\d{1,2}\s+(?:jan\w*|feb\w*|mar\w*|apr\w*|mei|may|jun\w*|jul\w*|agu\w*|aug\w*|sep\w*|okt\w*|oct\w*|nov\w*|des\w*|dec\w*)(?:\s+20\d\d)?|\b\d{1,2}:\d\d(?::\d\d)?\b",
        " ",
        text,
        flags=re.I,
    )
    matches = list(AMOUNT.finditer(text))
    for m in sorted(
        matches,
        key=lambda m: bool(m.group(2) or "rp" in m.group().lower()),
        reverse=True,
    ):
        n = m.group(1)
        suffix = (m.group(2) or "").lower()
        if suffix:
            value = float(n.replace(",", ".")) * (
                1000000 if suffix in ("jt", "juta") else 1000
            )
        else:
            value = float(re.sub(r"[.,](?=\d{3}(?:[.,]|$))", "", n).replace(",", "."))
            if value < 500:
                continue
        return value
    return None


def time_in(text):
    """Return an explicit owner time; colloquial hours have minute precision."""
    lower = text.lower()
    # A dot is a clock separator only after an explicit time word, never in money.
    lower = re.sub(
        r"(\b(?:jam|pukul)\s+(?:(?:jd|jadi|ke)\s+)?)([01]?\d|2[0-3])\.([0-5]\d)(?!\d)",
        r"\1\2:\3",
        lower,
    )
    match = re.search(
        r"\b(?:jam\s+|pukul\s+)?([01]?\d|2[0-3]):([0-5]\d)(?::([0-5]\d))?\b", lower
    )
    if match:
        return (
            int(match[1]),
            int(match[2]),
            int(match[3] or 0),
            "SECOND" if match[3] else "MINUTE",
        )
    match = re.search(
        r"\b(?:jam|pukul)\s+(1[0-2]|[1-9])\s+(pagi|siang|sore|malam)\b", lower
    )
    if not match:
        return None
    hour = int(match[1])
    period = match[2]
    if hour < 12 and (
        period == "sore"
        or (period == "siang" and hour < 7)
        or (period == "malam" and hour >= 6)
    ):
        hour += 12
    elif period in ("pagi", "malam") and hour == 12:
        hour = 0
    return hour, 0, 0, "MINUTE"


def is_context_line(text):
    """Recognize batch instructions and context, not incomplete transaction rows."""
    return bool(
        re.search(
            r"^(?:buat\s+(?:draft|rekap|batch)|tampilkan\b|kalau\b.*(?:detail|tanya|jelas)|"
            r"jangan\s+(?:simpan|catat|eksekusi)\b|(?:semua|seluruh)\s+(?:transaksi|tanggal|jam)\b|"
            r"(?:jam|pukul)\s+(?:tidak diketahui|\d)|penerimaan\s+dari\b.*\badalah\b|"
            r"alokasi\s+anggaran\b|patokan\s+rekap\b)",
            text.strip(),
            re.I,
        )
    )


def date_in(text, now=None):
    now = now or datetime.now(ZONE)
    lower = text.lower()
    if "hari ini" in lower:
        return now.date().isoformat()
    if "kemarin" in lower:
        return (now - timedelta(days=1)).date().isoformat()
    m = re.search(r"\b(20\d\d)-(\d\d)-(\d\d)\b", lower)
    if m:
        try:
            return datetime(*map(int, m.groups())).date().isoformat()
        except ValueError:
            return None
    m = re.search(
        r"\b(\d{1,2})\s+(jan\w*|feb\w*|mar\w*|apr\w*|mei|may|jun\w*|jul\w*|agu\w*|aug\w*|sep\w*|okt\w*|oct\w*|nov\w*|des\w*|dec\w*)(?:\s+(20\d\d))?",
        lower,
    )
    if m:
        try:
            return (
                datetime(int(m[3] or now.year), MONTHS[m[2][:3]], int(m[1]))
                .date()
                .isoformat()
            )
        except ValueError:
            return None
    return None


def account_matches(engine, text):
    out = []
    for a in engine.list_accounts(active_only=True):
        aliases = {
            a.name.lower(),
            *[(x.strip().lower()) for x in (a.aliases or "").split(",") if x.strip()],
        }
        if a.name.lower() == "blu gether":
            aliases.add("gether")
        if a.name.lower() == "blu saving":
            aliases.add("saving")
        if a.name.lower() == "bca utama":
            aliases.add("bca")
        for alias in aliases:
            for m in re.finditer(
                r"(?<!\w)" + re.escape(alias) + r"(?!\w)", text.lower()
            ):
                # A budget purpose after "untuk" is not another ledger account.
                before = text.lower()[: m.start()]
                purpose = list(re.finditer(r"\b(?:utk|untuk)\b", before))
                explicit_source = re.search(r"\b(?:dari|dr|pakai|akun|ke)\s*$", before)
                if purpose and not explicit_source:
                    continue
                out.append((m.start(), m.end(), a))
    out.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    chosen = []
    for m in out:
        if not any(m[0] < v[1] and m[1] > v[0] for v in chosen):
            chosen.append(m)
    return chosen


def classify(engine, note, direction, counterparty=None):
    cat = sub = None
    if direction == "INCOME":
        cat = "Gaji & Pemasukan"
        sub = (
            "Refund"
            if re.search(r"refund|ganti|pengembalian|cashback", note, re.I)
            else (
                "Kontribusi Rumah Tangga"
                if counterparty or re.search(r"kontribusi|rumah tangga", note, re.I)
                else (
                    "Salary"
                    if re.search(r"gaji|uang pulsa|uang makan", note, re.I)
                    else None
                )
            )
        )
    elif direction != "TRANSFER":
        for pat, c, s in PATTERNS:
            if re.search(r"\b(?:" + pat + r")\b", note, re.I):
                cat, sub = c, s
                break
        if not cat:
            found = engine.find_category_by_keyword(note)
            if found:
                cat, sub = found["category_name"], found["subcategory_name"]
    category = next(
        (
            c
            for c in engine.list_categories(active_only=True)
            if c.name.casefold() == (cat or "").casefold()
        ),
        None,
    )
    subcategory = None
    if category and sub:
        subcategory = next(
            (
                s
                for s in engine.list_subcategories(category_id=category.id)
                if s.name.casefold() == sub.casefold()
            ),
            None,
        )
    return {
        "category_id": category.id if category else None,
        "category_name": cat,
        "subcategory_id": subcategory.id if subcategory else None,
        "subcategory_name": sub,
        "proposed_category": cat if cat and not category else None,
        "proposed_subcategory": sub if sub and not subcategory else None,
    }


def parse_line(engine, text, common_date=None, now=None, batch=False):
    now = now or datetime.now(ZONE)
    lower = text.lower()
    matches = account_matches(engine, text)
    acc = matches[0][2] if matches else None
    meaningful = lower
    for start, end, a in reversed(matches):
        meaningful = meaningful[:start] + " " + meaningful[end:]
    transfer = (
        bool(re.search(r"\b(trf|tf|transfer|pindah)\b", meaningful))
        and len(matches) >= 2
        and bool(re.search(r"\bke\b", lower))
    )
    income = bool(
        re.search(r"\b(terima|diterima|masuk|gaji|cashback|refund)\b", meaningful)
    )
    direction = "TRANSFER" if transfer else ("INCOME" if income else "EXPENSE")
    inbound_internal = bool(
        income
        and len(matches) >= 2
        and re.search(r"\b(?:dari|dr)\b", lower[: matches[-1][0]])
    )
    destination = matches[-1][2].id if transfer else None
    if inbound_internal:
        destination = acc.id
        acc = matches[-1][2]
        direction = "TRANSFER"
    funding = (
        matches[-1][2]
        if direction == "EXPENSE"
        and len(matches) >= 2
        and re.search(r"\b(?:dari|dr)\b", lower[: matches[-1][0]])
        else None
    )
    card = next(
        (
            c
            for c in engine.list_credit_cards(active_only=True)
            if c.name.lower() in lower
        ),
        None,
    )
    if card and re.search(r"bayar|pembayaran|tagihan", meaningful):
        direction = "CC_PAYMENT"
    txdate = date_in(lower, now) or common_date
    old = bool(
        re.search(
            r"\b(kemarin|lalu|kemaren|kemarin dulu)\b|\d+\s*(?:x|hari)|\bdr\s+\d+\s+(?:okt|sep)",
            lower,
        )
    )
    occurred = None
    precision = "DATE"
    time_source = None
    tm = time_in(lower)
    if not txdate and not batch and not old:
        txdate = now.date().isoformat()
        occurred = now.isoformat()
        precision = "ESTIMATED"
        time_source = "TELEGRAM_MESSAGE"
    if txdate and tm:
        occurred = f"{txdate}T{tm[0]:02}:{tm[1]:02}:{tm[2]:02}+07:00"
        precision = tm[3]
        time_source = "OWNER"
    counterparty = None
    if income:
        cp = re.search(r"\b(?:dari|dr)\s+([a-z]+)", meaningful)
        if cp:
            counterparty = cp[1]
    from .gmail_reliability import state

    scope = state(engine.db, "intake_owner_context", {}).get(
        "excluded_personal_income_names", []
    )
    outside_scope = any(
        re.search(r"\bgaji\s+" + re.escape(name) + r"\b", lower) for name in scope
    )
    monetary_tokens = re.findall(
        r"(?:rp\.?\s*\d[\d.,]*|\d+(?:[.,]\d+)*\s*(?:rb|ribu|jt|juta|k)\b)", lower
    )
    result = {
        "multiple_amounts": len(monetary_tokens) > 1,
        "amount": amount(text),
        "account_id": acc.id if acc else None,
        "account_name": acc.name if acc else None,
        "direction": direction,
        "date": txdate,
        "message_at": now.isoformat(),
        "occurred_at": occurred,
        "time_precision": precision,
        "time_source": time_source,
        "time_accuracy": "ESTIMATED" if precision == "ESTIMATED" or re.search(r"patokan|perkiraan|samakan|kira.kira", lower) else "CONFIRMED" if occurred else "UNKNOWN",
        "note": meaningful.strip(),
        "counterparty": counterparty,
        "purpose": re.split(r"\b(?:utk|untuk)\b", meaningful)[-1].strip(),
        "credit_card_id": card.id if card and direction == "CC_PAYMENT" else None,
        "destination_account_id": destination,
        "funding_account_id": funding.id if funding else None,
        "funding_account_name": funding.name if funding else None,
        "replacement_pending": bool(
            acc
            and acc.name.lower() == "cash bensin"
            and not re.search(r"\bbensin\b|\bbb[m]?\b", meaningful)
        ),
        "requires_explanation": bool(
            re.search(r"\bganti uang belanja\b|\butang rumah\b", meaningful)
        ),
        "facts_confirmed": False,
        "outside_scope": outside_scope,
        "instruction_hold": bool(
            re.search(r"\b(jangan|rencana|misal|kalau|anggaran)\b", lower)
        ),
    }
    result.update(classify(engine, meaningful, direction, counterparty))
    result["facts_confirmed"] = bool(
        result.get("category_name") and not result.get("instruction_hold")
    )
    result["user_labels_verified"] = bool(
        result["facts_confirmed"]
        and (
            direction == "INCOME"
            or any(
                re.search(r"\b(?:" + pattern + r")\b", meaningful, re.I)
                for pattern, _, _ in PATTERNS
            )
        )
    )
    result["initial_classification"] = {
        k: result.get(k)
        for k in ("category_id", "subcategory_id", "category_name", "subcategory_name")
    }
    return result


def parse_batch(engine, text, now=None):
    requires_preview = bool(
        re.search(
            r"\b(?:draft|rekap|rekapan|jangan|persetujuan)\b|^\s*\d+[.)]",
            text,
            re.I | re.M,
        )
    )
    lines = [
        re.sub(r"^\s*(?:[-•]|\d+[.)])\s*", "", s).strip()
        for s in re.split(r"[\n;]", text)
        if s.strip()
    ]
    expanded = []
    for line in lines:
        parts = re.split(r"\s+dan\s+", line, flags=re.I)
        if len(parts) > 1 and all(
            amount(part) is not None and account_matches(engine, part) for part in parts
        ):
            expanded.extend(parts)
        else:
            expanded.append(line)
    lines = expanded
    entries = []
    common = None
    common_time = None
    for line in lines:
        d = date_in(line, now)
        context = (
            is_context_line(line)
            and amount(line) is None
            and not account_matches(engine, line)
        )
        if context or (amount(line) is None and d):
            if d:
                common = d
            if "jam tidak diketahui" in line.lower():
                common_time = None
            elif time_in(line):
                common_time = time_in(line)
            continue
        if amount(line) is None and re.match(
            r"^(transaksi|rekap|catat|batch)", line, re.I
        ):
            continue
        entry = parse_line(engine, line, common, now, batch=len(lines) > 1)
        entry["requires_preview"] = requires_preview or len(lines) > 1
        if common_time and entry.get("date") and not entry.get("occurred_at"):
            hour, minute, second, precision = common_time
            entry.update(
                occurred_at=f"{entry['date']}T{hour:02}:{minute:02}:{second:02}+07:00",
                time_precision=precision,
                time_source="OWNER",
                time_accuracy=owner_accuracy(text, shared=True),
            )
        entries.append(entry)
    return entries
