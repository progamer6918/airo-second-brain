"""Owner time corrections use persistent previews and the existing Telegram outbox."""

import re
from . import temporal as t
from .gmail_reliability import enqueue, dispatch
from .intake_parser import time_in


def card(parent, owner, proposal, page=0):
    rows = proposal["items"]
    start = page * 12
    part = rows[start : start + 12]
    text = f"🕒 Rekapan perubahan waktu — {proposal['id'][:6]}\nTanggal, nominal, dan saldo tetap.\n"
    for row in part:
        before = row["before"]
        after = row["after"]
        text += f"• {row['entity_id']}: {t.display(before)} → {t.display(after)}\n"
    text += (
        f"Halaman {page+1}/{max(1,(len(rows)+11)//12)}; {len(rows)} catatan tertaut."
    )
    buttons = []
    if proposal["status"] not in ("APPLIED",):
        buttons.append(
            [
                {
                    "text": "✅ Terapkan perubahan waktu",
                    "callback_data": "tm:apply:" + proposal["id"],
                }
            ]
        )
    nav = []
    if page:
        nav.append(
            {"text": "◀️", "callback_data": f"tm:page:{proposal['id']}:{page-1}"}
        )
    if start + 12 < len(rows):
        nav.append(
            {"text": "▶️", "callback_data": f"tm:page:{proposal['id']}:{page+1}"}
        )
    if nav:
        buttons.append(nav)
    with parent.engine.db.atomic():
        enqueue(
            parent.engine.db,
            "time_preview",
            proposal["id"] + ":" + str(page) + ":" + proposal["status"],
            owner,
            "sendMessage",
            {
                "chat_id": str(owner),
                "text": text,
                "reply_markup": {"inline_keyboard": buttons},
            },
        )
    dispatch(parent.engine.db, parent.outbound)


def _handle(parent, update):
    cq = update.get("callback_query")
    msg = update.get("message", {})
    sender = (cq or msg).get("from", {}).get("id")
    if cq and str(cq.get("data", "")).startswith("tm:"):
        if not parent.is_owner(sender):
            return True, "BLOCKED_NON_OWNER_CALLBACK"
        parts = cq["data"].split(":")
        p = t.get_preview(parent.engine.db, parts[2])
        if parts[1] == "apply":
            t.apply(parent.engine.db, p["id"])
            p = t.get_preview(parent.engine.db, p["id"])
            with parent.engine.db.atomic():
                enqueue(
                    parent.engine.db,
                    "time_receipt",
                    p["id"],
                    sender,
                    "sendMessage",
                    {
                        "chat_id": str(sender),
                        "text": f"✅ Waktu {len(p['items'])} catatan diperbarui. Nominal, saldo, dan urutan buku besar tetap.",
                    },
                )
            dispatch(parent.engine.db, parent.outbound)
            return True, "TEMPORAL_APPLIED"
        if parts[1] == "page":
            card(parent, sender, p, int(parts[3]))
            return True, "TEMPORAL_PREVIEW"
    text = msg.get("text", "")
    lower = text.lower()
    if not re.match(
        r"^(?:ubah|koreksi|hapus)\s+(?:jam|waktu)\s+(?:batch|transaksi)\b", lower
    ):
        return None
    if not parent.is_owner(sender):
        return True, "BLOCKED_NON_OWNER_MESSAGE"
    m = re.search(r"\b(batch|transaksi)\s+([a-z0-9_]{6,40})\b", lower)
    if not m:
        parent.outbound.send_message(
            sender,
            "Contoh: ubah jam batch ABC123 jadi 17.30 perkiraan, atau ubah jam transaksi tx_ABC123 jadi 12.05. Tanggal tetap; perubahan ditampilkan sebelum disimpan.",
        )
        return True, "TEMPORAL_NEEDS_REFERENCE"
    c = parent.engine.db.get_connection()
    if m[1] == "batch":
        matches = c.execute(
            "SELECT id FROM intake_batches WHERE id LIKE ? AND owner=?",
            (m[2] + "%", str(sender)),
        ).fetchall()
        ids = (
            [
                r[0]
                for r in c.execute(
                    "SELECT x.transaction_id FROM intake_transactions x JOIN intake_items i ON i.id=x.item_id WHERE i.batch_id=? AND x.role='POSTING'",
                    (matches[0][0],),
                )
            ]
            if len(matches) == 1
            else []
        )
    else:
        matches = c.execute(
            "SELECT id FROM transactions WHERE id LIKE ? AND status!='VOID'",
            (m[2] + "%",),
        ).fetchall()
        ids = [r[0] for r in matches] if len(matches) == 1 else []
    if not ids:
        parent.outbound.send_message(
            sender,
            "Referensi belum ditemukan atau tidak unik. Pakai Ref transaksi atau kode batch dari receipt.",
        )
        return True, "TEMPORAL_NEEDS_REFERENCE"
    unknown = lower.startswith("hapus") or "tidak diketahui" in lower
    clock = time_in(re.sub(r"(?<!\d)(\d{1,2})\.(\d{2})(?!\d)", r"\1:\2", lower))
    if not clock and not unknown:
        parent.outbound.send_message(
            sender, "Isi jam, misalnya 17.30, atau tulis jam tidak diketahui."
        )
        return True, "TEMPORAL_NEEDS_CLOCK"
    changes = []
    for ident in ids:
        row = c.execute("SELECT * FROM transactions WHERE id=?", (ident,)).fetchone()
        d = (
            dict(
                occurred_at=None,
                time_precision="DATE",
                time_accuracy="UNKNOWN",
                time_source=None,
            )
            if unknown
            else dict(
                occurred_at=f"{row['date']}T{clock[0]:02}:{clock[1]:02}:{clock[2]:02}+07:00",
                time_precision=clock[3],
                time_accuracy=(
                    "ESTIMATED"
                    if m[1] == "batch"
                    or re.search(r"perkiraan|patokan|samakan|kira.kira", lower)
                    else "CONFIRMED"
                ),
                time_source="OWNER",
            )
        )
        changes.append(
            dict(id=ident, temporal=d, evidence="OWNER_TELEGRAM_TIME_CORRECTION")
        )
    p = t.preview(parent.engine.db, changes)
    card(parent, sender, p)
    return True, "TEMPORAL_PREVIEW"


def handle(parent, update):
    try:
        return _handle(parent, update)
    except (ValueError, KeyError, IndexError) as exc:
        msg = update.get("message") or update.get("callback_query", {})
        owner = msg.get("from", {}).get("id")
        if parent.is_owner(owner):
            message = (
                str(exc)
                if isinstance(exc, ValueError)
                else "Rekapan waktu belum tersedia; buat rekapan baru."
            )
            with parent.engine.db.atomic():
                enqueue(
                    parent.engine.db,
                    "time_error",
                    str(update.get("update_id")) or str(owner),
                    owner,
                    "sendMessage",
                    {"chat_id": str(owner), "text": "Belum diterapkan: " + message},
                )
            dispatch(parent.engine.db, parent.outbound)
        return True, "TEMPORAL_NEEDS_REVIEW"
