# 🔒 PANDUAN KEAMANAN

## ⚠️ PERINGATAN PENTING

Bot ini menangani data sensitif seperti cookie dan token Facebook. **SANGAT PENTING** untuk mengikuti panduan keamanan ini.

---

## 🛡️ Best Practices

### 1. Jangan Pernah Share Credentials
- ❌ Jangan share cookie Facebook Anda dengan siapapun
- ❌ Jangan simpan cookie di file text biasa
- ❌ Jangan commit cookie/token ke Git
- ❌ Jangan screenshot cookie/token
- ❌ Jangan posting cookie di forum/chat

### 2. Session Management
- ✅ Bot menggunakan enkripsi SHA256 untuk session
- ✅ Session auto-expire setelah 7 hari
- ✅ Gunakan `/reset` untuk logout
- ✅ Credentials hanya di-store di memory & encrypted file

### 3. Bot Telegram
- ✅ Setiap user punya session terpisah
- ✅ Data tidak di-share antar users
- ✅ Bot tidak menyimpan password
- ✅ Hasil crack hanya visible untuk user masing-masing

### 4. Testing
- ✅ Test file TIDAK boleh hardcode credentials
- ✅ Gunakan input runtime untuk cookie/token
- ✅ REDACT credentials di dokumentasi
- ✅ Clean credentials dari git history

---

## 🚨 Apa yang TIDAK Boleh Dilakukan

### JANGAN:
1. **Hardcode cookie/token di kode**
   ```python
   # ❌ JANGAN SEPERTI INI
   COOKIE = "datr=xxx; c_user=123; xs=abc"
   
   # ✅ LAKUKAN SEPERTI INI
   COOKIE = input("Masukkan cookie: ")
   ```

2. **Commit credentials ke Git**
   - Selalu check file sebelum commit
   - Gunakan `.gitignore` untuk file sensitif
   - Clean git history jika ter-commit

3. **Share hasil crack dengan info lengkap**
   - Jangan share ID|Password|Cookie|Token
   - Redact data sensitif saat share screenshot
   - Hanya share statistik jika perlu

4. **Gunakan bot untuk illegal activity**
   - Hanya gunakan untuk akun sendiri
   - Atau dengan izin eksplisit dari pemilik
   - Unauthorized access adalah ILLEGAL

---

## 📁 File yang Harus Di-ignore

Tambahkan ke `.gitignore`:
```
# Credentials & Sessions
.fancookie.txt
.fantoken.txt
sessions/
*.session

# Test data sensitif
test_real_data.py
my_cookie.txt

# Hasil crack
OK/
CP/
data/dump_*.txt

# Logs
/tmp/logs/
*.log
```

---

## 🔐 Cara Aman Menggunakan Bot

### Via Telegram (Recommended)
1. Chat langsung dengan bot @CliperttBot
2. Gunakan `/login` dan paste cookie
3. Bot akan encrypt & store session
4. Session auto-expire, tidak perlu manual cleanup
5. Gunakan `/reset` jika ingin logout manual

### Via Python Script (Advanced)
1. Jangan hardcode credentials
2. Gunakan input() atau environment variables
3. Clean credentials setelah selesai
4. Tidak commit test file dengan credentials

---

## ⚠️ Jika Credentials Ter-expose

### Langkah Segera:
1. **Ganti password Facebook** SEGERA
2. **Logout semua device** di Facebook settings
3. **Enable 2FA** untuk extra security
4. **Clean git history** jika ter-commit:
   ```bash
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch FILE_WITH_CREDENTIALS" \
   --prune-empty --tag-name-filter cat -- --all
   ```
5. **Force push** (jika sudah di-push):
   ```bash
   git push origin --force --all
   ```

### Untuk Bot Developer:
1. Revoke semua tokens di Facebook Developer
2. Generate token baru
3. Update bot dengan token baru
4. Notify users untuk re-login

---

## 📊 Security Checklist

Sebelum commit/deploy, pastikan:

- [ ] Tidak ada hardcoded cookie/token
- [ ] Test files menggunakan input runtime
- [ ] Dokumentasi tidak expose credentials
- [ ] `.gitignore` sudah mencakup file sensitif
- [ ] Session files di-encrypt
- [ ] Logs tidak contain credentials
- [ ] Screenshots di-redact
- [ ] README tidak contain example credentials

---

## 🛡️ Technical Security Measures

Bot ini sudah implement:

### 1. Session Encryption
```python
# Cookie di-encrypt dengan SHA256
hash_object = hashlib.sha256(cookie.encode())
encrypted_cookie = hash_object.hexdigest()
```

### 2. No File Storage (by default)
- Credentials di-store di memory (UserSession)
- Optional: encrypted session file dengan auto-expire
- Tidak ada plain text cookie di disk

### 3. Session Isolation
- Setiap user punya session terpisah
- User A tidak bisa akses session User B
- Thread-safe operations

### 4. Auto-cleanup
- Session expire setelah 7 hari
- Auto-delete expired sessions
- No lingering credentials

---

## 📞 Reporting Security Issues

Jika menemukan security vulnerability:

1. **JANGAN** post di public issue
2. Contact developer via private message
3. Provide details (tanpa expose credentials)
4. Wait untuk patch sebelum disclose

---

## ⚖️ Legal Disclaimer

- Bot ini untuk **educational purposes** only
- Unauthorized access adalah **ILLEGAL**
- Developer tidak bertanggung jawab atas penyalahgunaan
- Gunakan dengan **BIJAK** dan **BERTANGGUNG JAWAB**

---

**Remember:** 
> *"With great power comes great responsibility"*

Gunakan bot ini dengan bijak dan selalu prioritaskan keamanan! 🙏

---

*Last updated: 22 November 2025*
