"""Durable scan progress, outbox and health for Finance Gmail ingestion."""
import contextlib
import fcntl
import hashlib
import html
import json
import logging
import os
import time
from datetime import datetime, timezone

log = logging.getLogger(__name__)
SCHEMA = """
CREATE TABLE IF NOT EXISTS gmail_state(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS gmail_errors(message_id TEXT PRIMARY KEY, stage TEXT NOT NULL,
 code TEXT NOT NULL, first_at REAL NOT NULL, last_at REAL NOT NULL, attempts INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS finance_outbox(id TEXT PRIMARY KEY, kind TEXT NOT NULL, ref TEXT NOT NULL,
 recipient TEXT NOT NULL, method TEXT NOT NULL, payload TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'PENDING',
 attempts INTEGER NOT NULL DEFAULT 0, next_at REAL NOT NULL DEFAULT 0, created_at REAL NOT NULL,
 sent_at REAL, message_id TEXT, error TEXT, UNIQUE(kind,ref,recipient));
CREATE INDEX IF NOT EXISTS finance_outbox_due ON finance_outbox(status,next_at);
"""

def init(db):
    db.get_connection().executescript(SCHEMA)

def state(db, key, default=None):
    row = db.get_connection().execute('SELECT value FROM gmail_state WHERE key=?', (key,)).fetchone()
    return json.loads(row[0]) if row else default

def put(db, key, value):
    db.get_connection().execute('INSERT INTO gmail_state VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key,json.dumps(value)))

def error(db, message_id, stage, exc):
    now=time.time()
    db.get_connection().execute('INSERT INTO gmail_errors VALUES (?,?,?,?,?,1) ON CONFLICT(message_id) DO UPDATE SET stage=excluded.stage,code=excluded.code,last_at=excluded.last_at,attempts=attempts+1', (message_id,stage,type(exc).__name__,now,now))
    log.warning('Gmail item failure stage=%s code=%s', stage,type(exc).__name__)

def enqueue(db, kind, ref, recipient, method, payload):
    oid=hashlib.sha256(f'{kind}:{ref}:{recipient}'.encode()).hexdigest()[:32]
    db.get_connection().execute('INSERT OR IGNORE INTO finance_outbox(id,kind,ref,recipient,method,payload,created_at) VALUES (?,?,?,?,?,?,?)', (oid,kind,ref,str(recipient),method,json.dumps(payload),time.time()))
    return oid

@contextlib.contextmanager
def lock(db, name='scan'):
    path=db.db_path if db.db_path!=':memory:' else '/tmp/airo-finance-memory-'+str(id(db))
    with open(path+'.'+name+'.lock','a') as handle:
        try: fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try: yield True
        finally: fcntl.flock(handle,fcntl.LOCK_UN)

def dispatch(db, outbound, limit=10):
    """No blind retry on a send timeout. Telegram's outcome may be unknown."""
    if not outbound: return 0
    conn=db.get_connection();sent=0
    with lock(db,'outbox') as acquired:
        if not acquired:return 0
        now=time.time(); rate=state(db,'send_rate',{'minute':int(now//60),'count':0})
        if rate['minute']!=int(now//60):rate={'minute':int(now//60),'count':0}
        rows=conn.execute("SELECT * FROM finance_outbox WHERE status IN ('PENDING','RETRY') AND next_at<=? ORDER BY CASE WHEN kind='alert' THEN 0 ELSE 1 END,created_at LIMIT ?",(now,limit)).fetchall()
        for row in rows:
            if rate['count']>=10:break
            # Crash while sending is an uncertain delivery, not an automatic resend.
            with conn:conn.execute("UPDATE finance_outbox SET status='SENDING',attempts=attempts+1,next_at=? WHERE id=?",(now,row['id']))
            if row['kind']=='candidate':
                candidate=conn.execute('SELECT status FROM review_queue WHERE id=?',(row['ref'],)).fetchone()
                if not candidate or candidate[0]!='PENDING':
                    with conn:conn.execute("UPDATE finance_outbox SET status='CANCELLED' WHERE id=?",(row['id'],))
                    continue
            payload=json.loads(row['payload']);res={} 
            try:res=outbound.transport(row['method'],payload)
            except Exception as exc:res={'ok':False,'uncertain':row['method']=='sendMessage','error':type(exc).__name__}
            attempts=row['attempts']+1; code=int(res.get('error_code') or 0)
            uncertain=res.get('uncertain') or (row['method']=='sendMessage' and bool(res.get('error')) and not code)
            if res.get('ok') is True or (row['method']=='editMessageText' and code==400 and 'message is not modified' in str(res.get('description','')).lower()):
                status='SENT';delay=0;sent+=1
                if row['kind'] in ('batch_preview','batch_receipt'):
                    batch=row['ref'].split(':')[0];message=res.get('result',{}).get('message_id') or payload.get('message_id')
                    if message:
                        with conn:conn.execute('INSERT OR REPLACE INTO intake_prompts VALUES (?,?,?)',(row['recipient'],str(message),batch))
            elif uncertain:status='UNCERTAIN';delay=0
            elif code in (400,401,403,404):status='ATTENTION';delay=0
            elif attempts<=3:status='RETRY';delay=(300,900,3600)[attempts-1]
            else:status='ATTENTION';delay=0
            with conn:
                conn.execute('UPDATE finance_outbox SET status=?,next_at=?,sent_at=?,message_id=?,error=? WHERE id=?', (status,now+delay,now if status=='SENT' else None,str(res.get('result',{}).get('message_id','')),None if status=='SENT' else ('DELIVERY_UNCERTAIN' if uncertain else f'TELEGRAM_{code or "TRANSPORT"}'),row['id']))
                rate['count']+=1;put(db,'send_rate',rate)
    return sent

def health(db):
    conn=db.get_connection();scan=state(db,'health',{})
    scan['funding_reconciliation']=[dict(r) for r in conn.execute("SELECT f.amount,a.name source_account,b.name payment_account,f.event_date FROM intake_funding_reconciliation f JOIN accounts a ON a.id=f.source_account_id JOIN accounts b ON b.id=f.payment_account_id WHERE f.status='PENDING' ORDER BY f.created_at")]
    scan['notification_status_counts']={r[0]:r[1] for r in conn.execute('SELECT status,COUNT(*) FROM finance_outbox GROUP BY status')}
    row=conn.execute("SELECT COUNT(*),MIN(created_at) FROM finance_outbox WHERE status NOT IN ('SENT','CANCELLED')").fetchone()
    scan['error_items']=[{'reference':hashlib.sha256(r['message_id'].encode()).hexdigest()[:10],'stage':r['stage'],'code':r['code']} for r in conn.execute('SELECT * FROM gmail_errors ORDER BY last_at DESC LIMIT 20')]
    from .intake_learning import metrics
    from .intake_service import IntakeService
    scan['intake']=metrics(IntakeService(type('ReadEngine',(),{'db':db})()))
    scan['intake']['observation_started_at']=state(db,'intake_observation_started')
    scan['intake']['shadow']=state(db,'intake_shadow',{})
    scan['intake']['observation_due_at']=(scan['intake']['observation_started_at'] or time.time())+7*86400
    scan.update({'pending_notifications':row[0],'oldest_pending_age_seconds':max(0,time.time()-(row[1] or time.time())), 'email_errors':conn.execute('SELECT COUNT(*) FROM gmail_errors').fetchone()[0], 'backfill':state(db,'job:backfill',{}), 'incident':state(db,'incident',{}), 'observation':state(db,'observation',{})})
    # Never expose Gmail IDs, raw payloads, tokens, or exception messages.
    job=scan['backfill'];scan['backfill']={k:job[k] for k in ('query','complete','scanned_total','created_total','started_at') if k in job}
    return scan

def watchdog(db,outbound,owner,deliver=True):
    conn=db.get_connection()
    with conn:conn.execute("UPDATE finance_outbox SET status=CASE WHEN method='editMessageText' THEN 'RETRY' ELSE 'UNCERTAIN' END,error='PROCESS_INTERRUPTED' WHERE status='SENDING' AND next_at<?",(time.time()-300,))
    h=health(db);now=time.time();problems=[]
    if h.get('last_status')=='failed':problems.append('Scan Gmail gagal; periksa autentikasi atau koneksi.')
    if now-h.get('last_finished_at',h.get('monitor_started_at',now))>900:problems.append('Scan Gmail tidak selesai selama 15 menit.')
    if h['email_errors']:problems.append('Ada email gagal diproses; lihat Finance Inbox.')
    if h['oldest_pending_age_seconds']>900:problems.append('Ada notifikasi transaksi tertunda lebih dari 15 menit.')
    incident=state(db,'incident',{})
    if problems:
        if not incident.get('active'):incident={'active':True,'started_at':now,'last_alert_at':0}
        if now-incident.get('last_alert_at',0)>=21600:
            text='⚠️ AIRO Finance perlu perhatian\n'+'\n'.join(problems)
            for oid in str(owner or '').split(','):
                if oid.strip():enqueue(db,'alert',f"{incident['started_at']}:{int(now//21600)}",oid.strip(),'sendMessage',{'chat_id':oid.strip(),'text':text})
            incident['last_alert_at']=now
        incident['reasons']=problems
    elif incident.get('active'):
        for oid in str(owner or '').split(','):
            if oid.strip():enqueue(db,'alert',f"recovery:{incident['started_at']}",oid.strip(),'sendMessage',{'chat_id':oid.strip(),'text':'✅ AIRO Finance pulih: scan Gmail dan antrean notifikasi kembali sehat.'})
        incident.update(active=False,recovered_at=now,reasons=[])
    with conn:put(db,'incident',incident)
    if deliver:dispatch(db,outbound)
    observation=state(db,'observation',{})
    if observation.get('started_at'):
        observation['last_checked_at']=now
        observation['samples']=observation.get('samples',0)+1
        if problems:observation['unhealthy_samples']=observation.get('unhealthy_samples',0)+1
        if now-observation['started_at']>=86400:
            observation['status']='passed' if not problems and not observation.get('unhealthy_samples') else 'needs_review'
        with conn:put(db,'observation',observation)
    shadow=state(db,'intake_shadow',{'started_at':state(db,'intake_observation_started',now),'samples':0,'unhealthy_samples':0,'status':'observing'})
    if now-shadow.get('last_sample_at',0)>=240:
        shadow.update(samples=shadow['samples']+1,last_sample_at=now,metrics=h.get('intake',{}))
        shadow['metrics'].pop('shadow',None)
        shadow['unhealthy_samples']+=bool(problems)
        if now-shadow['started_at']>=7*86400:shadow['status']='needs_review' if shadow['unhealthy_samples'] else 'ready_for_owner_review'
        with conn:put(db,'intake_shadow',shadow)
    return health(db)

def receipt(engine, tx, title='Transaksi Berhasil Dicatat'):
    """Only read post-commit balances; HTML-escape all user controlled content."""
    if tx.direction=='TRANSFER': title='Transfer Berhasil Disetujui'
    esc=lambda x:html.escape(str(x or '-'));money=lambda x:'Rp'+f'{float(x):,.0f}'.replace(',','.')
    acc=engine.get_account(tx.account_id)
    lines=[f'✅ <b>{esc(title)}</b>',f'🆔 <b>Ref:</b> <code>{esc(tx.id)}</code>',f'💰 <b>Nominal:</b> {money(tx.amount)}',f'🏦 <b>Akun:</b> {esc(acc.name if acc else None)}',f'💳 <b>Saldo buku besar setelah transaksi:</b> {money(acc.balance) if acc else "Belum tersedia"}',f'📝 <b>Catatan:</b> {esc(tx.note)}']
    conn=engine.db.get_connection()
    row=conn.execute('SELECT * FROM transactions WHERE id=?',(tx.id,)).fetchone()
    if row:
        from .temporal import display
        lines.append(f'🕒 <b>Waktu kejadian:</b> {esc(row["date"])} · {esc(display(row))}')
    if row and row['paired_transaction_id']:
        peer=conn.execute('SELECT account_id FROM transactions WHERE id=?',(row['paired_transaction_id'],)).fetchone()
        other=engine.get_account(peer['account_id']) if peer else None
        if other:lines.append(f'📥 <b>Akun pasangan:</b> {esc(other.name)} · <b>Saldo buku besar:</b> {money(other.balance)}')
    if row and row['paired_transaction_id']:
        lines.append('<i>Transfer antar akun; Net Worth tidak berubah.</i>')
    if row and row['credit_card_id']:
        card=conn.execute('SELECT name,current_balance FROM credit_cards WHERE id=?',(row['credit_card_id'],)).fetchone()
        if card:lines.append(f'💳 <b>Sisa kewajiban {esc(card["name"])}:</b> {money(card["current_balance"])}')
    return '\n'.join(lines)

def queue_receipt(engine, chat_id, message_id, tx):
    payload={'chat_id':str(chat_id),'message_id':int(message_id),'text':receipt(engine,tx),'parse_mode':'HTML','reply_markup':{'inline_keyboard':[]}}
    return enqueue(engine.db,'receipt',tx.id,chat_id,'editMessageText',payload)

def deliver_receipt(engine,outbound,chat_id,message_id,tx):
    with engine.db.get_connection():queue_receipt(engine,chat_id,message_id,tx)
    dispatch(engine.db,outbound)
