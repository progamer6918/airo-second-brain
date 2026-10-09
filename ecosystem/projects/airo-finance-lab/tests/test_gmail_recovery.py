import sys,os,tempfile,unittest,json,time
from pathlib import Path
from unittest.mock import MagicMock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
os.environ['AIRO_FINANCE_OFFLINE_TEST']='1'
from airo_finance_core import DatabaseManager,FinanceCoreEngine,GmailIntelligenceService
from airo_finance_core.telegram_ingress import TelegramOutboundAdapter,FinanceTelegramIngressRouter
from airo_finance_core import gmail_reliability as rel
class Recovery(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.db=DatabaseManager(self.tmp.name+'/test.db');self.db.init_schema();self.e=FinanceCoreEngine(self.db)
  self.acc=self.e.create_account('Blu','BANK',1000);self.dst=self.e.create_account('Saving','BANK',500)
  self.calls=[];self.out=TelegramOutboundAdapter('mock',transport=lambda m,p:self.calls.append((m,p)) or {'ok':True,'result':{'message_id':42}})
  self.s=GmailIntelligenceService(self.e,outbound=self.out,owner_chat_id='1');self.s.defer_delivery=True
 def tearDown(self):self.db.close();self.tmp.cleanup()
 def item(self,mid='m1',text='Pembayaran QRIS Rp100 di Toko'):
  return self.s.process_email(text,'Transaksi berhasil','receipt@blubybcadigital.id',mid)
 def api(self,pages,fail=None):
  api=MagicMock();api.users().messages().list().execute.side_effect=pages
  def get(**args):
   if fail and args['id']==fail:raise ConnectionError('network')
   x=MagicMock();x.execute.return_value={'snippet':'Pembayaran QRIS Rp100 di Toko','payload':{'headers':[{'name':'From','value':'receipt@blubybcadigital.id'}]}};return x
  api.users().messages().get.side_effect=get;self.s._gmail_service=api;return api
 def test_default_and_ambiguous(self):
  p=self.s.parse_email('Nominal Rp10.000','Transaksimu Pakai blu Berhasil','receipt@blu.id');self.assertEqual(p['tx_type'],'Pengeluaran');self.assertFalse(p['direction_known'])
  r=self.s.process_email('Nominal Rp100','Receipt','unknown@example.test','unknown');self.assertLess(r['confidence'],.7);self.assertIsNone(r['parsed']['account_id'])
  with self.assertRaises(ValueError):self.e.approve_review_item(r['review_id'])
 def test_atomic_candidate_rollback(self):
  with patch.object(rel,'enqueue',side_effect=RuntimeError('crash')):
   with self.assertRaises(RuntimeError):self.item()
  c=self.db.get_connection();self.assertEqual(c.execute('SELECT COUNT(*) FROM review_queue').fetchone()[0],0);self.assertEqual(c.execute('SELECT COUNT(*) FROM processed_emails').fetchone()[0],0)
 def test_message_id_and_fingerprint(self):
  a=self.item();self.assertEqual(self.item()['status'],'DUPLICATE_SKIPPED');b=self.item('m2');self.assertEqual(b['status'],'QUEUED_FOR_REVIEW');self.assertIn('Kemungkinan duplikat',' '.join(b['parsed']['review_reasons']))
 def test_pagination_and_lock(self):
  api=self.api([{'messages':[{'id':'one'}],'nextPageToken':'p2'},{'messages':[{'id':'two'}]}]);r=self.s.scan_inbox();self.assertEqual(r['scanned'],2);self.assertEqual(r['status'],'completed');self.assertTrue(r['complete'])
  with rel.lock(self.db):self.assertEqual(self.s.scan_inbox()['status'],'already_running')
 def test_failure_isolation(self):
  self.api([{'messages':[{'id':'bad'},{'id':'good'}]}]);original=self.s.process_email
  self.s.process_email=lambda *a,**k:(_ for _ in ()).throw(ValueError('bad parse')) if a[3]=='bad' else original(*a,**k)
  r=self.s.scan_inbox();self.assertEqual(r['errors'],1);self.assertEqual(r['processed'],1);self.assertEqual(r['status'],'partial')
 def test_resume(self):
  self.api([{'messages':[{'id':'one'}],'nextPageToken':'p2'},{'messages':[{'id':'two'}]}])
  r=self.s.scan_inbox(job_key='backfill',budget_seconds=0);self.assertEqual(r['status'],'partial')
  r=self.s.scan_inbox(job_key='backfill');self.assertEqual(r['scanned_total'],2);self.assertTrue(rel.state(self.db,'job:backfill')['complete'])
 def test_outbox_retry_uncertain_permanent(self):
  self.item();fail=TelegramOutboundAdapter('mock',lambda m,p:{'ok':False,'error_code':503})
  rel.dispatch(self.db,fail);row=self.db.get_connection().execute('SELECT * FROM finance_outbox').fetchone();self.assertEqual(row['status'],'RETRY');self.assertEqual(row['attempts'],1)
  with self.db.get_connection():self.db.get_connection().execute('UPDATE finance_outbox SET next_at=0')
  rel.dispatch(self.db,self.out);self.assertEqual(self.db.get_connection().execute('SELECT status FROM finance_outbox').fetchone()[0],'SENT')
  self.item('m2');unc=TelegramOutboundAdapter('mock',lambda m,p:{'ok':False,'error':'TimeoutError','uncertain':True});rel.dispatch(self.db,unc);self.assertEqual(self.db.get_connection().execute("SELECT status FROM finance_outbox WHERE status!='SENT'").fetchone()[0],'UNCERTAIN')
 def test_approval_receipt_and_repeated_click(self):
  r=self.item();item,tx=self.e.approve_review_item(r['review_id']);text=rel.receipt(self.e,tx);self.assertIn('Blu',text);self.assertIn('Rp900',text)
  with self.assertRaises(ValueError):self.e.approve_review_item(r['review_id'])
  self.assertEqual(self.e.get_account(self.acc.id).balance,900)
  rel.deliver_receipt(self.e,self.out,'1',2,tx);rel.deliver_receipt(self.e,self.out,'1',2,tx);self.assertEqual(sum(m=='editMessageText' for m,p in self.calls),1)
 def test_transfer_receipt(self):
  out,into=self.e.transfer_funds(self.acc.id,self.dst.id,100);text=rel.receipt(self.e,out);self.assertIn('Saving',text);self.assertIn('Rp600',text);self.assertIn('Rp900',text)
 def test_approval_atomic_rollback(self):
  r=self.item();original=self.e.record_transaction_metadata
  self.e.record_transaction_metadata=lambda **k:(_ for _ in ()).throw(RuntimeError('crash'))
  with self.assertRaises(RuntimeError):self.e.approve_review_item(r['review_id'])
  self.assertEqual(self.e.get_account(self.acc.id).balance,1000);self.assertEqual(self.e.get_review_queue_item(r['review_id']).status,'PENDING')
 def test_watchdog_and_recovery(self):
  with self.db.get_connection():rel.put(self.db,'health',{'last_finished_at':time.time(),'last_status':'failed'})
  rel.watchdog(self.db,self.out,'1');rel.watchdog(self.db,self.out,'1');self.assertEqual(len(self.calls),1)
  with self.db.get_connection():rel.put(self.db,'health',{'last_finished_at':time.time(),'last_status':'completed'})
  rel.watchdog(self.db,self.out,'1');self.assertEqual(len(self.calls),2);self.assertFalse(rel.state(self.db,'incident')['active'])
 def test_manual_router_receipt(self):
  router=FinanceTelegramIngressRouter(self.e,self.out,'1')
  cand=router.confirmation_handler.stage_input('beli kopi Rp100 blu')
  update={'callback_query':{'id':'cb','data':'cfm:'+cand.candidate_id,'from':{'id':'1'},'message':{'chat':{'id':'1'},'message_id':7}}}
  handled,status=router.handle_update(update)
  self.assertTrue(handled);self.assertTrue(status.startswith('CONFIRMED:'))
  edits=[p for m,p in self.calls if m=='editMessageText'];self.assertEqual(len(edits),1);self.assertIn('Rp900',edits[0]['text']);self.assertIn('Blu',edits[0]['text'])
 def test_receipt_atomic_failure(self):
  r=self.item()
  with patch.object(rel,'queue_receipt',side_effect=RuntimeError('outbox failure')):
   with self.assertRaises(RuntimeError):self.e.approve_review_item(r['review_id'],receipt_target=('1',2))
  self.assertEqual(self.e.get_account(self.acc.id).balance,1000);self.assertEqual(self.e.get_review_queue_item(r['review_id']).status,'PENDING')
 def test_credit_card_receipt(self):
  c=self.db.get_connection()
  with c:c.execute("INSERT INTO credit_cards(id,name,bank_name,credit_limit,current_balance,billing_cycle_day,payment_due_day) VALUES ('cc','Test Card','Test',5000,1000,1,10)")
  parsed={'account_id':self.acc.id,'amount':100,'direction':'CC_PAYMENT','credit_card_id':'cc','note':'Bayar kartu'}
  q=self.e.enqueue_review_item('test',parsed);item,tx=self.e.approve_review_item(q.id)
  text=rel.receipt(self.e,tx);self.assertIn('Sisa kewajiban Test Card',text);self.assertEqual(self.e.get_account(self.acc.id).balance,900)
 def test_partial_page_continuation(self):
  self.api([{'messages':[{'id':'one'},{'id':'two'}]}]);original=self.s.process_email
  def slow(*args,**kw):
   value=original(*args,**kw);time.sleep(.03);return value
  self.s.process_email=slow
  r=self.s.scan_inbox(job_key='backfill',budget_seconds=.01)
  self.assertEqual(r['status'],'partial');self.assertEqual(len(rel.state(self.db,'job:backfill')['pending']),1)
  self.s.process_email=original;r=self.s.scan_inbox(job_key='backfill')
  self.assertTrue(r['complete']);self.assertEqual(r['scanned_total'],2)
 def test_edit_does_not_guess_account(self):
  r=self.s.process_email('Nominal Rp100','Receipt','unknown@example.test','unknown')
  router=FinanceTelegramIngressRouter(self.e,self.out,'1')
  cq={'id':'cb','data':'gmc:'+r['review_id'],'from':{'id':'1'},'message':{'chat':{'id':'1'},'message_id':2}}
  handled,status=router.handle_update({'callback_query':cq});self.assertTrue(handled);self.assertIn('EDIT',status)
  cand=router.confirmation_handler.get_candidate(r['review_id']);self.assertFalse(cand.account_id);self.assertFalse(cand.direction_confirmed)
  cq['data']='dtype:'+r['review_id']+':INCOME';router.handle_update({'callback_query':cq});self.assertTrue(cand.direction_confirmed);self.assertEqual(cand.direction,'INCOME')
 def test_permanent_failure(self):
  self.item();rel.dispatch(self.db,TelegramOutboundAdapter('mock',lambda m,p:{'ok':False,'error_code':403}))
  self.assertEqual(self.db.get_connection().execute('SELECT status FROM finance_outbox').fetchone()[0],'ATTENTION')
 def test_inferred_email_date(self):
  r=self.s.process_email('Pembayaran QRIS Rp100','Receipt','receipt@blubybcadigital.id','dated',received_date='2026-09-10')
  self.assertEqual(r['parsed']['date'],'2026-09-10');self.assertTrue(r['parsed']['date_inferred_from_email'])
 def test_identity_mismatch_not_cached(self):
  import types
  creds=MagicMock();creds.expired=False
  fake_credentials=types.ModuleType('google.oauth2.credentials');fake_credentials.Credentials=MagicMock();fake_credentials.Credentials.from_authorized_user_file.return_value=creds
  fake_requests=types.ModuleType('google.auth.transport.requests');fake_requests.Request=MagicMock()
  fake_discovery=types.ModuleType('googleapiclient.discovery');candidate=MagicMock();candidate.users().getProfile().execute.return_value={'emailAddress':'other@example.test'};fake_discovery.build=MagicMock(return_value=candidate)
  mods={'google.oauth2.credentials':fake_credentials,'google.auth.transport.requests':fake_requests,'googleapiclient.discovery':fake_discovery}
  for name in ('google','google.oauth2','google.auth','google.auth.transport','googleapiclient'):
   m=types.ModuleType(name);m.__path__=[];mods[name]=m
  path=Path(self.tmp.name)/'mock_auth.json';path.write_text('{}')
  self.s.token_path=str(path)
  with patch.dict(sys.modules,mods):
   for _ in range(2):
    with self.assertRaises(RuntimeError):self.s.get_service()
    self.assertIsNone(self.s._gmail_service)
 def test_auth_failure_alert(self):
  with patch.object(self.s,'get_service',side_effect=PermissionError('auth failed')):
   with self.assertRaises(RuntimeError):self.s.scan_inbox()
  self.assertEqual(rel.state(self.db,'health')['last_status'],'failed');self.assertTrue(rel.state(self.db,'incident')['active'])
if __name__=='__main__':unittest.main()
