# AIRO Finance — Sprint 7D Real Email Source Setup Design

Date: 2026-05-27 Asia/Jakarta
Scope: Sprint 7D Real Email Source Setup Manual Config Only
Mode: design-only / manual-config-only
Deploy performed: false

## Roadmap position

Sprint 0A: closed
Sprint 0B: done
Sprint 1: closed
Sprint 2: closed
Sprint 3: closed
Sprint 4: closed / live pass
Sprint 5: core live pass
Sprint 6: dashboard live pass recorded
Sprint 6B: closed
Sprint 7: Email Ingestion active / default OFF
Sprint 7B: Email Sandbox Fixture Matrix closed
Sprint 7C: Synthetic Candidate Simulation closed
Sprint 7D: Real Email Source Setup active

## Purpose

Sprint 7D records the real email source configuration safely before any live Gmail read or trigger is allowed.
All configurations are recorded manually. No automated connection or fetching is configured.

## Configuration Details

### 1. Provider/Source: Blu
* **Sender Allowlist**: `receipts@blubybcadigital.id`
* **Gmail Label**: `Info Terbaru`
* **Transaction Types**:
  * `transfer masuk`
  * `transfer keluar`
  * `refund`
  * `e-wallet payment`
* **Account Mapping**: `Blu` -> `Blu`
* **Safe Subject Examples**:
  * `Transaksimu Pakai blu Berhasil`
  * `Info Transaksi Masuk ke blu Kamu 💸`

### 2. Provider/Source: Tokopedia Card
* **Sender Allowlist**: `noreply@tokopedia.com`
* **Gmail Label**: `Info Terbaru`
* **Transaction Types**:
  * `kartu kredit purchase`
  * `pembayaran kartu kredit`
  * `refund`
* **Account Mapping**: `Tokopedia Card last4 2003` -> `Tokopedia Card`
* **Safe Subject Examples**:
  * `Selamat, Bayar Otomatis Air PDAM anda berhasil`
  * `Selamat, pembayaran tagihan Kartu Kredit Anda BERHASIL`

## Global Safety Contract & Guardrails

Required invariant:
* **Email Ingestion Enabled**: false
* **Email default OFF**: true
* **Dry-run only**: true
* **Gmail Live Read**: forbidden (No Gmail live read performed)
* **Mailbox Read**: forbidden (No mailbox read performed)
* **Gmail Trigger Install**: forbidden (No Gmail/mail trigger created)
* **Email Modification**: forbidden (No email modified)
* **Full Email Body Storage**: forbidden (No full email body stored)
* **OTP/Security Parsing/Forwarding**: forbidden (No OTP/security parsing/forwarding)
* **Raw Email Forwarding**: forbidden (No raw email forwarding to Telegram)
* **Finance Write**: forbidden (No finance write performed)
* **Ledger / Event / Queue Write**: forbidden (No Account Ledger, Finance Events, Review Queue, or domain tab write from email)

## Conclusion

This phase establishes the trusted sender configurations and pattern inputs manually. Real integration and read operations are deferred to Sprint 7E.

RESULT=PASS_SPRINT7D_REAL_EMAIL_SOURCE_SETUP_DESIGN_RECORDED
NEXT=sprint7d_real_email_source_setup_phase_closeout
