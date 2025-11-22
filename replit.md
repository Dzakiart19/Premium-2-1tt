# Bot Telegram untuk Facebook Scraping & Cracking

## Overview

Proyek ini adalah bot Telegram yang dirancang untuk melakukan scraping dan cracking akun Facebook menggunakan metode EXACT dari repositori `fanky86/Premium`. Bot ini mencakup dump ID publik, crack ID publik, crack dari dump file, dan dashboard real-time di Telegram. Bot ini dikembangkan agar production-ready dan sangat dioptimalkan untuk kinerja.

**Status:** ✅ Bot aktif dan berjalan - @CliperttBot  
**Update Terakhir:** November 22, 2025 - Struktur file dipindahkan ke root directory

## User Preferences

- **Bahasa:** Bahasa Indonesia (WAJIB)
- **Style:** Copy EXACT dari run.py yang working di termux
- **Dashboard:** Realtime update seperti log terminal
- **Testing:** Harus test dengan data real dari user
- **Perintah:** Jangan membuat perubahan pada `run.py`. Jangan membuat perubahan pada metode exact di `core/auth.py`, `core/dumper.py`, `core/cracker.py`.
- **Security:** JANGAN PERNAH hardcode credentials (cookie/token) di kode atau dokumentasi. Semua credentials harus input runtime atau encrypted.

## System Architecture

**UI/UX Decisions:**
- **Dashboard Realtime:** Menampilkan progress visual dengan progress bar, statistik live (Success, CP, Failed), kecepatan pemrosesan (ID/s), dan estimasi waktu selesai (ETA), diperbarui setiap 2 detik.
- **Komunikasi Telegram:** Interaksi bot sepenuhnya melalui perintah Telegram seperti `/login`, `/menu`, `/crack_publik`, `/dump_publik`, `/crack_dump`, `/hasil`, `/status`, `/reset`, `/info`, `/method`, dan `/help`.
- **Output Hasil:** Hasil crack (OK dan CP) disimpan secara lokal dalam file di folder terpisah (`OK/` dan `CP/`) dan dapat dilihat melalui perintah `/hasil`.

**Project Structure:**
```
/
├── core/                # Modul inti (auth, cracker, dumper, utils)
├── CP/                  # Folder hasil crack checkpoint
├── OK/                  # Folder hasil crack berhasil
├── data/                # Folder data dump
├── telegram_bot.py      # Main bot Telegram (entry point)
├── telegram_integration.py  # Integrasi Telegram dengan core
├── run.py              # Script console (legacy)
└── pyproject.toml      # Dependencies
```

**Technical Implementations:**
- **Login:** Menggunakan cookie Facebook untuk login dan secara otomatis mengekstrak access token dengan metode adsmanager (exact dari `run.py` line 927-933). Cookie disimpan per-session dan dienkripsi SHA256 untuk persistensi.
- **Dump ID Publik:** Mengambil ID teman dari target publik menggunakan Graph API (exact dari `run.py` line 1184-1187) dengan dukungan paginasi dan penyimpanan otomatis ke file `.txt`.
- **Cracking:** Mengimplementasikan tiga metode cracking (exact dari `run.py`):
    - **Mobile API (fanky_api):** Menggunakan `https://api.facebook.com/restserver.php` (paling stabil).
    - **B-API (fanky_b_api):** Menggunakan `https://b-api.facebook.com/method/auth.login` (metode lama, sebagai cadangan).
    - **Graph API (fankygraphv1):** Menggunakan `https://graph.facebook.com/auth/login` (alternatif dengan penanganan rate limit).
- **Password Generator:** Ditingkatkan dengan 120+ kombinasi yang mencakup nama+tahun, nama+simbol, password umum Indonesia dan global, serta variasi case.
- **Optimasi Cracker:** Termasuk auto-retry (2x), penanganan error yang lebih baik, delay yang dioptimalkan (0.3-0.6s), auto-fallback ke metode MOBILE, dan timeout 20s.
- **Session Management:** Persistensi sesi dengan enkripsi SHA256 untuk cookie, auto-save dan restore sesi, serta validasi token otomatis. Sesi disimpan dalam `sessions/user_{id}.session`.
- **Penanganan Cookie:** Implementasi `CookieParser` terpadu di `core/utils.py` untuk parsing dan validasi cookie yang konsisten di seluruh modul.
- **Multi-threading:** Menggunakan `ThreadPoolExecutor` dengan 30 worker untuk pemrosesan paralel, dengan adaptive rate limiting dan operasi thread-safe.

**Fitur Spesifikasi:**
- **Login:** `/login` dengan input cookie.
- **Crack ID Publik:** `/crack_publik` (membutuhkan ID target).
- **Dump ID Publik:** `/dump_publik` (membutuhkan ID target atau 'me').
- **Crack dari Dump:** `/crack_dump` (membutuhkan nama file dump).
- **Lihat Hasil:** `/hasil` untuk melihat akun OK dan CP.
- **Informasi Bot:** `/info` menampilkan detail kinerja.
- **Pilih Metode Crack:** `/method` untuk memilih antara MOBILE/B-API/GRAPH.
- **Status Sesi:** `/status` menampilkan info sesi (cookie, token, ukuran file).
- **Reset Sesi:** `/reset` untuk menghapus data sesi.

## External Dependencies

- **Telegram Bot API:** Untuk integrasi dengan platform Telegram.
- **Facebook Graph API:** Digunakan untuk dump ID publik.
- **Facebook Mobile API (`api.facebook.com`):** Endpoint utama untuk cracking.
- **Facebook B-API (`b-api.facebook.com`):** Endpoint cadangan untuk cracking.