"""Offline regression: all people, credentials, recipients and sends are synthetic."""
import contextlib
import csv
from datetime import date, datetime, timezone
import hashlib
import importlib.util
import io
import json
import multiprocessing
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'ecosystem/projects/vortex-ai-skill-lab/scripts/personal-workflow/birthday_reminder_simple.py'
spec = importlib.util.spec_from_file_location('birthday_v4', SCRIPT)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


def worker(state, evidence, crash=False):
    def send(text):
        with open(evidence, 'a') as output:
            output.write('synthetic-send\n'); output.flush(); os.fsync(output.fileno())
        if crash:
            os._exit(17)
        time.sleep(0.02)
        return {'message_id': 7, 'chat': {'id': 123}}
    m.send_once(state, 'birthday:2026-10-15', 'synthetic message', '123', send)


class SenderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.state = self.root / 'sender-state'; self.calls = []

    def tearDown(self):
        self.temp.cleanup()

    def send(self, text):
        self.calls.append(text)
        return {'message_id': 7, 'chat': {'id': 123}}

    def once(self, send=None, text='synthetic message', recipient='123', key='birthday:2026-10-15'):
        return m.send_once(self.state, key, text, recipient, send or self.send)

    def dataset(self, rows=None):
        rows = rows or [{'NAMA': 'SYNTHETIC A', 'BIRTH_DAY': '15', 'BIRTH_MONTH': '10',
                         'BIRTH_YEAR': '', 'YEAR_KNOWN': '0', 'REVIEW_FLAGS': ''}]
        fields = ['NAMA', 'BIRTH_DAY', 'BIRTH_MONTH', 'BIRTH_YEAR', 'YEAR_KNOWN',
                  'SOURCE_FILE_ID', 'SOURCE_SHA256', 'REVIEW_FLAGS']
        for row in rows:
            row.update({'SOURCE_FILE_ID': 'synthetic', 'SOURCE_SHA256': 'a' * 64})
        stream = io.StringIO(); writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
        data = stream.getvalue().encode(); checksum = hashlib.sha256(data).hexdigest()
        folder = self.root / 'dataset'; folder.mkdir(mode=0o700)
        files = {folder / 'birthdays.csv': data,
            folder / 'manifest.json': json.dumps({'PRIVATE_CSV_SHA256': checksum,
                'SOURCE_SHA256': 'a' * 64, 'DATA_AUTHORITY': 'OWNER_DESIGNATED_LATEST_SOURCE',
                'VALID_BIRTHDAY_ROWS': len(rows)}).encode(),
            self.root / 'prepared-dataset.json': json.dumps({'dataset_dir': str(folder),
                'private_csv_sha256': checksum, 'source_sha256': 'a' * 64, 'source_file_id': 'synthetic'}).encode()}
        for path, content in files.items():
            path.write_bytes(content); path.chmod(0o600)
        return checksum

    def activation(self, checksum):
        value = {'status': 'VERIFIED', 'scope': 'BIRTHDAY_REMINDER_ONLY',
            'bot_username': 'earnsai_reminder_bot', 'bot_id': 42, 'authority_ref': 'synthetic-owner-reference',
            'dataset_sha256': checksum, 'recipient_sha256': m.digest('123')}
        path = self.root / 'activation.json'; path.write_text(json.dumps(value)); path.chmod(0o600)

    def api(self, token, method, payload=None):
        self.assertEqual(token, 'SYNTHETIC-ONLY')
        return {'id': 42, 'is_bot': True, 'username': 'earnsai_reminder_bot'} if method == 'getMe' else {'id': 123}

    def test_csv_unknown_year_no_age_inference(self):
        self.dataset(); people, _ = m.load_dataset(self.root)
        message = m.build_message(people, date(2026, 10, 15))
        self.assertIn('tahun lahir belum pasti', message)
        self.assertNotIn('/2024', message); self.assertNotIn('2 tahun', message)
        self.assertIn('🎂 Reminder Ulang Tahun Hari Ini', message)

    def test_known_year_format_preserved(self):
        message = m.build_message([{'name': 'SYNTHETIC', 'day': 15, 'month': 10, 'year': 2000}], date(2026, 10, 15))
        self.assertIn('15/10/2000', message); self.assertIn('26 tahun', message)

    def test_timezone_day_boundary(self):
        self.assertEqual(m.current_day(datetime(2026, 10, 14, 18, tzinfo=timezone.utc)), date(2026, 10, 15))

    def test_quarantine_flag_rejected(self):
        self.dataset([{'NAMA': 'SYNTHETIC', 'BIRTH_DAY': '15', 'BIRTH_MONTH': '10',
                       'BIRTH_YEAR': '', 'YEAR_KNOWN': '0', 'REVIEW_FLAGS': 'DATE_COLUMN_CONFLICT'}])
        with self.assertRaisesRegex(m.RecoveryError, 'INELIGIBLE_CSV_RECORD'):
            m.load_dataset(self.root)

    def test_checksum_tamper_rejected(self):
        self.dataset(); (self.root / 'dataset/birthdays.csv').write_text('tampered')
        with self.assertRaisesRegex(m.RecoveryError, 'CHECKSUM'):
            m.load_dataset(self.root)

    def test_dataset_permissions_rejected(self):
        self.dataset(); (self.root / 'dataset/birthdays.csv').chmod(0o644)
        with self.assertRaises(m.RecoveryError):
            m.load_dataset(self.root)

    def test_check_only_no_network_or_send_state(self):
        self.dataset()
        with mock.patch.object(m, 'verify_identity', side_effect=AssertionError('offline')):
            result = m.run(self.root, check=True)
        self.assertEqual(result['sends'], 0); self.assertFalse(self.state.exists())

    def test_no_match_zero_sends_without_credentials(self):
        self.dataset()
        with mock.patch.object(m, 'current_day', return_value=date(2026, 10, 16)), \
             mock.patch.object(m, 'verify_identity', side_effect=AssertionError('must not send')):
            self.assertEqual(m.run(self.root)['status'], 'NO_MATCH')
        self.assertFalse(self.state.exists())

    def test_retry_same_day_sent_once_even_changed_text(self):
        self.assertEqual(self.once()['status'], 'SENT')
        self.assertEqual(self.once(text='updated synthetic dataset')['status'], 'ALREADY_SENT')
        self.assertEqual(len(self.calls), 1)

    def test_later_day_can_send(self):
        self.once(); self.once(key='birthday:2026-10-16')
        self.assertEqual(len(self.calls), 2)

    def test_timeout_blocks_all_automatic_retries(self):
        def fail(text):
            self.calls.append('attempt'); raise TimeoutError('SYNTHETIC SECRET MUST NOT LEAK')
        with self.assertRaisesRegex(m.RecoveryError, '^DELIVERY_UNCERTAIN_RECONCILE_BEFORE_RETRY$'):
            self.once(send=fail)
        self.assertEqual(self.once()['status'], 'UNCERTAIN_REQUIRES_RECONCILIATION')
        self.assertEqual(self.calls, ['attempt'])

    def test_invalid_ack_blocks_retry(self):
        with self.assertRaises(m.RecoveryError):
            self.once(send=lambda text: {'message_id': 7, 'chat': {'id': 999}})
        self.assertEqual(self.once()['status'], 'UNCERTAIN_REQUIRES_RECONCILIATION')
        self.assertEqual(self.calls, [])

    def test_crash_after_external_send_preserves_uncertain_intent(self):
        ctx = multiprocessing.get_context('fork'); evidence = self.root / 'synthetic-deliveries'
        process = ctx.Process(target=worker, args=(str(self.state), str(evidence), True))
        process.start(); process.join(10); self.assertEqual(process.exitcode, 17)
        self.assertEqual(self.once()['status'], 'UNCERTAIN_REQUIRES_RECONCILIATION')
        self.assertEqual(len(evidence.read_text().splitlines()), 1); self.assertFalse(self.calls)

    def test_crash_before_external_send_blocks_retry(self):
        ctx = multiprocessing.get_context('fork')
        process = ctx.Process(target=lambda: self.once(send=lambda text: os._exit(18)))
        process.start(); process.join(10); self.assertEqual(process.exitcode, 18)
        self.assertEqual(self.once()['status'], 'UNCERTAIN_REQUIRES_RECONCILIATION')
        self.assertFalse(self.calls)

    def test_crash_after_ack_before_final_commit_blocks_retry(self):
        def ack_with_commit_failure(text):
            self.calls.append('external send')
            with sqlite3.connect(self.state / 'delivery.sqlite3') as conn:
                conn.execute("CREATE TRIGGER forced BEFORE UPDATE ON deliveries WHEN NEW.status='SENT' BEGIN SELECT RAISE(ABORT,'synthetic crash'); END")
            return {'message_id': 7, 'chat': {'id': 123}}
        with self.assertRaises(sqlite3.DatabaseError):
            self.once(send=ack_with_commit_failure)
        self.assertEqual(self.once()['status'], 'UNCERTAIN_REQUIRES_RECONCILIATION')
        self.assertEqual(self.calls, ['external send'])

    def test_overlapping_processes_send_once(self):
        ctx = multiprocessing.get_context('fork'); evidence = self.root / 'synthetic-deliveries'
        processes = [ctx.Process(target=worker, args=(str(self.state), str(evidence))) for _ in range(8)]
        for process in processes: process.start()
        for process in processes:
            process.join(10); self.assertEqual(process.exitcode, 0)
        self.assertEqual(len(evidence.read_text().splitlines()), 1)

    def test_restart_in_new_process_does_not_resend(self):
        ctx = multiprocessing.get_context('fork'); evidence = self.root / 'synthetic-deliveries'
        for _ in range(2):
            process = ctx.Process(target=worker, args=(str(self.state), str(evidence)))
            process.start(); process.join(10); self.assertEqual(process.exitcode, 0)
        self.assertEqual(len(evidence.read_text().splitlines()), 1)

    def test_changed_destination_requires_review(self):
        self.once()
        with self.assertRaisesRegex(m.RecoveryError, 'DESTINATION_CHANGED'):
            self.once(recipient='456')
        self.assertEqual(len(self.calls), 1)

    def test_oversize_message_never_attempted(self):
        with self.assertRaisesRegex(m.RecoveryError, 'MESSAGE_TOO_LONG'):
            self.once(text='x' * 4097)
        self.assertFalse(self.calls); self.assertFalse(self.state.exists())

    def test_state_symlink_rejected(self):
        actual = self.root / 'actual'; actual.mkdir(mode=0o700)
        self.state.symlink_to(actual, target_is_directory=True)
        with self.assertRaises(m.RecoveryError): self.once()

    def test_state_private_and_no_personal_payload(self):
        self.once(text='SYNTHETIC PRIVATE PAYLOAD')
        with sqlite3.connect(self.state / 'delivery.sqlite3') as conn:
            rows = conn.execute('SELECT * FROM deliveries').fetchall()
        self.assertNotIn('SYNTHETIC PRIVATE PAYLOAD', str(rows))
        self.assertEqual((self.state / 'delivery.sqlite3').stat().st_mode & 0o077, 0)

    def test_missing_credentials_fail_closed(self):
        with self.assertRaisesRegex(m.RecoveryError, 'DEDICATED_CREDENTIALS_MISSING'):
            m.verify_identity(self.root, 'synthetic', environ={}, api=self.api)

    def test_correct_identity_and_recipient_require_bound_authority(self):
        checksum = self.dataset(); self.activation(checksum)
        self.assertEqual(m.verify_identity(self.root, checksum,
            environ={'TELEGRAM_BOT_TOKEN': 'SYNTHETIC-ONLY', 'TELEGRAM_CHAT_ID': '123'}, api=self.api)[1], '123')

    def test_wrong_bot_rejected(self):
        checksum = self.dataset(); self.activation(checksum)
        with self.assertRaisesRegex(m.RecoveryError, 'BOT_IDENTITY_MISMATCH'):
            m.verify_identity(self.root, checksum,
                environ={'TELEGRAM_BOT_TOKEN': 'SYNTHETIC-ONLY', 'TELEGRAM_CHAT_ID': '123'},
                api=lambda *args: {'id': 42, 'is_bot': True, 'username': 'wrong_synthetic_bot'})

    def test_wrong_recipient_rejected(self):
        checksum = self.dataset(); self.activation(checksum)
        with self.assertRaisesRegex(m.RecoveryError, 'RECIPIENT_IDENTITY_MISMATCH'):
            m.verify_identity(self.root, checksum,
                environ={'TELEGRAM_BOT_TOKEN': 'SYNTHETIC-ONLY', 'TELEGRAM_CHAT_ID': '123'},
                api=lambda *args: self.api(*args) if args[1] == 'getMe' else {'id': 999})

    def test_actual_send_path_uses_daily_and_stable_smoke_keys(self):
        self.dataset()
        with mock.patch.object(m, 'current_day', return_value=date(2026, 10, 15)), \
             mock.patch.object(m, 'verify_identity', return_value=('SYNTHETIC-ONLY', '123')), \
             mock.patch.object(m, 'telegram_api', return_value={'message_id': 7, 'chat': {'id': 123}}) as api:
            self.assertEqual(m.run(self.root)['status'], 'SENT')
            self.assertEqual(m.run(self.root)['status'], 'ALREADY_SENT')
            self.assertEqual(m.run(self.root, smoke=True)['status'], 'SENT')
            self.assertEqual(m.run(self.root, smoke=True)['status'], 'ALREADY_SENT')
        self.assertEqual(api.call_count, 2)

    def test_cli_error_does_not_print_personal_records(self):
        self.dataset()
        result = subprocess.run(['python3', str(SCRIPT), '--private-root', str(self.root), '--smoke'],
                                text=True, capture_output=True, env={**os.environ, 'TELEGRAM_BOT_TOKEN': '', 'TELEGRAM_CHAT_ID': ''})
        self.assertEqual(result.returncode, 1)
        self.assertNotIn('SYNTHETIC A', result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['code'], 'DEDICATED_CREDENTIALS_MISSING')


    def test_h1_then_day_have_independent_durable_keys(self):
        self.dataset()
        with mock.patch.object(m, 'verify_identity', return_value=('SYNTHETIC-ONLY', '123')), \
             mock.patch.object(m, 'telegram_api', return_value={'message_id': 7, 'chat': {'id': 123}}) as api:
            with mock.patch.object(m, 'current_day', return_value=date(2026, 10, 14)):
                self.assertEqual(m.run(self.root, advance=True)['status'], 'SENT')
                self.assertEqual(m.run(self.root, advance=True)['status'], 'ALREADY_SENT')
            with mock.patch.object(m, 'current_day', return_value=date(2026, 10, 15)):
                self.assertEqual(m.run(self.root)['status'], 'SENT')
                self.assertEqual(m.run(self.root)['status'], 'ALREADY_SENT')
        self.assertEqual(api.call_count, 2)
        with sqlite3.connect(self.state / 'delivery.sqlite3') as conn:
            self.assertEqual(set(r[0] for r in conn.execute('SELECT delivery_key FROM deliveries')),
                             {'birthday-eve:2026-10-15', 'birthday:2026-10-15'})

    def test_h1_message_has_preparation_text_and_unknown_year(self):
        text = m.build_message([{'name': 'SYNTHETIC', 'day': 18, 'month': 10, 'year': None}], date(2026, 10, 18), advance=True)
        self.assertIn('H-1', text); self.assertIn('18/10/2026', text)
        self.assertIn('Siapkan desain ucapan', text); self.assertIn('tahun lahir belum pasti', text)

    def test_h1_year_boundary_uses_tomorrow_age(self):
        self.dataset([{'NAMA': 'SYNTHETIC', 'BIRTH_DAY': '1', 'BIRTH_MONTH': '1', 'BIRTH_YEAR': '2000', 'YEAR_KNOWN': '1', 'REVIEW_FLAGS': ''}])
        with mock.patch.object(m, 'current_day', return_value=date(2026, 12, 31)), \
             mock.patch.object(m, 'verify_identity', return_value=('SYNTHETIC-ONLY', '123')), \
             mock.patch.object(m, 'telegram_api', return_value={'message_id': 7, 'chat': {'id': 123}}) as api:
            self.assertEqual(m.run(self.root, advance=True)['status'], 'SENT')
        text = api.call_args[0][2]['text']; self.assertIn('01/01/2027', text); self.assertIn('27 tahun', text)

    def test_h1_leap_day_and_month_boundary(self):
        self.dataset([{'NAMA': 'SYNTHETIC', 'BIRTH_DAY': '29', 'BIRTH_MONTH': '2', 'BIRTH_YEAR': '', 'YEAR_KNOWN': '0', 'REVIEW_FLAGS': ''}])
        with mock.patch.object(m, 'current_day', return_value=date(2028, 2, 28)):
            self.assertEqual(m.run(self.root, check=True, advance=True)['matches'], 1)
        with mock.patch.object(m, 'current_day', return_value=date(2027, 2, 28)):
            self.assertEqual(m.run(self.root, check=True, advance=True)['matches'], 0)

    def test_cli_default_checks_both_day_and_eve_without_sends(self):
        self.dataset()
        result = subprocess.run(['python3', str(SCRIPT), '--private-root', str(self.root), '--check'], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(set(json.loads(result.stdout)['reminders']), {'day', 'eve'})
        self.assertFalse(self.state.exists())


if __name__ == '__main__':
    unittest.main()
