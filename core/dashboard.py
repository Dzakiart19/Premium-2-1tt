"""
Modul dashboard realtime untuk monitoring operasi crack
Menggunakan rich console untuk tampilan yang menarik
"""

import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich import box
from datetime import datetime
from typing import Dict, Optional


class Dashboard:
    """Class untuk dashboard realtime"""
    
    def __init__(self):
        self.console = Console()
        self.live = None
        self.operation_type = ""
        self.stats = {
            'total': 0,
            'current': 0,
            'ok': 0,
            'cp': 0,
            'failed': 0,
            'progress': 0
        }
        self.start_time = None
        self.current_target = ""
        self.last_result = None
    
    def start(self, operation: str, target: str = ""):
        """
        Mulai dashboard
        
        Args:
            operation: Jenis operasi (dump/crack)
            target: Target operasi
        """
        self.operation_type = operation
        self.current_target = target
        self.start_time = datetime.now()
        self.stats = {
            'total': 0,
            'current': 0,
            'ok': 0,
            'cp': 0,
            'failed': 0,
            'progress': 0
        }
    
    def update_stats(self, stats: Dict):
        """
        Update statistik
        
        Args:
            stats: Dict statistik baru
        """
        self.stats.update(stats)
        if 'total' in stats and stats['total'] > 0:
            self.stats['progress'] = int((self.stats.get('current', 0) / stats['total']) * 100)
    
    def set_result(self, result: Dict):
        """
        Set hasil terakhir
        
        Args:
            result: Dict hasil
        """
        self.last_result = result
    
    def generate_layout(self) -> Panel:
        """
        Generate layout dashboard
        
        Returns:
            Panel dengan layout lengkap
        """
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=7)
        )
        
        header = self._generate_header()
        body = self._generate_body()
        footer = self._generate_footer()
        
        layout["header"].update(header)
        layout["body"].update(body)
        layout["footer"].update(footer)
        
        return Panel(
            layout,
            title=f"[bold cyan]🔥 FB CRACK DASHBOARD[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
    
    def _generate_header(self) -> Panel:
        """Generate header"""
        elapsed = ""
        if self.start_time:
            delta = datetime.now() - self.start_time
            elapsed = f"{delta.seconds // 60}m {delta.seconds % 60}s"
        
        header_text = Text()
        header_text.append("⚡ Operasi: ", style="bold yellow")
        header_text.append(self.operation_type.upper(), style="bold green")
        header_text.append(" | ⏱️  Waktu: ", style="bold yellow")
        header_text.append(elapsed, style="bold green")
        
        if self.current_target:
            header_text.append(" | 🎯 Target: ", style="bold yellow")
            header_text.append(self.current_target, style="bold green")
        
        return Panel(header_text, border_style="yellow")
    
    def _generate_body(self) -> Table:
        """Generate body dengan statistik"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="blue",
            box=box.ROUNDED
        )
        
        table.add_column("📊 Metric", style="cyan", width=20)
        table.add_column("📈 Value", justify="right", style="green", width=15)
        table.add_column("📉 Percentage", justify="right", style="yellow", width=15)
        
        total = self.stats.get('total', 0)
        current = self.stats.get('current', 0)
        ok = self.stats.get('ok', 0)
        cp = self.stats.get('cp', 0)
        failed = self.stats.get('failed', 0)
        
        table.add_row(
            "Total Target",
            str(total),
            "100%"
        )
        
        table.add_row(
            "Progress",
            f"{current}/{total}",
            f"{self.stats.get('progress', 0)}%"
        )
        
        table.add_row(
            "✅ Success (OK)",
            str(ok),
            f"{(ok/total*100) if total > 0 else 0:.1f}%" 
        )
        
        table.add_row(
            "⚠️  Checkpoint (CP)",
            str(cp),
            f"{(cp/total*100) if total > 0 else 0:.1f}%"
        )
        
        table.add_row(
            "❌ Failed",
            str(failed),
            f"{(failed/total*100) if total > 0 else 0:.1f}%"
        )
        
        return table
    
    def _generate_footer(self) -> Panel:
        """Generate footer dengan hasil terakhir"""
        if not self.last_result:
            footer_text = Text("⏳ Menunggu hasil...", style="italic dim")
        else:
            footer_text = Text()
            
            if self.last_result.get('type') == 'OK':
                footer_text.append("✅ SUKSES!\n", style="bold green")
                footer_text.append(f"ID: {self.last_result.get('user_id', 'N/A')}\n", style="cyan")
                footer_text.append(f"Password: {self.last_result.get('password', 'N/A')}\n", style="yellow")
                
                if 'cookie' in self.last_result:
                    cookie_preview = self.last_result['cookie'][:50] + "..." if len(self.last_result['cookie']) > 50 else self.last_result['cookie']
                    footer_text.append(f"Cookie: {cookie_preview}", style="dim")
                    
            elif self.last_result.get('type') == 'CP':
                footer_text.append("⚠️  CHECKPOINT\n", style="bold yellow")
                footer_text.append(f"ID: {self.last_result.get('user_id', 'N/A')}\n", style="cyan")
                footer_text.append(f"Password: {self.last_result.get('password', 'N/A')}", style="yellow")
        
        return Panel(footer_text, title="[bold]Hasil Terakhir[/bold]", border_style="green")
    
    def print_static(self):
        """Print dashboard static (tanpa live update)"""
        panel = self.generate_layout()
        self.console.print(panel)
    
    def print_summary(self):
        """Print summary hasil akhir"""
        table = Table(
            title="[bold cyan]📊 SUMMARY HASIL[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
            border_style="cyan",
            box=box.DOUBLE
        )
        
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Count", justify="right", style="green", width=15)
        
        table.add_row("Total Processed", str(self.stats.get('current', 0)))
        table.add_row("✅ Success (OK)", str(self.stats.get('ok', 0)))
        table.add_row("⚠️  Checkpoint (CP)", str(self.stats.get('cp', 0)))
        table.add_row("❌ Failed", str(self.stats.get('failed', 0)))
        
        elapsed = ""
        if self.start_time:
            delta = datetime.now() - self.start_time
            elapsed = f"{delta.seconds // 60}m {delta.seconds % 60}s"
        table.add_row("⏱️  Total Waktu", elapsed)
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")
