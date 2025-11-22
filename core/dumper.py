"""
Modul untuk dump ID Facebook
Handle dump dari ID publik, teman, dll
Updated November 2025 dengan Graph API v22.0
"""

import requests
import sys
from typing import List, Tuple, Optional, Callable, Dict
from .utils import UserAgentGenerator, CookieParser


class FacebookDumper:
    """Class untuk dump ID Facebook dengan Graph API v22.0"""
    
    def __init__(self, cookie: str, token: Optional[str] = None):
        self.cookie_raw = cookie
        self.cookie_dict = CookieParser.parse(cookie)
        self.token = token
        self.session = requests.Session()
        self.ids = []
        self.cookie_only_mode = not bool(token)
    
    def dump_public(
        self, 
        target_id: str, 
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> Tuple[bool, str, List[str]]:
        """
        Dump ID dari target publik menggunakan Graph API v22.0
        
        Args:
            target_id: ID target Facebook atau 'me' untuk teman sendiri
            progress_callback: Fungsi callback untuk update progress
            
        Returns:
            Tuple (success, message, id_list)
        """
        self.ids = []
        
        # CRITICAL FIX: Gunakan cookie_raw bukan self.cookie!
        if not self.token and not self.cookie_raw:
            return (False, "❌ Cookie tidak tersedia. Silakan login ulang dengan /login", [])
        
        try:
            original_target = target_id
            
            if target_id.lower() == 'me':
                user_id = self._get_user_id_from_cookie()
                if not user_id:
                    return (False, "❌ Tidak dapat menemukan User ID dari cookie.\n\n💡 Pastikan cookie Anda valid dan lengkap.", [])
                target_id = user_id
            
            if not target_id or not target_id.isdigit():
                return (False, f"❌ Target ID tidak valid: '{original_target}'\n\n💡 Gunakan ID numerik Facebook atau 'me' untuk teman sendiri.", [])
            
            if self.token:
                if progress_callback:
                    progress_callback(0)
                
                error_msg = self._dump_friends_graph_api(target_id, "", progress_callback)
                
                if self.ids:
                    return (True, f"✅ Berhasil dump {len(self.ids)} ID dari target {target_id}", self.ids)
                else:
                    if error_msg:
                        return (False, error_msg, [])
                    else:
                        return (False, f"❌ Tidak ada ID yang berhasil di-dump.\n\n💡 Kemungkinan:\n• Target tidak memiliki teman publik\n• Akun target bersifat private\n• ID target salah: {target_id}\n\n🔄 Coba:\n1. Gunakan 'me' untuk dump teman sendiri\n2. Gunakan ID publik lain", [])
            else:
                return (False, "⚠️ Token tidak tersedia!\n\n💡 Token diperlukan untuk dump ID.\n\n🔄 Silakan login ulang dengan /login\nBot akan otomatis extract token dari cookie Anda.", [])
                
        except Exception as e:
            return (False, f"❌ Error dump: {str(e)}\n\n🔄 Coba login ulang dengan /login", [])
    
    def _dump_friends_graph_api(
        self, 
        target_id: str, 
        after_cursor: str, 
        progress_callback: Optional[Callable[[int], None]]
    ) -> Optional[str]:
        """
        Dump teman menggunakan Facebook Graph API (EXACT METHOD DARI RUN.PY LINE 1180-1209)
        
        Method yang sama persis dengan run.py yang working di termux!
        
        Args:
            target_id: ID target
            after_cursor: Cursor untuk pagination
            progress_callback: Fungsi callback untuk update progress
            
        Returns:
            Error message jika ada, None jika sukses
        """
        try:
            # EXACT HEADERS DARI RUN.PY LINE 1182
            headers = {
                "connection": "keep-alive", 
                "accept": "*/*", 
                "sec-fetch-dest": "empty", 
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin", 
                "sec-fetch-user": "?1",
                "sec-ch-ua-mobile": "?1",
                "upgrade-insecure-requests": "1", 
                "user-agent": "Mozilla/5.0 (Linux; Android 11; AC2003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36",
                "accept-encoding": "gzip, deflate",
                "accept-language": "id-ID,id;q=0.9"
            }
            
            # EXACT PARAMS DARI RUN.PY LINE 1184-1186
            if len(self.ids) == 0 or not after_cursor:
                params = {
                    "access_token": self.token,
                    "fields": "name,friends.fields(id,name,birthday)"
                }
            else:
                params = {
                    "access_token": self.token,
                    "fields": f"name,friends.fields(id,name,birthday).after({after_cursor})"
                }
            
            # EXACT URL & REQUEST DARI RUN.PY LINE 1187
            # CRITICAL FIX: Gunakan cookie_dict yang sudah diparsing saat init
            url = f"https://graph.facebook.com/{target_id}"
            
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                cookies=self.cookie_dict,
                timeout=30
            )
            
            data = response.json()
            
            # Error checking (SAMA SEPERTI RUN.PY LINE 1189-1195)
            if "error" in data:
                error_msg = data['error'].get('message', 'Unknown error')
                return f"❌ Error dari Facebook API: {error_msg}"
            
            if "friends" not in data or "data" not in data["friends"]:
                return "❌ Tidak dapat mengakses daftar teman. Pastikan akun bersifat publik atau token valid."
            
            # EXACT LOOP UNTUK APPEND ID (SAMA SEPERTI RUN.PY LINE 1197-1200)
            for i in data["friends"]["data"]:
                friend_id = i.get("id", "")
                friend_name = i.get("name", "Unknown")
                
                if friend_id and friend_name:
                    self.ids.append(f"{friend_id}|{friend_name}")
                    
                    if progress_callback:
                        progress_callback(len(self.ids))
                    else:
                        sys.stdout.write(f"\r • sedang dump id, berhasil mendapatkan : {len(self.ids)} ID")
                        sys.stdout.flush()
            
            # EXACT PAGINATION CHECK (SAMA SEPERTI RUN.PY LINE 1202-1203)
            if "paging" in data["friends"] and "cursors" in data["friends"]["paging"]:
                if "after" in data["friends"]["paging"]["cursors"]:
                    next_cursor = data["friends"]["paging"]["cursors"]["after"]
                    return self._dump_friends_graph_api(target_id, next_cursor, progress_callback)
            
            return None
                    
        except Exception as e:
            return f"❌ Error tidak terduga: {str(e)}"
    
    def dump_from_user_friends(
        self,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> Tuple[bool, str, List[str]]:
        """
        Dump ID dari daftar teman user sendiri (me)
        
        Args:
            progress_callback: Fungsi callback untuk update progress
            
        Returns:
            Tuple (success, message, id_list)
        """
        return self.dump_public("me", progress_callback)
    
    def _get_user_id_from_cookie(self) -> Optional[str]:
        """
        Extract user ID dari cookie
        
        Returns:
            User ID atau None
        """
        try:
            # Gunakan cookie dict yang sudah diparsing
            if 'c_user' in self.cookie_dict:
                return self.cookie_dict['c_user']
            
            # Fallback: parse dari raw string
            import re
            match = re.search(r'c_user=(\d+)', self.cookie_raw)
            if match:
                return match.group(1)
            return None
        except:
            return None
    
    def save_to_file(self, filename: str) -> Tuple[bool, str]:
        """
        Simpan hasil dump ke file
        
        Args:
            filename: Nama file (akan otomatis ditambahkan di folder data/)
            
        Returns:
            Tuple (success, message)
        """
        try:
            import os
            os.makedirs("data", exist_ok=True)
            
            # Fix: Remove duplicate data/ prefix if already in filename
            if filename.startswith("data/"):
                filepath = filename
            else:
                filepath = f"data/{filename}"
            
            if not filepath.endswith('.txt'):
                filepath += '.txt'
            
            with open(filepath, "w", encoding="utf-8") as f:
                for id_data in self.ids:
                    f.write(id_data + "\n")
            
            return (True, f"✅ Berhasil simpan {len(self.ids)} ID ke {filepath}")
        except Exception as e:
            return (False, f"❌ Error simpan file: {str(e)}")
    
    def load_from_file(self, filename: str) -> Tuple[bool, str, int]:
        """
        Load ID dari file
        
        Args:
            filename: Nama file (bisa dengan atau tanpa path)
            
        Returns:
            Tuple (success, message, count)
        """
        try:
            if not filename.startswith("data/") and not filename.startswith("/"):
                filename = f"data/{filename}"
            
            if not filename.endswith('.txt'):
                filename += '.txt'
            
            self.ids = []
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and "|" in line:
                        self.ids.append(line)
                    elif line and line.isdigit():
                        self.ids.append(f"{line}|Unknown")
            
            return (True, f"✅ Berhasil load {len(self.ids)} ID dari {filename}", len(self.ids))
        except FileNotFoundError:
            return (False, f"❌ File tidak ditemukan: {filename}", 0)
        except Exception as e:
            return (False, f"❌ Error load file: {str(e)}", 0)
