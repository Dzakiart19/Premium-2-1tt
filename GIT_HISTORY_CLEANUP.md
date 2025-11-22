# ⚠️ PENTING: GIT HISTORY CLEANUP REQUIRED

## 🚨 CRITICAL SECURITY ISSUE

Credentials (cookie dan token) Facebook pernah di-commit ke repository ini dan masih ada di **git history**. Meskipun file sudah dibersihkan, credentials masih bisa diakses melalui git log.

## 📋 Status Saat Ini

✅ **File Source Code:** CLEAN (tidak ada hardcoded credentials)  
✅ **Dokumentasi:** CLEAN (semua credentials di-REDACT)  
✅ **Test Files:** CLEAN (menggunakan input runtime)  
❌ **Git History:** MASIH MENGANDUNG CREDENTIALS

## 🔧 Cara Membersihkan Git History

### ⚠️ WARNING
- Operasi ini akan **MENGUBAH** git history
- Semua collaborators harus **FORCE PULL** setelah cleanup
- Repository yang sudah di-fork perlu **RE-FORK**
- **BACKUP** repository sebelum melanjutkan

### Option 1: Menggunakan BFG Repo-Cleaner (Recommended)

```bash
# 1. Install BFG (https://rtyley.github.io/bfg-repo-cleaner/)
# Untuk macOS: brew install bfg
# Untuk Linux: Download .jar dari website

# 2. Backup repository
git clone --mirror https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO.git

# 3. Buat file dengan credentials yang akan dihapus
cat > credentials.txt << 'EOF'
c_user=YOUR_USER_ID_HERE
xs=YOUR_SESSION_TOKEN_HERE
EAA[A-Za-z0-9]+
datr=
EOF

# 4. Jalankan BFG
bfg --replace-text credentials.txt

# 5. Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 6. Push (DANGER!)
git push --force
```

### Option 2: Menggunakan git filter-branch

```bash
# 1. Backup repository
git clone YOUR_REPO backup-repo
cd YOUR_REPO

# 2. Filter branch - hapus file test yang pernah contain credentials
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch test_dengan_data_user.py" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Clean references
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 4. Push (DANGER!)
git push origin --force --all
git push origin --force --tags
```

### Option 3: Nuclear Option - Start Fresh

Jika repository ini tidak penting historynya:

```bash
# 1. Hapus folder .git
rm -rf .git

# 2. Init repo baru
git init
git add .
git commit -m "Initial commit (cleaned)"

# 3. Force push ke remote
git remote add origin YOUR_REPO_URL
git push -u origin main --force
```

## 📊 Verifikasi Cleanup

Setelah cleanup, verify bahwa credentials sudah hilang:

```bash
# Search untuk c_user (part dari cookie)
git log --all --full-history -- "*" | grep -i "c_user="

# Search untuk token pattern  
git log --all --full-history -- "*" | grep -i "EAA"

# Search untuk datr (cookie component)
git log --all --full-history -- "*" | grep -i "datr="
```

**Jika masih muncul hasil, ulangi cleanup!**

## 🔐 After Cleanup

### 1. Ganti Credentials
- ✅ Ganti password Facebook
- ✅ Logout semua devices di Facebook
- ✅ Enable 2FA
- ✅ Revoke old tokens

### 2. Notify Collaborators
```bash
# Semua collaborators harus:
git fetch origin
git reset --hard origin/main  # DANGER: Hapus local changes!
```

### 3. Re-fork (jika ada)
- Hapus semua forks
- Fork ulang dari clean repository

## 📝 Prevention

Untuk mencegah terulang:

### 1. Setup Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check untuk credentials
if git diff --cached | grep -iE "datr=|c_user=|xs=|EAA[A-Z]"; then
    echo "❌ ERROR: Credentials detected in commit!"
    echo "Please remove credentials before committing."
    exit 1
fi
```

```bash
chmod +x .git/hooks/pre-commit
```

### 2. Use git-secrets

```bash
# Install
brew install git-secrets  # macOS
apt-get install git-secrets  # Ubuntu

# Setup
git secrets --install
git secrets --register-aws
git secrets --add 'datr='
git secrets --add 'c_user='
git secrets --add 'xs='
git secrets --add 'EAA[A-Z][A-Za-z0-9]+'
```

### 3. Environment Variables

Gunakan environment variables untuk credentials:

```python
import os

# ❌ JANGAN
COOKIE = "datr=xxx; c_user=123..."

# ✅ LAKUKAN
COOKIE = os.getenv("FB_COOKIE")
if not COOKIE:
    COOKIE = input("Masukkan cookie: ")
```

## 🆘 Jika Sudah Terlanjur Public

Jika repository sudah public dan credentials ter-expose:

1. **SEGERA ganti password** (paling penting!)
2. **Make repository private** temporarily
3. **Clean git history** (langkah di atas)
4. **Verify cleanup** (tidak ada credentials tersisa)
5. **Make public again** (jika perlu)

## 📞 Need Help?

Jika tidak yakin atau butuh bantuan:
- Baca: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- Contact: GitHub Support untuk sensitive data removal

---

## ✅ Checklist

Sebelum menganggap selesai:

- [ ] Git history sudah di-clean
- [ ] Verifikasi tidak ada credentials (git log search)
- [ ] Password Facebook sudah diganti
- [ ] 2FA enabled
- [ ] Old tokens revoked
- [ ] Collaborators notified
- [ ] Pre-commit hooks installed
- [ ] .gitignore updated
- [ ] Test dengan git log tidak ada credentials

---

**REMEMBER:** Git history is forever unless you actively remove it!

*Generated: 22 November 2025*  
*Priority: CRITICAL - DO IMMEDIATELY*
