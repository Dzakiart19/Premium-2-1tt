# 📁 STRUKTUR PROJECT - BOT TELEGRAM FACEBOOK CRACK

## ✅ Struktur File Baru (Root Directory)

```
/
├── 📁 core/                       # Modul inti aplikasi
│   ├── __init__.py
│   ├── auth.py                    # Autentikasi Facebook
│   ├── cracker.py                 # Engine crack Facebook
│   ├── dumper.py                  # Dump ID publik
│   ├── dashboard.py               # Dashboard console
│   ├── telegram_dashboard.py      # Dashboard Telegram
│   ├── session_manager.py         # Manajemen sesi user
│   └── utils.py                   # Utilities (parser, generator)
│
├── 📁 CP/                         # Hasil crack checkpoint
├── 📁 OK/                         # Hasil crack berhasil
├── 📁 data/                       # Data dump ID
│
├── 📄 telegram_bot.py             # ⭐ MAIN BOT TELEGRAM
├── 📄 telegram_integration.py     # Integrasi Telegram-Core
├── 📄 run.py                      # Script console (legacy)
│
├── 📄 pyproject.toml              # Dependencies Python
├── 📄 requirements.txt            # Requirements file
├── 📄 uv.lock                     # Lock file dependencies
│
├── 📄 README.md                   # Dokumentasi utama
├── 📄 replit.md                   # Dokumentasi Replit
├── 📄 PANDUAN_TEST_BOT.md         # Panduan testing bot
└── 📄 PANDUAN_TEST.md             # Panduan testing lainnya
```

## 🚀 Entry Point

**Main File:** `telegram_bot.py`

**Workflow Replit:**
```bash
python telegram_bot.py
```

## 📦 Core Modules

### 1. **core/auth.py**
- Login dengan cookie Facebook
- Extract access token otomatis
- Validasi cookie

### 2. **core/dumper.py**
- Dump ID dari target publik
- Dump teman sendiri ('me')
- Graph API v22.0

### 3. **core/cracker.py**
- Metode: Mobile, B-API, Graph
- Multi-threading (30 workers)
- Auto-retry & fallback

### 4. **core/dashboard.py**
- Dashboard console real-time
- Progress bar & statistik

### 5. **core/telegram_dashboard.py**
- Dashboard Telegram real-time
- Update progress otomatis

### 6. **core/session_manager.py**
- Simpan/restore session
- Enkripsi SHA256

### 7. **core/utils.py**
- CookieParser
- PasswordGenerator
- UserAgentGenerator

## 📂 Folder Hasil

### **CP/** - Checkpoint
File format: `ID|PASSWORD|NAMA`

### **OK/** - Berhasil
File format: `ID|PASSWORD|NAMA`

### **data/** - Dump ID
File format: `ID|NAMA`

## 🔧 Workflow

```
1. User → /login (cookie)
2. Bot → Extract token
3. User → /dump_publik (ID target)
4. Bot → Dump ID dari Graph API
5. User → /crack_dump
6. Bot → Crack semua ID
7. Bot → Save hasil ke OK/CP
8. User → /hasil (lihat hasil)
```

## ⚙️ Dependencies

```toml
[project.dependencies]
python-telegram-bot >= 20.0
requests >= 2.31.0
beautifulsoup4 >= 4.12.0
rich >= 13.0.0
```

## 🌐 Bot Telegram

**Username:** @CliperttBot  
**Status:** ✅ Aktif dan Running

**Commands:**
- `/start` - Mulai bot
- `/login` - Login Facebook
- `/dump_publik` - Dump ID publik
- `/crack_publik` - Crack ID publik
- `/crack_dump` - Crack dari dump
- `/hasil` - Lihat hasil
- `/status` - Status session
- `/reset` - Reset session
- `/method` - Ganti metode
- `/info` - Info bot
- `/help` - Bantuan

## 📝 Catatan

- Semua file sudah dipindahkan dari `Premium-2-1t/` ke root directory
- Workflow sudah diupdate ke `python telegram_bot.py`
- Bot langsung berjalan dari root directory
- Tidak ada subfolder Premium-2-1t lagi

## ✨ Update Terakhir

**Tanggal:** November 22, 2025  
**Perubahan:**
- ✅ Pindah semua file ke root directory
- ✅ Update workflow path
- ✅ Hapus folder Premium-2-1t
- ✅ Bersihkan file zip & test
- ✅ Bot running di root directory
