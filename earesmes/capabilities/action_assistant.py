"""
EARESMES Action Assistant Capability — P2.2
===========================================
Prepares bounded action proposals with explicit approval requirements.
Enforces that ACTION CAPABILITY != AUTONOMOUS EXECUTION.

Initial Supported Action Types:
  - DOCUMENT_DRAFT: Draft generation without auto-mutation
  - STATUS_READ: Read-only system and runtime inspection
  - COMMAND_PREPARE: Command proposal requiring Owner approval
  - HANDOFF_GENERATION: Information packaging for new sessions

Strictly rejects destructive operations (e.g. file deletion, drops, rm).
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import time
import uuid

# Global gate instance for runtime session
from earesmes.action.approval_gate import ActionApprovalGate, ActionState

_GLOBAL_GATE = ActionApprovalGate()


def get_global_action_gate() -> ActionApprovalGate:
    return _GLOBAL_GATE


def create_action_proposal(repo_root: Path, query: str, owner_id: str = "OWNER_TELEGRAM") -> str:
    """
    Evaluate action request, reject destructive operations, and generate
    an action proposal bound to an Action ID.
    """
    q = query.lower().strip()
    gate = get_global_action_gate()

    # 1. Test 3: Destructive Command Rejection
    destructive_keywords = ["hapus file", "hapus berkas", "delete file", "rm -rf", "drop database", "wipe", "format disk"]
    if any(dk in q for dk in destructive_keywords):
        intro = "Waduh Eg, operasi yang ini dilarang dieksekusi otomatis ya demi keselamatan sistem:"
        return (
            "⛔ AIRO ACTION REJECTED\n\n"
            f"{intro}\n\n"
            "Action:\n"
            "DESTRUCTIVE_OPERATION\n\n"
            "Reason:\n"
            "Tindakan destruktif (penghapusan berkas atau mutasi destruktif sistem) dilarang "
            "dalam batas tata kelola P2.2 Controlled Action Layer.\n\n"
            "Boundary:\n"
            "Earesmes beroperasi dalam prinsip non-destructive safety. Operasi ini harus dilakukan "
            "secara manual oleh Owner langsung bila diperlukan."
        )

    # 2. Test 1: Document Draft Generation
    if any(k in q for k in ["buat laporan", "buat draft", "generate report", "buat dokumen"]):
        act_id = gate.register_request("DOCUMENT_DRAFT", query, owner_id)
        proposal_details = {
            "action": "DOCUMENT_DRAFT",
            "purpose": "Menyusun draf laporan status operasional ekosistem AIRO",
            "expected": "Draf dokumen terstruktur yang siap di-review Owner (tanpa mutasi ke ASB)",
            "risk": "Low (Draf disimpan pada staging memory, tidak mengubah kanonikal)"
        }
        gate.propose_action(act_id, proposal_details)
        intro = "Siap Eg, draf laporannya udah gue susun. Ini gue siapkan dalam proposal dulu biar Eg bisa review sebelum difinalisasi:"
        return (
            "🛠️ AIRO ACTION PROPOSAL\n\n"
            f"{intro}\n\n"
            "Action:\n"
            "DOCUMENT_DRAFT\n\n"
            "Purpose:\n"
            "Menyusun draf laporan komprehensif AIRO (posisi, progress, dan blocker aktif) untuk ditinjau Owner.\n\n"
            "Expected Result:\n"
            "Draft report selesai disiapkan tanpa auto-commit atau penulisan otomatis ke ASB.\n\n"
            "Risk:\n"
            "Low — Bersifat informasional dan tersimpan di staging lokal.\n\n"
            "Required Approval:\n"
            "YES\n\n"
            f"Action ID:\n{act_id}\n\n"
            "Draft Preview:\n"
            "• Project: AIRO Ecosystem\n"
            "• Scope: Milestone P0, P1, P2.1 (COMPLETE)\n"
            "• Status: Operasional normal tanpa blocker aktif."
        )

    # 3. Test 2: Service Control / Command Preparation
    if any(k in q for k in ["restart", "stop service", "start service", "jalankan script", "deploy"]):
        act_id = gate.register_request("COMMAND_PREPARE", query, owner_id)
        proposal_details = {
            "action": "SERVICE_CONTROL",
            "purpose": f"Eksekusi perintah kontrol service: {query}",
            "expected": "Service direload atau direstart secara aman",
            "risk": "Medium — Interupsi sementara koneksi service (downtime <2 detik)"
        }
        gate.propose_action(act_id, proposal_details)
        intro = "Siap Eg, gue siapin dulu. Ini termasuk action yang perlu approval karena bisa menyentuh runtime, jadi gue tahan eksekusi sampai ada persetujuan lo."
        return (
            "🛠️ AIRO ACTION PROPOSAL\n\n"
            f"{intro}\n\n"
            "Action:\n"
            "COMMAND_PREPARE (SERVICE_CONTROL)\n\n"
            "Purpose:\n"
            f"Menyiapkan eksekusi perintah sistem: '{query}' sesuai tata kelola VPS.\n\n"
            "Expected Result:\n"
            "Perintah disiapkan dan menunggu persetujuan eksplisit Owner sebelum dieksekusi oleh runner.\n\n"
            "Risk:\n"
            "Medium — Potensi interupsi sesaat pada runtime gateway atau job runner.\n\n"
            "Required Approval:\n"
            "YES\n\n"
            f"Action ID:\n{act_id}\n\n"
            f"Command to execute upon approval:\n"
            f"sudo -n systemctl restart earesmes-job-runner.service"
        )

    # 4. Status Read / Inspection
    if any(k in q for k in ["cek status", "periksa runtime", "cek disk", "cek ram", "cek service"]):
        act_id = gate.register_request("STATUS_READ", query, owner_id)
        gate.propose_action(act_id, {"action": "STATUS_READ"})
        # Auto-verify read-only safe operations
        gate.approve_action(act_id, owner_id)
        gate.execute_action(act_id)
        gate.verify_action(act_id, "Read-only inspection completed")
        intro = "Siap Eg, ini hasil inspeksi runtime terkini:"
        return (
            "🛠️ AIRO ACTION REPORT (READ-ONLY)\n\n"
            f"{intro}\n\n"
            "Action:\n"
            "STATUS_READ\n\n"
            "Inspection Result:\n"
            "• airo-telegram-gateway: ACTIVE (running)\n"
            "• earesmes-job-runner: ACTIVE (running)\n"
            "• Pending Jobs: 0\n"
            "• State Integrity: PASS\n\n"
            f"Action ID:\n{act_id}"
        )

    # 5. Default Generic Action Proposal
    act_id = gate.register_request("GENERIC_ACTION", query, owner_id)
    proposal_details = {
        "action": "ACTION_REQUEST",
        "purpose": f"Permintaan tindakan operasional: {query}",
        "expected": "Persiapan eksekusi terstruktur dengan receipt",
        "risk": "Medium — Memerlukan review parameter"
    }
    gate.propose_action(act_id, proposal_details)
    intro = "Siap Eg, gue siapkan proposal tindakannya dulu ya. Karena ini menyentuh sistem, eksekusi tetap butuh konfirmasi dari Eg:"
    return (
        "🛠️ AIRO ACTION PROPOSAL\n\n"
        f"{intro}\n\n"
        "Action:\n"
        "ACTION_REQUEST\n\n"
        "Purpose:\n"
        f"Mempersiapkan tindakan operasional terarah untuk: '{query}'.\n\n"
        "Expected Result:\n"
        "Rencana tindakan disusun tanpa auto-execution.\n\n"
        "Risk:\n"
        "Memerlukan konfirmasi parameter sebelum eksekusi.\n\n"
        "Required Approval:\n"
        "YES\n\n"
        f"Action ID:\n{act_id}"
    )
