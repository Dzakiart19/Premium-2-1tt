# 📋 Panduan Test Bot Telegram Crack Facebook

## ✅ Status Perbaikan
**Tanggal:** 22 November 2025

### Masalah yang Diperbaiki:
1. ✅ Command `/crack_publik` - Handler ditambahkan
2. ✅ Command `/dump_publik` - Handler ditambahkan  
3. ✅ Command `/crack_dump` - Handler ditambahkan
4. ✅ Command `/hasil` - Handler ditambahkan

### Yang Ditambahkan:
- 4 Command handlers baru di `telegram_bot.py`
- Registrasi command di fungsi `main()`
- Validasi login sebelum eksekusi command
- State management untuk setiap command

---

## 🧪 Langkah Test

### 1️⃣ Test Login
```
Kirim: /login
Bot meminta cookie
Kirim cookie yang diberikan user
```

**Cookie yang diberikan:**
```
dbln=%7B%22100023449360931%22%3A%22VG56uyjD%22%2C%2261583843228443%22%3A%22fPOY5Jyk%22%7D; sb=-1sdadTuYQAS1RJL4Zr-RkZs; ps_l=1; ps_n=1; dpr=2.673030376434326; locale=id_ID; datr=jk0eaSuT60mOUzhTIRrh6TMC; pas=61583843228443%3APpfCvpKTmQ; vpd=v1%3B1002x502x2.4312500953674316; wl_cbv=v2%3Bclient_version%3A2991%3Btimestamp%3A1763787674; c_user=100023449360931; wd=891x1779; fr=1AzJUZ2ihbORdvqiK.AWdk6nI5k5OOC8uaE7Bwjzrqvbmrmi2p_dWBFz8VPn2TU7PB8G4.BpIeFU..AAA.0.0.BpIeFU.AWdG0FnIPHJNauhMm6R7tE11XJ0; xs=35%3AM7eLT4CupP467g%3A2%3A1763788618%3A-1%3A-1%3A%3AAczGWRLvj0fZDA9IMoV7SdWpI1gQWL4K7p_RB2VMVw; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1763828054270%2C%22v%22%3A1%7D
```

**Expected:**
- ✅ Login berhasil
- ✅ Token ditemukan
- ✅ Cookie tersimpan

---

### 2️⃣ Test Command /crack_publik
```
Kirim: /crack_publik
Bot meminta ID target
Kirim ID: 100028074584110
```

**Expected:**
- ✅ Bot mulai dump ID dari target
- ✅ Dashboard real-time muncul
- ✅ Pilihan metode crack muncul setelah dump selesai

---

### 3️⃣ Test Command /dump_publik  
```
Kirim: /dump_publik
Bot meminta ID target
Kirim ID: 100028074584110
```

**Expected:**
- ✅ Bot mulai dump ID
- ✅ Dashboard real-time muncul
- ✅ File tersimpan di folder `data/`

---

### 4️⃣ Test Command /crack_dump
```
Kirim: /crack_dump
Bot meminta nama file
Kirim: hasil_dump.txt (atau nama file yang ada)
```

**Expected:**
- ✅ Bot load file dari folder `data/`
- ✅ Pilihan metode crack muncul
- ✅ Crack dimulai setelah pilih metode

---

### 5️⃣ Test Command /hasil
```
Kirim: /hasil
Bot menampilkan pilihan OK atau CP
Pilih salah satu
```

**Expected:**
- ✅ Bot menampilkan list file hasil
- ✅ Jumlah akun per file ditampilkan

---

## 🔍 Test Via Menu (Alternative)

Semua command juga bisa diakses via:
```
/menu → Pilih button yang sesuai
```

**Menu Button:**
- 🎯 Crack ID Publik → sama dengan `/crack_publik`
- 📥 Dump ID Publik → sama dengan `/dump_publik`
- 🔨 Crack dari Dump → sama dengan `/crack_dump`
- 📊 Lihat Hasil → sama dengan `/hasil`

---

## 📊 Command Lain untuk Test

```
/status   → Cek status sesi (login, cookie, token)
/method   → Pilih metode crack (MOBILE/B-API/GRAPH)
/reset    → Reset sesi jika ada masalah
/help     → Bantuan lengkap
/info     → Info bot
```

---

## ⚙️ Technical Details

### Bot Username
```
@CliperttBot
```

### Workflow Status
```
✅ RUNNING
```

### File Structure
```
├── OK/          # Hasil crack sukses
├── CP/          # Hasil checkpoint  
├── data/        # File dump ID
└── sessions/    # Session files (auto)
```

### Command Handlers Registered
```python
✅ /start
✅ /help
✅ /menu
✅ /status
✅ /reset
✅ /login
✅ /info
✅ /method
✅ /crack_publik   ← BARU
✅ /dump_publik    ← BARU
✅ /crack_dump     ← BARU
✅ /hasil          ← BARU
```

---

## 🔐 Security Notes

- Cookie disimpan di memory (UserSession)
- Session file otomatis dibuat di `sessions/`
- Session expired setelah 30 hari
- Auto-restore session saat bot restart
- No logging untuk cookie/token

---

## ❗ Troubleshooting

### Jika command tidak merespon:
1. Check status bot: `/status`
2. Restart session: `/reset`
3. Login ulang: `/login`

### Jika dump gagal:
- Pastikan ID target publik
- Atau gunakan 'me' untuk dump teman sendiri

### Jika crack gagal:
- Pastikan ada file dump di folder `data/`
- Coba metode lain: `/method`

---

## 🎯 Test ID dari User

**ID untuk test:**
```
100028074584110
```

**Cookie untuk login:**
```
(Sudah diberikan di atas)
```

---

**Status:** ✅ Semua command sudah diperbaiki dan siap test!
