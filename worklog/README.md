# AIRO Second Brain Worklog System

- **Status:** `ACTIVE_CANONICAL_DOCUMENTATION`
- **Scope:** `ASB_GLOBAL`

---

## 1. Overview & Conceptual Model

Sistem Worklog ASB v0.6 membagi memori pekerjaan menjadi 4 lapisan utama dengan peran baby-friendly yang jelas:

1. **Session (`worklog/sessions/YYYY-MM-DD/<Project>/01 - <Title>.md`)**:  
   *"Apa yang terjadi dalam satu pekerjaan?"*  
   Merupakan rekam memori episodik permanen per sesi pekerjaan (1 sesi = 1 proyek + 1 tujuan utama).
2. **Daily (`worklog/daily/YYYY-MM-DD.md`)**:  
   *"Hari ini gue ngapain?"*  
   Merupakan tampilan navigasi harian otomatis yang tergenerasi secara deterministik dari berkas sesi harian. Daily **BUKAN** sumber kebenaran kanonis status proyek dan dapat didaur ulang kapan saja (`DAILY_IDEMPOTENT=PASS`).
3. **Project Docs (`projects/`, `docs/`, `CURRENT.md`)**:  
   *"Project sekarang posisi sebenarnya di mana?"*  
   Merupakan sumber kebenaran kanonis (*canonical source of truth*) posisi dan komitmen proyek saat ini.
4. **LLM Wiki (`wiki/`)**:  
   *"Pelajaran apa yang layak diingat?"*  
   Merupakan repositori pengetahuan dan pelajaran semantik yang dapat digunakan kembali lintas sesi.

---

> [!IMPORTANT]
> Daily dan Session history **TIDAK PERNAH** meng-override bukti kanonis status proyek saat ini yang ada pada berkas proyek atau hasil pengujian live runtime.
