# 🤖 Bot Telegram Crack Facebook

Bot Telegram untuk dump ID Facebook dan crack account. Adaptasi dari [fanky86/Premium](https://github.com/fanky86/Premium) yang original untuk Termux.

## ⚠️ DISCLAIMER PENTING

**PERINGATAN:**
- ⚖️ **Educational Only** - Hanya untuk tujuan edukasi
- 🚫 **Ilegal jika Disalahgunakan** - Akses unauthorized adalah ILEGAL
- ⏰ **API Deprecated (2025)** - Metode crack sudah outdated, success rate rendah
- 👤 **Tanggung Jawab User** - Anda bertanggung jawab penuh atas penggunaan bot ini

**REALITAS 2025:**
- ❌ Crack methods sebagian besar di-block Facebook
- ⚠️ Dump ID butuh token valid dengan permission
- ✅ Error messages jelas dalam Bahasa Indonesia

## 🚀 Fitur

1. **Login dengan Cookie** - Auto-extract token (5 metode)
2. **Dump ID Publik** - Dari target atau teman sendiri
3. **Crack ID** - 3 metode (deprecated tapi tersedia)
4. **Lihat Hasil** - Browse hasil OK dan CP
5. **Dashboard Realtime** - Progress update seperti log termux

## 📋 Cara Pakai

### 1. Setup Bot

Di Replit (sudah auto-setup):
```bash
# Set token bot di Secrets atau:
export TELEGRAM_BOT_TOKEN='token_dari_botfather'

# Run bot (atau klik Run button):
python telegram_bot.py
```

### 2. Login ke Bot

1. Buka bot Telegram Anda
2. `/start` - Mulai bot
3. `/login` - Login dengan cookie Facebook
4. Kirim cookie (format: `c_user=123; xs=abc; ...`)

**Cara dapat cookie:**
- Buka facebook.com di browser
- F12 → Application → Cookies
- Copy semua cookies

### 3. Dump ID

1. `/menu` → Dump ID Publik
2. Kirim ID target (atau `me` untuk teman sendiri)
3. Tunggu proses selesai
4. Pilih metode crack (opsional)

### 4. Lihat Hasil

1. `/hasil` atau via menu
2. Pilih OK atau CP
3. Browse files hasil

## 🏗️ Struktur

```
├── core/                    # Modul inti
│   ├── auth.py             # Login & token (5 metode)
│   ├── dumper.py           # Dump ID (Graph API)
│   ├── cracker.py          # Crack (deprecated methods)
│   └── telegram_dashboard.py  # Dashboard realtime
├── telegram_bot.py         # Main bot
├── OK/                     # Hasil crack sukses
├── CP/                     # Hasil checkpoint
└── data/                   # File dump
```

## 🐛 Troubleshooting

**Login Gagal:**
- Cookie expired → Dapatkan cookie baru
- Token tidak found → Login ulang

**Dump Gagal:**
- "Token expired" → `/login` ulang
- "No permission" → Token tidak punya akses
- "Target invalid" → ID salah atau private

**Crack Tidak Hasil:**
- **NORMAL DI 2025** - API deprecated
- Facebook block request
- Password tidak weak / ada 2FA

## 💡 Tips

✅ **DO:**
- Gunakan cookie fresh (<1 hari)
- Pilih target publik
- Baca error message (sudah jelas)
- Focus ke dump ID (skip crack)

❌ **DON'T:**
- Gunakan akun utama
- Share cookie/token
- Spam request
- Expect crack work di 2025

## 📞 Credits

- **Original:** [fanky86/Premium](https://github.com/fanky86/Premium)
- **Platform:** Termux → Telegram Bot
- **Bahasa:** Indonesia

---

**INGAT:** Gunakan dengan bijak! Author tidak bertanggung jawab atas penyalahgunaan.
