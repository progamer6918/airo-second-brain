#!/usr/bin/env python3
"""Private V3 birthday sender. No automatic retry after an uncertain delivery."""
import argparse
from contextlib import closing, contextmanager
import csv
from datetime import date, datetime
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import sqlite3
import stat
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo('Asia/Jakarta')
EXPECTED_BOT = 'earnsai_reminder_bot'
SMOKE_MESSAGE = '✅ AIRO Birthday Reminder VPS recovery test berhasil.'


class RecoveryError(Exception):
    """Only application-owned codes may reach logs."""


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def private_path(root, path, directory=False):
    root, path = Path(root).absolute(), Path(path).absolute()
    if not path.is_relative_to(root):
        raise RecoveryError('PRIVATE_PATH_OUTSIDE_ROOT')
    for part in (path, *path.parents):
        if part.is_symlink():
            raise RecoveryError('PRIVATE_PATH_SYMLINK')
        if part == root:
            break
    info = path.stat()
    expected = stat.S_ISDIR if directory else stat.S_ISREG
    if not expected(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
        raise RecoveryError('PRIVATE_PATH_OWNER_OR_PERMISSIONS')
    return path


def read_private_json(root, path):
    return json.loads(private_path(root, path).read_text())


def load_dataset(root):
    root = private_path(root, root, directory=True)
    pointer = read_private_json(root, root / 'prepared-dataset.json')
    directory = private_path(root, Path(pointer['dataset_dir']), directory=True)
    manifest = read_private_json(root, directory / 'manifest.json')
    data = private_path(root, directory / 'birthdays.csv').read_bytes()
    checksum = hashlib.sha256(data).hexdigest()
    if (checksum != pointer['private_csv_sha256'] or checksum != manifest['PRIVATE_CSV_SHA256']
            or pointer['source_sha256'] != manifest['SOURCE_SHA256']
            or manifest.get('DATA_AUTHORITY') != 'OWNER_DESIGNATED_LATEST_SOURCE'):
        raise RecoveryError('DATASET_AUTHORITY_OR_CHECKSUM_MISMATCH')
    people = []
    reader = csv.DictReader(io.StringIO(data.decode('utf-8-sig')))
    required = {'NAMA', 'BIRTH_DAY', 'BIRTH_MONTH', 'BIRTH_YEAR', 'YEAR_KNOWN',
                'SOURCE_FILE_ID', 'SOURCE_SHA256', 'REVIEW_FLAGS'}
    if not required.issubset(reader.fieldnames or []):
        raise RecoveryError('V3_CSV_HEADERS_REQUIRED')
    for row in reader:
        if (not row['NAMA'].strip() or row['NAMA'].strip() == '-'
                or row['REVIEW_FLAGS'] not in ('', 'POSSIBLE_DUPLICATE')
                or row['SOURCE_SHA256'] != pointer['source_sha256']
                or row['SOURCE_FILE_ID'] != pointer['source_file_id']):
            raise RecoveryError('INELIGIBLE_CSV_RECORD')
        day, month = int(row['BIRTH_DAY']), int(row['BIRTH_MONTH'])
        date(2024, month, day)  # Leap-day-safe validation without inventing birth year.
        if row['YEAR_KNOWN'] not in ('0', '1'):
            raise RecoveryError('INVALID_YEAR_KNOWN')
        known = row['YEAR_KNOWN'] == '1'
        year = int(row['BIRTH_YEAR']) if known else None
        if known:
            if year <= 1900 or year == 2024:
                raise RecoveryError('PLACEHOLDER_YEAR_CANNOT_BE_KNOWN')
            date(year, month, day)
        elif row['BIRTH_YEAR']:
            raise RecoveryError('UNKNOWN_YEAR_MUST_BE_EMPTY')
        people.append({'name': row['NAMA'], 'day': day, 'month': month, 'year': year})
    if len(people) != manifest['VALID_BIRTHDAY_ROWS']:
        raise RecoveryError('DATASET_ROW_COUNT_MISMATCH')
    return people, checksum


def current_day(now=None):
    return (now or datetime.now(TIMEZONE)).astimezone(TIMEZONE).date()


def build_message(matches, today):
    lines = ['🎂 Reminder Ulang Tahun Hari Ini', f"Tanggal: {today.strftime('%d/%m/%Y')}",
             '', 'Hari ini ada yang ulang tahun:', '']
    for index, person in enumerate(matches, 1):
        birth_text = f"{person['day']:02d}/{person['month']:02d}"
        age = 'tahun lahir belum pasti'
        if person['year'] is not None:
            birth_text += f"/{person['year']}"
            age = f"{today.year - person['year']} tahun"
        lines += [f"{index}. {person['name']}", f'   Tanggal lahir: {birth_text}', f'   Usia: {age}', '']
    lines.append('Jangan lupa follow up / kirim ucapan.')
    return '\n'.join(lines)


def telegram_api(token, method, payload=None):
    request = Request(f'https://api.telegram.org/bot{token}/{method}',
                      data=urlencode(payload or {}).encode(), method='POST')
    try:
        with urlopen(request, timeout=30) as response:
            result = json.loads(response.read(1024 * 1024))
    except Exception:
        raise RecoveryError('TELEGRAM_API_OUTCOME_UNCONFIRMED') from None
    if not isinstance(result, dict) or result.get('ok') is not True:
        raise RecoveryError('TELEGRAM_API_REJECTED_OR_INVALID')
    return result['result']


def verify_identity(root, checksum, environ=None, api=telegram_api):
    environ = os.environ if environ is None else environ
    token, recipient = environ.get('TELEGRAM_BOT_TOKEN'), environ.get('TELEGRAM_CHAT_ID')
    if not token or not recipient:
        raise RecoveryError('DEDICATED_CREDENTIALS_MISSING')
    try:
        recipient = str(int(recipient))
    except ValueError:
        raise RecoveryError('AUTHORITATIVE_NUMERIC_RECIPIENT_REQUIRED') from None
    activation = read_private_json(root, root / 'activation.json')
    if (activation.get('status') != 'VERIFIED' or activation.get('scope') != 'BIRTHDAY_REMINDER_ONLY'
            or activation.get('bot_username') != EXPECTED_BOT or not activation.get('authority_ref')
            or activation.get('dataset_sha256') != checksum
            or activation.get('recipient_sha256') != digest(recipient)):
        raise RecoveryError('BIRTHDAY_ACTIVATION_AUTHORITY_REQUIRED')
    me = api(token, 'getMe')
    if (me.get('username') != EXPECTED_BOT or me.get('is_bot') is not True
            or me.get('id') != activation.get('bot_id')):
        raise RecoveryError('DEDICATED_BOT_IDENTITY_MISMATCH')
    chat = api(token, 'getChat', {'chat_id': recipient})
    if str(chat.get('id')) != recipient:
        raise RecoveryError('RECIPIENT_IDENTITY_MISMATCH')
    return token, recipient


@contextmanager
def delivery_lock(root):
    os.umask(0o077)
    root = Path(root)
    root.mkdir(mode=0o700, exist_ok=True)
    private_path(root, root, directory=True)
    lock = root / 'delivery.lock'
    fd = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        private_path(root, lock)
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def send_once(state_root, delivery_key, text, recipient, send):
    """Persist intent before sending. A crash/timeout never enables automatic resend.

    The lock spans claim, network call and final commit. There is deliberately no
    reset/retry command for uncertain entries; reconcile against actual delivery
    evidence before an explicitly authorized operational recovery.
    """
    if len(text.encode('utf-16-le')) // 2 > 4096:
        raise RecoveryError('MESSAGE_TOO_LONG_REQUIRES_REVIEW')
    state_root = Path(state_root)
    with delivery_lock(state_root):
        database = state_root / 'delivery.sqlite3'
        if database.exists() or database.is_symlink():
            private_path(state_root, database)
        with closing(sqlite3.connect(database)) as conn:
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute('PRAGMA synchronous=FULL')
            conn.execute('''CREATE TABLE IF NOT EXISTS deliveries (
                delivery_key TEXT PRIMARY KEY, status TEXT NOT NULL,
                message_sha256 TEXT NOT NULL, recipient_sha256 TEXT NOT NULL,
                attempted_at TEXT NOT NULL, message_id INTEGER)''')
            conn.commit()
            row = conn.execute('SELECT status,recipient_sha256,message_id FROM deliveries WHERE delivery_key=?',
                               (delivery_key,)).fetchone()
            if row:
                if row[1] != digest(recipient):
                    raise RecoveryError('DESTINATION_CHANGED_REQUIRES_REVIEW')
                return {'status': 'ALREADY_SENT' if row[0] == 'SENT' else 'UNCERTAIN_REQUIRES_RECONCILIATION',
                        'message_id': row[2]}
            conn.execute('INSERT INTO deliveries VALUES (?,?,?,?,?,NULL)',
                         (delivery_key, 'SENDING', digest(text), digest(recipient),
                          datetime.now(TIMEZONE).isoformat()))
            conn.commit()  # Durable barrier before any external send side effect.
            try:
                response = send(text)
                message_id = response.get('message_id')
                if (not isinstance(message_id, int) or isinstance(message_id, bool) or message_id <= 0
                        or str(response.get('chat', {}).get('id')) != recipient):
                    raise RecoveryError('DELIVERY_ACK_INVALID')
            except Exception:
                conn.execute("UPDATE deliveries SET status='UNKNOWN' WHERE delivery_key=?", (delivery_key,))
                conn.commit()
                raise RecoveryError('DELIVERY_UNCERTAIN_RECONCILE_BEFORE_RETRY') from None
            conn.execute("UPDATE deliveries SET status='SENT',message_id=? WHERE delivery_key=?", (message_id, delivery_key))
            conn.commit()
            return {'status': 'SENT', 'message_id': message_id}


def run(root, check=False, smoke=False):
    root = Path(root)
    people, checksum = load_dataset(root)
    today = current_day()
    matches = [p for p in people if (p['month'], p['day']) == (today.month, today.day)]
    if check:
        return {'status': 'CHECK_ONLY', 'eligible_rows': len(people), 'matches': len(matches), 'sends': 0}
    if not matches and not smoke:
        return {'status': 'NO_MATCH', 'sends': 0}
    token, recipient = verify_identity(root, checksum)
    text = SMOKE_MESSAGE if smoke else build_message(matches, today)
    # Dataset edits, restarts and clock overrides must not create another daily key.
    key = 'smoke:recovery-v2' if smoke else f'birthday:{today.isoformat()}'
    return send_once(root / 'sender-state', key, text, recipient,
                     lambda message: telegram_api(token, 'sendMessage', {'chat_id': recipient, 'text': message}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private-root', type=Path, required=True)
    parser.add_argument('--check', action='store_true', help='Validate private data; no credentials, network or send state')
    parser.add_argument('--smoke', action='store_true', help='One approved recovery smoke; independently durable key')
    args = parser.parse_args()
    try:
        result = run(args.private_root, args.check, args.smoke)
    except Exception as exc:
        code = str(exc) if isinstance(exc, RecoveryError) else 'LOCAL_VALIDATION_OR_STATE_ERROR'
        print(json.dumps({'status': 'ERROR', 'code': code}))
        return 1
    print(json.dumps(result))  # Never print names, dates of birth, tokens, chat IDs or API bodies.
    return 3 if result['status'] == 'UNCERTAIN_REQUIRES_RECONCILIATION' else 0


if __name__ == '__main__':
    sys.exit(main())
