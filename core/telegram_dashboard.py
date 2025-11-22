"""
Modul dashboard realtime khusus untuk Telegram
Update pesan secara berkala seperti log termux
November 2025
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Optional, Any
from telegram import Message
from telegram.error import BadRequest, TimedOut


class TelegramDashboard:
    """
    Class untuk dashboard realtime di Telegram
    Mengirim update berkala seperti log di termux
    """
    
    def __init__(self):
        self.message: Optional[Message] = None
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
        self.last_update_time = 0
        self.update_interval = 2
        self.is_running = False
    
    async def start(self, message: Message, operation: str, target: str = ""):
        """
        Mulai dashboard dengan pesan Telegram
        
        Args:
            message: Message object dari Telegram
            operation: Jenis operasi (DUMP/CRACK)
            target: Target operasi
        """
        self.message = message
        self.operation_type = operation.upper()
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
        self.last_result = None
        self.last_update_time = time.time()
        self.is_running = True
    
    async def update_stats(self, stats: Dict, force: bool = False):
        """
        Update statistik dan refresh tampilan jika perlu
        
        Args:
            stats: Dict statistik baru
            force: Force update meskipun belum waktunya
        """
        self.stats.update(stats)
        if 'total' in stats and stats['total'] > 0:
            self.stats['progress'] = int((self.stats.get('current', 0) / stats['total']) * 100)
        
        current_time = time.time()
        if force or (current_time - self.last_update_time >= self.update_interval):
            await self._refresh_display()
            self.last_update_time = current_time
    
    async def set_result(self, result: Dict, force_update: bool = True):
        """
        Set hasil terakhir dan update tampilan
        
        Args:
            result: Dict hasil crack/dump
            force_update: Update tampilan immediately
        """
        self.last_result = result
        if force_update:
            await self._refresh_display()
    
    async def _refresh_display(self):
        """Refresh tampilan dashboard di Telegram"""
        if not self.message or not self.is_running:
            return
        
        try:
            text = self._generate_display_text()
            await self.message.edit_text(text, parse_mode='HTML')
        except BadRequest as e:
            if "message is not modified" not in str(e).lower():
                pass
        except TimedOut:
            pass
        except Exception as e:
            pass
    
    def _generate_display_text(self) -> str:
        """Generate teks display untuk Telegram dengan format MODERN & GACOR"""
        elapsed = ""
        if self.start_time:
            delta = datetime.now() - self.start_time
            minutes = delta.seconds // 60
            seconds = delta.seconds % 60
            elapsed = f"{minutes}m {seconds}s"
        
        total = self.stats.get('total', 0)
        current = self.stats.get('current', 0)
        ok = self.stats.get('ok', 0)
        cp = self.stats.get('cp', 0)
        failed = self.stats.get('failed', 0)
        progress = self.stats.get('progress', 0)
        
        success_rate = 0
        if current > 0:
            success_rate = round(((ok + cp) / current) * 100, 1)
        
        speed = 0
        if self.start_time and current > 0:
            elapsed_seconds = (datetime.now() - self.start_time).total_seconds()
            if elapsed_seconds > 0:
                speed = round(current / elapsed_seconds, 1)
        
        eta = ""
        if speed > 0 and current < total:
            remaining = total - current
            eta_seconds = remaining / speed
            eta_minutes = int(eta_seconds // 60)
            eta_secs = int(eta_seconds % 60)
            eta = f"{eta_minutes}m {eta_secs}s"
        
        progress_bar = self._create_progress_bar(progress)
        
        text = f"""╔════════════════════════════════════════╗
║       <b>🔥 FB CRACK DASHBOARD 🔥</b>         ║
╠════════════════════════════════════════╣
║                                        ║
║  ⚡ <b>Operasi</b>    : {self.operation_type:<22} ║
║  ⏱ <b>Waktu</b>      : {elapsed:<22} ║"""
        
        if self.current_target:
            target_preview = self.current_target[:20] + "..." if len(self.current_target) > 20 else self.current_target
            text += f"\n║  🎯 <b>Target</b>     : {target_preview:<22} ║"
        
        text += f"""
║  🚀 <b>Kecepatan</b>  : {speed} ID/s{' ' * (19 - len(str(speed)))} ║"""
        
        if eta:
            text += f"\n║  ⏰ <b>ETA</b>        : {eta:<22} ║"
        
        text += f"""
║                                        ║
╠════════════════════════════════════════╣
║           <b>📊 STATISTIK LIVE</b>            ║
╠════════════════════════════════════════╣
║                                        ║
║  📈 Total        : {total:<23} ║
║  🔄 Progress     : {current}/{total} ({progress}%){' ' * max(0, 16 - len(str(current)) - len(str(total)) - len(str(progress)))} ║
║  {progress_bar}  ║
║                                        ║
║  ✅ Success (OK) : {ok:<23} ║
║  ⚠️ Checkpoint   : {cp:<23} ║
║  ❌ Failed       : {failed:<23} ║
║  📊 Success Rate : {success_rate}%{' ' * (20 - len(str(success_rate)))} ║
║                                        ║"""
        
        if self.last_result:
            text += """
╠════════════════════════════════════════╣
║         <b>📌 HASIL TERAKHIR</b>              ║
╠════════════════════════════════════════╣
║                                        ║"""
            
            if self.last_result.get('type') == 'OK':
                text += "\n║  ✅ <b>SUKSES CRACK!</b>                     ║\n"
                user_id = self.last_result.get('user_id', 'N/A')
                password = self.last_result.get('password', 'N/A')
                
                text += f"║  🆔 ID  : <code>{user_id[:28]}</code>"
                text += " " * max(0, 29 - len(user_id)) + "║\n"
                
                text += f"║  🔑 PW  : <code>{password[:28]}</code>"
                text += " " * max(0, 29 - len(password)) + "║\n"
                
                if 'cookie' in self.last_result and self.last_result['cookie']:
                    text += "║  🍪 Cookie tersimpan                   ║\n"
                
                if 'token' in self.last_result and self.last_result['token']:
                    text += "║  🎫 Token tersimpan                    ║\n"
                    
            elif self.last_result.get('type') == 'CP':
                text += "\n║  ⚠️ <b>CHECKPOINT DETECTED</b>               ║\n"
                user_id = self.last_result.get('user_id', 'N/A')
                password = self.last_result.get('password', 'N/A')
                
                text += f"║  🆔 ID  : <code>{user_id[:28]}</code>"
                text += " " * max(0, 29 - len(user_id)) + "║\n"
                
                text += f"║  🔑 PW  : <code>{password[:28]}</code>"
                text += " " * max(0, 29 - len(password)) + "║\n"
            
            text += "║                                        ║"
        else:
            if current == 0:
                text += """
╠════════════════════════════════════════╣
║  ⏳ <i>Memulai proses crack...</i>           ║"""
            else:
                text += """
╠════════════════════════════════════════╣
║  ⏳ <i>Sedang memproses targets...</i>        ║"""
            text += "\n║                                        ║"
        
        text += "\n╚════════════════════════════════════════╝"
        
        return text
    
    def _create_progress_bar(self, progress: int) -> str:
        """
        Buat progress bar visual
        
        Args:
            progress: Persentase progress (0-100)
            
        Returns:
            Progress bar string
        """
        bar_length = 30
        filled = int((progress / 100) * bar_length)
        empty = bar_length - filled
        
        bar = "█" * filled + "░" * empty
        return f"[{bar}]"
    
    async def finish(self, final_message: Optional[str] = None):
        """
        Selesaikan dashboard dan tampilkan summary
        
        Args:
            final_message: Pesan final optional
        """
        self.is_running = False
        
        if not self.message:
            return
        
        try:
            if final_message:
                await self.message.edit_text(final_message, parse_mode='HTML')
            else:
                text = self._generate_summary_text()
                await self.message.edit_text(text, parse_mode='HTML')
        except Exception as e:
            pass
    
    def _generate_summary_text(self) -> str:
        """Generate teks summary hasil akhir"""
        elapsed = ""
        if self.start_time:
            delta = datetime.now() - self.start_time
            minutes = delta.seconds // 60
            seconds = delta.seconds % 60
            elapsed = f"{minutes}m {seconds}s"
        
        total = self.stats.get('total', 0)
        current = self.stats.get('current', 0)
        ok = self.stats.get('ok', 0)
        cp = self.stats.get('cp', 0)
        failed = self.stats.get('failed', 0)
        
        text = f"""╔══════════════════════════════════╗
║  <b>📊 SUMMARY HASIL</b>               ║
╚══════════════════════════════════╝

⚡ <b>Operasi:</b> {self.operation_type}
⏱ <b>Total Waktu:</b> {elapsed}

┌──────────────────────────────────┐
│  <b>HASIL AKHIR</b>                     │
└──────────────────────────────────┘

📊 Total Target  : {total}
✔️ Diproses      : {current}
✅ Success (OK)  : {ok}
⚠️ Checkpoint    : {cp}
❌ Failed        : {failed}

"""
        
        if ok > 0:
            text += f"✅ Hasil OK disimpan di folder <code>OK/</code>\n"
        if cp > 0:
            text += f"⚠️ Hasil CP disimpan di folder <code>CP/</code>\n"
        
        text += f"\n💾 Gunakan /hasil untuk melihat file hasil"
        text += "\n\n╚══════════════════════════════════╝"
        
        return text


class TelegramDashboardSimple:
    """
    Class sederhana untuk operasi yang tidak perlu realtime update
    Hanya show progress dengan messages terpisah
    """
    
    @staticmethod
    async def send_progress(message: Message, text: str, parse_mode: str = 'HTML'):
        """Send progress message"""
        try:
            await message.reply_text(text, parse_mode=parse_mode)
        except Exception as e:
            pass
    
    @staticmethod
    async def edit_progress(message: Message, text: str, parse_mode: str = 'HTML'):
        """Edit existing message with progress"""
        try:
            await message.edit_text(text, parse_mode=parse_mode)
        except Exception as e:
            pass
