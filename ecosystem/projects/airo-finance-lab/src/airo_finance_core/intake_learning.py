"""Explainable owner-confirmed rules and chronological shadow evaluation."""

import hashlib, json, re, time
from .intake_store import dump, uid
from .gmail_reliability import state

GENERIC = {
    "transaksimu pakai blu berhasil",
    "internet transaction journal",
    "info transaksi masuk ke blu kamu",
}


def features(data):
    merchant = (data.get("merchant") or "").lower().strip()
    note = (data.get("note") or "").lower().strip()
    phrase = (
        merchant
        if merchant and merchant not in GENERIC
        else re.sub(r"\b(?:rp\s*)?\d+(?:[.,]\d+)*\s*(?:rb|jt|ribu|juta|k)?\b", "", note)
    )
    phrase = re.sub(
        r"\b(bayar|beli|utk|untuk|ini|itu|adalah|tgl|tanggal)\b", "", phrase
    )
    phrase = " ".join(phrase.split())[:120]
    hour = (data.get("occurred_at") or "")[11:13]
    slot = (
        (
            "LUNCH"
            if 11 <= int(hour) <= 13
            else "DINNER" if 17 <= int(hour) <= 22 else "OTHER"
        )
        if hour.isdigit()
        else None
    )
    return {
        "account_id": data.get("account_id"),
        "direction": data.get("direction"),
        "phrase": phrase,
        "counterparty": data.get("counterparty"),
        "amount": data.get("amount"),
        "time_slot": slot,
    }


def key(data):
    return hashlib.sha256(dump(features(data)).encode()).hexdigest()[:24]


def observe(service, row, data):
    c = service.conn
    now = time.time()
    f = features(data)
    final = {
        k: data.get(k)
        for k in ("category_id", "subcategory_id", "category_name", "subcategory_name")
    }
    c.execute(
        "INSERT INTO intake_observations VALUES (?,?,?,?,?,?)",
        (
            uid(),
            row["id"],
            dump(f),
            dump(row["data"].get("initial_classification", {})),
            (
                dump(final)
                if data.get("facts_confirmed") and data.get("user_labels_verified")
                else None
            ),
            now,
        ),
    )
    if data.get("lines"):
        return
    if (
        not data.get("facts_confirmed")
        or not data.get("user_labels_verified")
        or not f["phrase"]
        or f["phrase"] in GENERIC
        or not final["category_id"]
    ):
        return
    k = key(data)
    old = c.execute("SELECT * FROM intake_rules WHERE rule_key=?", (k,)).fetchone()
    payload = {"features": f, "classification": final, "scope": "EMAIL_SUGGESTION"}
    if old:
        conflict = json.loads(old["payload"])["classification"] != final
        c.execute(
            "UPDATE intake_rules SET confirmations=confirmations+?,conflicts=conflicts+?,enabled=CASE WHEN ? THEN 0 ELSE enabled END,last_at=? WHERE id=?",
            (not conflict, conflict, conflict, now, old["id"]),
        )
    else:
        c.execute(
            "INSERT INTO intake_rules VALUES (?,?,?,?,?,?,?,?,?)",
            (uid(), k, dump(payload), 1, 0, now, now, 0, 0),
        )


def suggest(service, data):
    r = service.conn.execute(
        "SELECT * FROM intake_rules WHERE rule_key=? AND conflicts=0 AND confirmations>=3",
        (key(data),),
    ).fetchone()
    if not r:
        return data
    result = dict(data)
    result.update(json.loads(r["payload"])["classification"])
    result["suggested_rule"] = r["id"]
    return result


def activate(service, rule_id):
    r = service.conn.execute(
        "SELECT * FROM intake_rules WHERE id=?", (rule_id,)
    ).fetchone()
    start = state(service.db, "intake_observation_started", time.time())
    if (
        not r
        or r["conflicts"]
        or r["confirmations"] < 5
        or time.time() - max(start, r["first_at"]) < 7 * 86400
    ):
        raise ValueError(
            "Pola belum lolos: perlu 7 hari pengamatan dan 5 konfirmasi tanpa konflik"
        )
    with service.db.atomic():
        service.conn.execute(
            "UPDATE intake_rules SET owner_approved=1,enabled=1 WHERE id=?", (rule_id,)
        )


def metrics(service):
    rows = service.conn.execute(
        "SELECT prediction,final FROM intake_observations WHERE final IS NOT NULL ORDER BY created_at"
    ).fetchall()
    exact = sum(json.loads(r["prediction"]) == json.loads(r["final"]) for r in rows)
    return {
        "verified_observations": len(rows),
        "exact_predictions": exact,
        "draft_items": service.conn.execute(
            "SELECT COUNT(*) FROM intake_items WHERE status='DRAFT'"
        ).fetchone()[0],
        "corrections": service.conn.execute(
            "SELECT COUNT(*) FROM intake_feedback"
        ).fetchone()[0],
        "questions": service.conn.execute(
            "SELECT COALESCE(SUM(quantity),0) FROM intake_interactions WHERE kind='QUESTION'"
        ).fetchone()[0],
        "clicks": service.conn.execute(
            "SELECT COUNT(*) FROM intake_interactions WHERE kind='CALLBACK'"
        ).fetchone()[0],
        "answers": service.conn.execute(
            "SELECT COUNT(*) FROM intake_interactions WHERE kind='ANSWER'"
        ).fetchone()[0],
        "enabled_email_rules": service.conn.execute(
            "SELECT COUNT(*) FROM intake_rules WHERE enabled=1"
        ).fetchone()[0],
    }


def chronological_evaluation(records):
    """Each record only sees prior labels; never uses future master-data aliases."""
    history = {}
    out = []
    for row in sorted(records, key=lambda r: r["observed_at"]):
        if row.get("status") not in ("ACTIVE", "CORRECTED") or not row.get("verified"):
            continue
        k = row["feature_key"]
        prior = history.get(k, [])
        guess = prior[-1] if prior and len(set(prior)) == 1 else None
        out.append(
            {
                "guessed": guess is not None,
                "correct": guess == row["label"] if guess is not None else None,
            }
        )
        history.setdefault(k, []).append(row["label"])
    return {
        "evaluated": len(out),
        "suggestions": sum(r["guessed"] for r in out),
        "correct": sum(r["correct"] is True for r in out),
    }


def historical_suggestion(engine, data):
    """Suggest from consistent explicit owner notes; generic approvals supply no labels."""
    from .intake_parser import account_matches, classify, date_in

    if data.get("category_id") and data.get("subcategory_id"):
        return data
    if not data.get("account_id") or not data.get("amount"):
        return data
    needle = features(data)["phrase"]
    if not needle or needle in GENERIC:
        return data
    labels = []
    rows = engine.db.get_connection().execute(
        "SELECT t.*,c.name category_name,s.name subcategory_name FROM transactions t JOIN categories c ON c.id=t.category_id LEFT JOIN subcategories s ON s.id=t.subcategory_id WHERE t.account_id=? AND t.direction=? AND t.status IN ('ACTIVE','CORRECTED') AND t.amount BETWEEN ? AND ? AND t.source IN ('MANUAL','TELEGRAM','TELEGRAM_BATCH') AND c.is_active=1 ORDER BY t.created_at DESC LIMIT 150",
        (
            data["account_id"],
            data["direction"],
            data["amount"] * 0.8,
            data["amount"] * 1.2,
        ),
    )
    for row in rows:
        old = dict(row)
        note = (old.get("note") or "").lower()
        if (
            not note
            or note in GENERIC
            or re.search(r"test|canary|smoke|dummy|demo", note)
        ):
            continue
        for start, end, a in reversed(account_matches(engine, note)):
            note = note[:start] + " " + note[end:]
        old["note"] = note
        if features(old)["phrase"] != needle:
            continue
        # Contradictory purpose/category labels are not trusted training examples.
        expected = classify(engine, note, old["direction"])
        if expected.get("category_id") and expected["category_id"] != old.get(
            "category_id"
        ):
            continue
        if expected.get("subcategory_id") and expected["subcategory_id"] != old.get(
            "subcategory_id"
        ):
            continue
        labels.append(
            tuple(
                old.get(k)
                for k in (
                    "category_id",
                    "subcategory_id",
                    "category_name",
                    "subcategory_name",
                )
            )
        )
    if len(labels) < 2 or len(set(labels)) != 1:
        return data
    result = dict(data)
    result.update(
        dict(
            zip(
                ("category_id", "subcategory_id", "category_name", "subcategory_name"),
                labels[0],
            )
        )
    )
    result.update(
        history_suggestion_count=len(labels),
        facts_confirmed=False,
        semantic_review_required=True,
    )
    return result
