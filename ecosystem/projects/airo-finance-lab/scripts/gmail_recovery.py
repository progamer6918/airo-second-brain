#!/usr/bin/env python3
"""Scanner/watchdog runner: only logs counts, never email bodies or credentials."""
import argparse,json,os,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from airo_finance_core import DatabaseManager,FinanceCoreEngine,GmailIntelligenceService
from airo_finance_core import gmail_reliability as rel
p=argparse.ArgumentParser();p.add_argument('mode',choices=['scan','dry-run','backfill','watchdog','reconcile','outbox']);p.add_argument('--db-path',default=str(Path(__file__).resolve().parents[1]/'data/airo_finance.db'));a=p.parse_args()
db=DatabaseManager(a.db_path);db.init_schema();engine=FinanceCoreEngine(db);svc=GmailIntelligenceService(engine);outbound,owner=svc.get_outbound()
try:
 if a.mode=='watchdog':result=rel.watchdog(db,outbound,owner)
 elif a.mode=='outbox':result={'notifications_sent':rel.dispatch(db,outbound)}
 elif a.mode=='reconcile':
  conn=db.get_connection();count=0
  with db.atomic():
   for row in conn.execute("SELECT p.review_item_id,q.parsed_result FROM processed_emails p JOIN review_queue q ON q.id=p.review_item_id WHERE q.status='PENDING'").fetchall():
    if conn.execute("SELECT 1 FROM finance_outbox WHERE kind='candidate' AND ref=?",(row[0],)).fetchone():continue
    parsed=json.loads(row[1]);text='♻️ Pemulihan kandidat lama; kartu ini mungkin pernah diterima.\n'+svc.format_telegram_review_card(parsed,row[0])
    for oid in str(owner or '').split(','):
     if oid.strip():rel.enqueue(db,'candidate',row[0],oid.strip(),'sendMessage',{'chat_id':oid.strip(),'text':text,'parse_mode':'HTML','reply_markup':{'inline_keyboard':[[{'text':'✅ Approve','callback_data':'gma:'+row[0]},{'text':'✏️ Edit','callback_data':'gmc:'+row[0]},{'text':'❌ Ignore','callback_data':'gmi:'+row[0]}]]}})
    count+=1
  result={'legacy_candidates_queued':count}
 else:
  if a.mode in ('backfill','dry-run'):
   bounds=rel.state(db,'backfill_bounds')
   if not bounds:
    end=int(time.time());bounds={'start':end-30*86400,'end':end}
    with db.get_connection():rel.put(db,'backfill_bounds',bounds)
   query=f"after:{bounds['start']} before:{bounds['end']}"
   result={'status':'completed','complete':True,'already_completed':True} if a.mode=='backfill' and rel.state(db,'job:backfill',{}).get('complete') else svc.scan_inbox(query=query,max_results=50,dry_run=a.mode=='dry-run',job_key='backfill')
  else:result=svc.scan_inbox()
  result={k:v for k,v in result.items() if k not in ('results','items')}
 print(json.dumps(result,ensure_ascii=False))
except Exception as e:
 print(json.dumps({'status':'failed','code':type(e).__name__,'detail':str(e)},ensure_ascii=False));sys.exit(1)
