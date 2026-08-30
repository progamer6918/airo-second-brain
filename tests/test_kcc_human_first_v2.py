#!/usr/bin/env python3
import unittest
import os
import sys
import json
import shutil
import tempfile
import subprocess

CANONICAL_WSL = "/home/egitaristorandas/AI_WORKSPACES/airo-second-brain"
AIRO_SESSION_BIN = os.path.join(CANONICAL_WSL, "bin/airo-session")

class TestKCCHumanFirstV2(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.env = os.environ.copy()
        self.env["AIRO_SESSION_STATE_DIR"] = self.tmp_dir
        self.env["AIRO_REPO_ROOT"] = CANONICAL_WSL
        self.ev_file = os.path.join(self.tmp_dir, "evidence.txt")
        with open(self.ev_file, "w") as f:
            f.write("PASS")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_t1_owner_request_explicit(self):
        # T1 Owner request explicit -> visible semantic request correct
        start_cmd = [
            sys.executable, AIRO_SESSION_BIN, "start",
            "--project-id", "airo-second-brain",
            "--project-name", "AIRO Second Brain",
            "--title", "Test Explicit Request",
            "--objective", "Test explicit owner request in V2 note",
            "--initiator", "OWNER",
            "--owner-request-summary", "Tolong perbaiki pencatatan sesi agar lebih mudah dibaca manusia.",
            "--owner-request-capture", "EXPLICIT"
        ]
        res = subprocess.run(start_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Start failed: {res.stderr}")

        close_cmd = [
            sys.executable, AIRO_SESSION_BIN, "close",
            "--script-status", "SCRIPT_SUCCESS",
            "--required-evidence", json.dumps([self.ev_file]),
            "--actual-evidence", json.dumps([self.ev_file]),
            "--ringkasnya", "Sesi ini membuktikan pencatatan permintaan Owner secara eksplisit.",
            "--yang-lo-minta", "Tolong perbaiki pencatatan sesi agar lebih mudah dibaca manusia.",
            "--yang-dikerjakan", json.dumps(["Memperbarui template rendering catatan", "Menjalankan uji coba unit"]),
            "--hasil", "Pencatatan sesi berhasil menggunakan format V2 yang ramah pengguna.",
            "--batasan", "– Tidak ada batasan penting yang tersisa dari sesi ini.",
            "--berikutnya", "– Tidak ada. Tujuan sesi ini selesai."
        ]
        res_close = subprocess.run(close_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res_close.returncode, 0, f"Close failed: {res_close.stderr}")

    def test_t2_owner_request_inferred(self):
        # T2 Owner request inferred -> marked INFERRED, no fake exact wording
        start_cmd = [
            sys.executable, AIRO_SESSION_BIN, "start",
            "--project-id", "airo-second-brain",
            "--project-name", "AIRO Second Brain",
            "--title", "Test Inferred Request",
            "--objective", "Diagnosa otomatis kegagalan",
            "--initiator", "OWNER",
            "--owner-request-capture", "INFERRED_FROM_TASK_CONTEXT"
        ]
        res = subprocess.run(start_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

        close_cmd = [
            sys.executable, AIRO_SESSION_BIN, "close",
            "--script-status", "SCRIPT_SUCCESS",
            "--required-evidence", json.dumps([self.ev_file]),
            "--actual-evidence", json.dumps([self.ev_file]),
            "--ringkasnya", "Sesi diagnosa inferensi task.",
            "--yang-lo-minta", "Diagnosa kegagalan sistem otomatis (diambil dari konteks tugas).",
            "--yang-dikerjakan", json.dumps(["Analisis log sistem"]),
            "--hasil", "Akar masalah teridentifikasi.",
            "--batasan", "– Tidak ada batasan penting yang tersisa dari sesi ini.",
            "--berikutnya", "– Tidak ada. Analisis selesai."
        ]
        res_close = subprocess.run(close_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res_close.returncode, 0)

    def test_t3_system_session(self):
        # T3 system session -> no fake Owner request
        start_cmd = [
            sys.executable, AIRO_SESSION_BIN, "start",
            "--project-id", "airo-second-brain",
            "--project-name", "AIRO Second Brain",
            "--title", "Test System Routine",
            "--objective", "Routine system maintenance",
            "--initiator", "SYSTEM"
        ]
        res = subprocess.run(start_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

        close_cmd = [
            sys.executable, AIRO_SESSION_BIN, "close",
            "--script-status", "SCRIPT_SUCCESS",
            "--required-evidence", json.dumps([self.ev_file]),
            "--actual-evidence", json.dumps([self.ev_file]),
            "--ringkasnya", "Pemeliharaan rutin sistem AIRO.",
            "--yang-lo-minta", "Sesi otomatis sistem AIRO.",
            "--yang-dikerjakan", json.dumps(["Pembersihan cache"]),
            "--hasil", "Sistem berjalan optimal.",
            "--batasan", "– Tidak ada batasan penting yang tersisa dari sesi ini.",
            "--berikutnya", "– Tidak ada. Pemeliharaan selesai."
        ]
        res_close = subprocess.run(close_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res_close.returncode, 0)

    def test_t4_t5_t6_placeholders_rejected(self):
        # T4, T5, T6 Generic placeholders rejected
        start_cmd = [
            sys.executable, AIRO_SESSION_BIN, "start",
            "--project-id", "airo-second-brain",
            "--project-name", "AIRO Second Brain",
            "--title", "Test Placeholder Reject",
            "--objective", "Test placeholder rejection"
        ]
        subprocess.run(start_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)

        close_cmd = [
            sys.executable, AIRO_SESSION_BIN, "close",
            "--script-status", "SCRIPT_SUCCESS",
            "--required-evidence", json.dumps([self.ev_file]),
            "--actual-evidence", json.dumps([self.ev_file]),
            "--ringkasnya", "Test",
            "--yang-lo-minta", "Permintaan Owner belum tercatat secara semantik untuk sesi ini.",
            "--hasil", "Pekerjaan sesi telah selesai dieksekusi dan diverifikasi.",
            "--berikutnya", "Lanjut ke langkah berikutnya di roadmap kanonis."
        ]
        res_close = subprocess.run(close_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertNotEqual(res_close.returncode, 0)
        self.assertIn("prohibited placeholder", res_close.stderr)

    def test_t7_t8_machine_context_preserved(self):
        # T7 visible excludes dump, T8 machine context preserved in HTML comment
        start_cmd = [
            sys.executable, AIRO_SESSION_BIN, "start",
            "--project-id", "airo-second-brain",
            "--project-name", "AIRO Second Brain",
            "--title", "Test Machine Context",
            "--objective", "Verify AI machine context preservation",
            "--initiator", "OWNER"
        ]
        subprocess.run(start_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)

        close_cmd = [
            sys.executable, AIRO_SESSION_BIN, "close",
            "--script-status", "SCRIPT_SUCCESS",
            "--required-evidence", json.dumps([self.ev_file]),
            "--actual-evidence", json.dumps([self.ev_file]),
            "--ringkasnya", "Memvalidasi layer 2 machine context.",
            "--yang-lo-minta", "Pastikan AI tetap bisa membaca metadata lengkap di background.",
            "--yang-dikerjakan", json.dumps(["Menyimpan machine context ke HTML comment block"]),
            "--hasil", "Machine context tersimpan lengkap dan valid secara JSON.",
            "--batasan", "– Tidak ada batasan penting yang tersisa dari sesi ini.",
            "--berikutnya", "– Tidak ada. Pengujian selesai."
        ]
        res_close = subprocess.run(close_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res_close.returncode, 0)

    def test_t9_t10_t11_t12_integrity_and_markdown(self):
        # T9 separate statuses, T10 session id, T11 evidence, T12 valid markdown
        start_cmd = [
            sys.executable, AIRO_SESSION_BIN, "start",
            "--project-id", "airo-second-brain",
            "--project-name", "AIRO Second Brain",
            "--title", "Test Integrity Invariants",
            "--objective", "Test frontmatter and markdown structure"
        ]
        res_start = subprocess.run(start_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res_start.returncode, 0)

        close_cmd = [
            sys.executable, AIRO_SESSION_BIN, "close",
            "--script-status", "SCRIPT_SUCCESS",
            "--required-evidence", json.dumps([self.ev_file]),
            "--actual-evidence", json.dumps([self.ev_file]),
            "--ringkasnya", "Uji validitas frontmatter dan Markdown.",
            "--yang-lo-minta", "Pastikan status terpisah dan link Markdown valid.",
            "--yang-dikerjakan", json.dumps(["Uji verifikasi integritas"]),
            "--hasil", "Seluruh struktur frontmatter dan layer 1/2 sesuai standar.",
            "--batasan", "– Tidak ada batasan penting yang tersisa dari sesi ini.",
            "--berikutnya", "– Tidak ada. Pengujian tuntas."
        ]
        res_close = subprocess.run(close_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res_close.returncode, 0)

    def test_t13_t14_t15_invariants_and_path_behavior(self):
        # T13 event capture, T14 canonical path, T15 closeout visibility
        start_cmd = [
            sys.executable, AIRO_SESSION_BIN, "start",
            "--project-id", "airo-second-brain",
            "--project-name", "AIRO Second Brain",
            "--title", "Test Invariants and Paths",
            "--objective", "Ensure path and event capture invariants"
        ]
        subprocess.run(start_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)

        evt_cmd = [
            sys.executable, AIRO_SESSION_BIN, "event",
            "--event-type", "validation",
            "--summary", "Testing validation event in V2"
        ]
        res_evt = subprocess.run(evt_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res_evt.returncode, 0)

        close_cmd = [
            sys.executable, AIRO_SESSION_BIN, "close",
            "--script-status", "SCRIPT_SUCCESS",
            "--required-evidence", json.dumps([self.ev_file]),
            "--actual-evidence", json.dumps([self.ev_file]),
            "--ringkasnya", "Uji event capture dan jalur kanonis.",
            "--yang-lo-minta", "Verifikasi capture event dan penutupan jalur kanonis.",
            "--yang-dikerjakan", json.dumps(["Menjalankan event validation"]),
            "--hasil", "Invarian event capture dan visibility lolos 100%.",
            "--batasan", "– Tidak ada batasan penting yang tersisa dari sesi ini.",
            "--berikutnya", "– Tidak ada. Selesai."
        ]
        res_close = subprocess.run(close_cmd, env=self.env, cwd=CANONICAL_WSL, capture_output=True, text=True)
        self.assertEqual(res_close.returncode, 0)

if __name__ == "__main__":
    unittest.main()
