"""Native Windows encrypted ASB backup; no WSL, pruning, or account login.

Format AIROGCM1: magic8 + salt32 + nonce12 + gzip tar ciphertext + tag16.
AES-256-GCM key: PBKDF2-HMAC-SHA256(recovery.key bytes, salt, 600000).
The 52-byte header is authenticated as additional data. Key stays on PC.
"""
import argparse, hashlib, io, json, os, shutil, sqlite3, subprocess, tarfile, tempfile, time
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BASE=Path(r'D:\AIRO_PRIVATE_BACKUPS\WSL-MIGRATION-20261006')
SSH=Path(r'C:\Windows\System32\OpenSSH\ssh.exe')
SCP=SSH.with_name('scp.exe')
SSHKEY=Path(r'C:\Users\Admin\.ssh\airo_tencent_vps.pem')
GIT=Path(r'C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe')
REMOTE='ubuntu@43.157.241.228'
DEST='/home/ubuntu/.local/state/airo-migration-backups/20261006'
SOURCES={'asb':Path(r'C:\Users\Admin\AI_WORKSPACES\airo-second-brain'),
         'recovery-staging':Path(r'C:\Users\Admin\AI_WORKSPACES\ASB_RECOVERY_STAGING'),
         'clip-inbox':Path(r'C:\Users\Admin\AIRO_CLIP_INBOX')}
EXCLUDED={'node_modules','venv','.venv','__pycache__','.pytest_cache'}

def command(args,**kwargs):
    result=subprocess.run([str(x) for x in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,**kwargs)
    if result.returncode:raise RuntimeError('Native command failed: '+Path(str(args[0])).name+' exit '+str(result.returncode))
    return result.stdout

def key(header):
    return PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=header[8:40],iterations=600000).derive((BASE/'recovery.key').read_bytes())

class EncryptWriter:
    def __init__(self,out,encryptor):self.out=out;self.encryptor=encryptor
    def write(self,data):self.out.write(self.encryptor.update(data));return len(data)
    def flush(self):self.out.flush()

class DecryptReader:
    def __init__(self,path):
        self.file=path.open('rb');header=self.file.read(52);assert header[:8]==b'AIROGCM1'
        self.remaining=path.stat().st_size-52-16
        self.file.seek(-16,2);tag=self.file.read(16);self.file.seek(52)
        self.dec=Cipher(algorithms.AES(key(header)),modes.GCM(header[40:52],tag)).decryptor()
        self.dec.authenticate_additional_data(header);self.finalized=False
    def read(self,n=-1):
        n=min(self.remaining,1048576 if n<0 else n)
        if n:
            data=self.file.read(n);assert len(data)==n;self.remaining-=n;return self.dec.update(data)
        if not self.finalized:self.dec.finalize();self.finalized=True
        return b''
    def finish(self):
        while self.read(1048576):pass
        assert self.finalized;self.file.close()

class HashReader:
    def __init__(self,source):self.source=source;self.hash=hashlib.sha256()
    def read(self,n=-1):
        data=self.source.read(n);self.hash.update(data);return data

def collect():
    entries=[];skipped=[]
    for label,root in SOURCES.items():
        if not root.exists():continue
        for parent,dirs,files in os.walk(root,followlinks=False):
            for name in list(dirs):
                p=Path(parent)/name
                if name in EXCLUDED or p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()):
                    dirs.remove(name);skipped.append(label+'/'+str(p.relative_to(root)).replace('\\','/'))
            for name in files:
                p=Path(parent)/name
                if p.is_symlink():skipped.append(label+'/'+str(p.relative_to(root)));continue
                # SQLite sidecars are represented by an online DB snapshot.
                if name.endswith(('-wal','-shm')) and Path(str(p)[:-4]).exists():continue
                entries.append((label+'/'+p.relative_to(root).as_posix(),p))
    return entries,skipped

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--scheduled',action='store_true')
    parser.add_argument('--restore-file',type=Path);parser.add_argument('--restore-directory',type=Path)
    args=parser.parse_args()
    assert os.name=='nt' and BASE.is_dir() and (BASE/'recovery.key').exists()
    if args.restore_file:
        assert args.restore_directory and not args.restore_directory.exists(),'Restore destination must be a new directory'
        assert args.restore_directory.resolve().is_relative_to(BASE.resolve()),'Restore only into a new directory under the private backup root'
        stage=Path(tempfile.mkdtemp(prefix='authenticated-full-restore-',dir=BASE))
        reader=DecryptReader(args.restore_file);restored={};manifest=None
        with tarfile.open(fileobj=reader,mode='r|gz') as bundle:
            for m in bundle:
                rel=Path(m.name);assert not rel.is_absolute() and '..' not in rel.parts and m.isfile()
                assert rel.parts[0] in list(SOURCES)+['native-backup-manifest.json']
                src=bundle.extractfile(m)
                if m.name=='native-backup-manifest.json':manifest=json.load(src);continue
                p=stage/rel;p.parent.mkdir(parents=True,exist_ok=True);digest=hashlib.sha256()
                with p.open('xb') as out:
                    for chunk in iter(lambda:src.read(1048576),b''):out.write(chunk);digest.update(chunk)
                restored[m.name]=digest.hexdigest()
        reader.finish();assert manifest and restored==manifest['hashes'],'Restore hashes did not match'
        args.restore_directory.parent.mkdir(parents=True,exist_ok=True)
        assert stage.resolve().parent==BASE.resolve()
        # Authentication completes before data reaches the requested destination.
        shutil.move(str(stage),str(args.restore_directory))
        print(json.dumps({'restore':'PASS','files':len(restored),'destination':str(args.restore_directory)}),flush=True)
        return
    latest=BASE/'native-backup-latest-receipt.json'
    if args.scheduled and latest.exists():
        prior=json.loads(latest.read_text())
        if prior.get('status')=='PASS' and time.time()-prior['completed_epoch']<23*3600:return
    stamp=time.strftime('%Y%m%d_%H%M%S');out=BASE/('native-'+stamp+'.agcm')
    receipt={'status':'IN_PROGRESS','started_epoch':time.time(),'format':'AIROGCM1','archive':out.name,'wsl_used':False,'key_transferred':False,'old_files_deleted':False}
    entries,skipped=collect();estimated=sum(p.stat().st_size for _,p in entries)
    assert shutil.disk_usage(BASE).free>estimated+2*1024**3,'Insufficient local free space; no old backups deleted'
    remote_free=int(command([SSH,'-i',SSHKEY,'-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',REMOTE,"df -B1 --output=avail /home/ubuntu | tail -1"],text=True).strip())
    assert remote_free>estimated+2*1024**3,'Insufficient VPS free space; no old backups deleted'
    temp=Path(tempfile.mkdtemp(prefix='native-restore-proof-',dir=BASE))
    manifest={};sqlite_names=[]
    try:
        header=b'AIROGCM1'+os.urandom(32)+os.urandom(12)
        enc=Cipher(algorithms.AES(key(header)),modes.GCM(header[40:52])).encryptor();enc.authenticate_additional_data(header)
        with out.open('xb') as file:
            file.write(header)
            with tarfile.open(fileobj=EncryptWriter(file,enc),mode='w|gz') as bundle:
                for name,p in entries:
                    original=p;before=p.stat()
                    if p.suffix in ('.db','.sqlite','.sqlite3'):
                        sample=p.open('rb').read(16)
                        if sample==b'SQLite format 3\x00':
                            p=temp/'sqlite-snapshots'/Path(name);p.parent.mkdir(parents=True,exist_ok=True)
                            with sqlite3.connect(original.as_uri()+'?mode=ro',uri=True) as src,sqlite3.connect(p) as dst:
                                src.backup(dst);assert dst.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
                            sqlite_names.append(name)
                    info=bundle.gettarinfo(str(p),arcname=name)
                    with p.open('rb') as src:
                        reader=HashReader(src);bundle.addfile(info,reader);manifest[name]=reader.hash.hexdigest()
                    if p==original:
                        after=p.stat();assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns),'Source changed during backup; no success claimed'
                payload=json.dumps({'hashes':manifest,'sqlite_snapshots':sqlite_names,'excluded_rebuildable_or_link_paths':skipped},ensure_ascii=False).encode()
                info=tarfile.TarInfo('native-backup-manifest.json');info.size=len(payload);bundle.addfile(info,io.BytesIO(payload))
            file.write(enc.finalize());file.write(enc.tag);file.flush();os.fsync(file.fileno())
        # Full authenticated decryption + hash validation, with materialized Git,
        # SQLite and an ordinary document restore rather than a listing only.
        restored={};stored_manifest=None;reader=DecryptReader(out)
        proof=temp/'restored';proof.mkdir()
        with tarfile.open(fileobj=reader,mode='r|gz') as bundle:
            for member in bundle:
                rel=Path(member.name);assert not rel.is_absolute() and '..' not in rel.parts and member.isfile()
                source=bundle.extractfile(member)
                if member.name=='native-backup-manifest.json':stored_manifest=json.load(source);continue
                digest=hashlib.sha256();target=None
                if member.name.startswith('asb/.git/') or member.name in sqlite_names or member.name=='asb/README.md':
                    p=proof/rel;p.parent.mkdir(parents=True,exist_ok=True);target=p.open('wb')
                for chunk in iter(lambda:source.read(1048576),b''):
                    digest.update(chunk)
                    if target:target.write(chunk)
                if target:target.close()
                restored[member.name]=digest.hexdigest()
        reader.finish();assert stored_manifest and restored==stored_manifest['hashes']
        if (proof/'asb/.git').exists():command([GIT,'-c','safe.directory='+str(proof/'asb'),'-C',proof/'asb','fsck','--full','--no-reflogs'],text=True)
        for name in sqlite_names:
            with sqlite3.connect(proof/name) as db:assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        sha=hashlib.file_digest(out.open('rb'),'sha256').hexdigest()
        command([SCP,'-i',SSHKEY,'-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',out,REMOTE+':'+DEST+'/'+out.name])
        remote_sha=command([SSH,'-i',SSHKEY,'-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',REMOTE,'sha256sum '+DEST+'/'+out.name],text=True).split()[0]
        assert remote_sha==sha
        receipt.update(status='PASS',completed_epoch=time.time(),bytes=out.stat().st_size,sha256=sha,full_authenticated_restore_hashes=True,restored_files=len(restored),sqlite_restores=len(sqlite_names),git_fsck='PASS' if (proof/'asb/.git').exists() else 'NOT_PRESENT',remote_checksum_match=True,proof_directory=str(proof),excluded_count=len(skipped))
    except BaseException as exc:
        receipt.update(status='FAIL',error_type=type(exc).__name__)
        raise
    finally:
        (BASE/('native-'+stamp+'-receipt.json')).write_text(json.dumps(receipt,indent=2));latest.write_text(json.dumps(receipt,indent=2))
        print(json.dumps(receipt),flush=True)

if __name__=='__main__':main()
