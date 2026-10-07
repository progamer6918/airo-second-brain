"""Persistent intake state; migrations are additive and contain no ledger writes."""

import json
import time
import uuid

SCHEMA = """
CREATE TABLE IF NOT EXISTS intake_batches(id TEXT PRIMARY KEY, owner TEXT NOT NULL,
 source_key TEXT NOT NULL UNIQUE, digest TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'DRAFT',
 created_at REAL NOT NULL, updated_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS intake_items(id TEXT PRIMARY KEY, batch_id TEXT NOT NULL REFERENCES intake_batches(id),
 number INTEGER NOT NULL, data TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'DRAFT',
 UNIQUE(batch_id,number));
CREATE TABLE IF NOT EXISTS intake_transactions(item_id TEXT NOT NULL REFERENCES intake_items(id),
 transaction_id TEXT NOT NULL REFERENCES transactions(id), role TEXT NOT NULL,
 PRIMARY KEY(item_id,transaction_id));
CREATE TABLE IF NOT EXISTS intake_sources(kind TEXT NOT NULL, source_id TEXT NOT NULL,
 item_id TEXT NOT NULL REFERENCES intake_items(id), PRIMARY KEY(kind,source_id));
CREATE TABLE IF NOT EXISTS intake_prompts(owner TEXT NOT NULL,message_id TEXT NOT NULL,batch_id TEXT NOT NULL,
 PRIMARY KEY(owner,message_id));
CREATE TABLE IF NOT EXISTS intake_context(owner TEXT PRIMARY KEY,batch_id TEXT NOT NULL,mode TEXT NOT NULL DEFAULT 'DETAIL');
CREATE TABLE IF NOT EXISTS intake_funding(item_id TEXT NOT NULL,line_number INTEGER NOT NULL,
 transaction_id TEXT NOT NULL REFERENCES transactions(id),amount REAL NOT NULL,PRIMARY KEY(item_id,line_number));
CREATE TABLE IF NOT EXISTS intake_feedback(id TEXT PRIMARY KEY, item_id TEXT NOT NULL,
 field TEXT NOT NULL, old_value TEXT,new_value TEXT,created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS intake_rules(id TEXT PRIMARY KEY, rule_key TEXT NOT NULL UNIQUE,
 payload TEXT NOT NULL, confirmations INTEGER NOT NULL DEFAULT 0, conflicts INTEGER NOT NULL DEFAULT 0,
 first_at REAL NOT NULL,last_at REAL NOT NULL,owner_approved INTEGER NOT NULL DEFAULT 0,enabled INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS intake_replacements(id TEXT PRIMARY KEY,item_id TEXT NOT NULL UNIQUE,
 amount REAL NOT NULL,purpose TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'PENDING',resolved_at REAL);
CREATE TABLE IF NOT EXISTS intake_interactions(id TEXT PRIMARY KEY,batch_id TEXT NOT NULL,
 kind TEXT NOT NULL,quantity INTEGER NOT NULL DEFAULT 1,created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS intake_observations(id TEXT PRIMARY KEY,item_id TEXT,features TEXT NOT NULL,
 prediction TEXT NOT NULL,final TEXT,created_at REAL NOT NULL);
"""


def uid():
    return uuid.uuid4().hex[:20]


def dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def init(db):
    c = db.get_connection()
    c.executescript(SCHEMA)
    for table, name, kind in [
        ("category_aliases", "is_active", "INTEGER NOT NULL DEFAULT 1"),
        ("transactions", "occurred_at", "TEXT"),
        ("transactions", "time_precision", "TEXT DEFAULT 'DATE'"),
        ("transactions", "time_source", "TEXT"),
        ("transactions", "message_at", "TEXT"),
    ]:
        if name not in [r[1] for r in c.execute("PRAGMA table_info(" + table + ")")]:
            c.execute("ALTER TABLE " + table + " ADD COLUMN " + name + " " + kind)
    # Generic notification titles cannot identify a purchase category.
    with c:
        c.execute(
            "UPDATE category_aliases SET is_active=0 WHERE lower(keyword) IN ('transaksimu pakai blu berhasil','info transaksi masuk ke blu kamu','internet transaction journal')"
        )
    from .gmail_reliability import state, put

    if not state(db, "intake_observation_started"):
        with c:
            put(db, "intake_observation_started", time.time())
