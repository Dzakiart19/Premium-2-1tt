"""
Modul Session Manager untuk Cookie Persistence
Auto-save dan auto-load cookie/token dengan enkripsi
Auto-validasi token expired dan login ulang otomatis
"""

import os
import json
import base64
import hashlib
import time
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta


class SessionManager:
    """
    Manager untuk session persistence dengan enkripsi
    Auto-save cookie/token dan auto-validasi expired
    """
    
    def __init__(self, session_dir: str = ".sessions"):
        self.session_dir = session_dir
        os.makedirs(session_dir, exist_ok=True)
    
    def _encrypt_data(self, data: str, user_id: int) -> str:
        """
        Enkripsi data dengan base64 dan hash user_id
        
        Args:
            data: Data yang akan dienkripsi
            user_id: User ID sebagai key
            
        Returns:
            Data terenkripsi
        """
        key = hashlib.sha256(str(user_id).encode()).digest()
        data_bytes = data.encode('utf-8')
        
        encrypted = bytearray()
        for i, byte in enumerate(data_bytes):
            encrypted.append(byte ^ key[i % len(key)])
        
        return base64.b64encode(bytes(encrypted)).decode('utf-8')
    
    def _decrypt_data(self, encrypted_data: str, user_id: int) -> str:
        """
        Dekripsi data
        
        Args:
            encrypted_data: Data terenkripsi
            user_id: User ID sebagai key
            
        Returns:
            Data asli
        """
        try:
            key = hashlib.sha256(str(user_id).encode()).digest()
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            decrypted = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                decrypted.append(byte ^ key[i % len(key)])
            
            return bytes(decrypted).decode('utf-8')
        except:
            return ""
    
    def save_session(self, user_id: int, cookie: str, token: Optional[str] = None) -> bool:
        """
        Simpan session user ke file encrypted
        
        Args:
            user_id: User ID
            cookie: Cookie Facebook
            token: Access token (optional)
            
        Returns:
            True jika berhasil
        """
        try:
            session_file = os.path.join(self.session_dir, f"user_{user_id}.session")
            
            session_data = {
                'user_id': user_id,
                'cookie': cookie,
                'token': token,
                'saved_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=30)).isoformat()
            }
            
            json_data = json.dumps(session_data)
            encrypted_data = self._encrypt_data(json_data, user_id)
            
            with open(session_file, 'w') as f:
                f.write(encrypted_data)
            
            return True
        except Exception as e:
            return False
    
    def load_session(self, user_id: int) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
        """
        Load session user dari file
        
        Args:
            user_id: User ID
            
        Returns:
            Tuple (success, cookie, token, message)
        """
        try:
            session_file = os.path.join(self.session_dir, f"user_{user_id}.session")
            
            if not os.path.exists(session_file):
                return (False, None, None, "Session tidak ditemukan")
            
            with open(session_file, 'r') as f:
                encrypted_data = f.read()
            
            json_data = self._decrypt_data(encrypted_data, user_id)
            if not json_data:
                return (False, None, None, "Gagal dekripsi session")
            
            session_data = json.loads(json_data)
            
            expires_at = datetime.fromisoformat(session_data.get('expires_at'))
            if datetime.now() > expires_at:
                self.delete_session(user_id)
                return (False, None, None, "Session expired (>30 hari)")
            
            cookie = session_data.get('cookie')
            token = session_data.get('token')
            saved_at = session_data.get('saved_at')
            
            message = f"✅ Session loaded dari {saved_at[:10]}"
            
            return (True, cookie, token, message)
            
        except Exception as e:
            return (False, None, None, f"Error load session: {str(e)}")
    
    def delete_session(self, user_id: int) -> bool:
        """
        Hapus session user
        
        Args:
            user_id: User ID
            
        Returns:
            True jika berhasil
        """
        try:
            session_file = os.path.join(self.session_dir, f"user_{user_id}.session")
            if os.path.exists(session_file):
                os.remove(session_file)
            return True
        except:
            return False
    
    def validate_token(self, token: str) -> Tuple[bool, str]:
        """
        Validasi apakah token masih valid dengan Graph API
        
        Args:
            token: Access token
            
        Returns:
            Tuple (valid, message)
        """
        if not token:
            return (False, "Token tidak tersedia")
        
        try:
            import requests
            
            url = 'https://graph.facebook.com/v22.0/me'
            params = {'access_token': token}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data:
                    name = data.get('name', 'Unknown')
                    user_id = data.get('id', 'Unknown')
                    return (True, f"✅ Token valid! User: {name} (ID: {user_id})")
            
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            
            if 'expired' in error_msg.lower() or 'invalid' in error_msg.lower():
                return (False, "❌ Token expired atau invalid")
            
            return (False, f"❌ Token tidak valid: {error_msg}")
            
        except Exception as e:
            return (False, f"❌ Error validasi: {str(e)}")
    
    def auto_restore_session(self, user_id: int) -> Tuple[bool, Optional[str], Optional[str], str]:
        """
        Auto-restore session dengan validasi token
        
        Args:
            user_id: User ID
            
        Returns:
            Tuple (success, cookie, token, message)
        """
        success, cookie, token, msg = self.load_session(user_id)
        
        if not success:
            return (False, None, None, msg or "Session tidak tersedia")
        
        if token:
            valid, validation_msg = self.validate_token(token)
            
            if valid:
                return (True, cookie, token, f"🔄 {msg}\n{validation_msg}")
            else:
                self.delete_session(user_id)
                return (False, None, None, 
                       f"⚠️ Session ditemukan tapi token expired.\n"
                       f"Silakan login ulang dengan /login")
        
        return (True, cookie, token, 
               f"🔄 {msg}\n"
               f"⚠️ Token tidak ditemukan, beberapa fitur mungkin terbatas")
    
    def get_session_info(self, user_id: int) -> Dict:
        """
        Dapatkan info session user
        
        Args:
            user_id: User ID
            
        Returns:
            Dict info session
        """
        try:
            session_file = os.path.join(self.session_dir, f"user_{user_id}.session")
            
            if not os.path.exists(session_file):
                return {
                    'exists': False,
                    'message': 'Session tidak ditemukan'
                }
            
            with open(session_file, 'r') as f:
                encrypted_data = f.read()
            
            json_data = self._decrypt_data(encrypted_data, user_id)
            session_data = json.loads(json_data)
            
            saved_at = datetime.fromisoformat(session_data.get('saved_at'))
            expires_at = datetime.fromisoformat(session_data.get('expires_at'))
            
            days_left = (expires_at - datetime.now()).days
            
            return {
                'exists': True,
                'saved_at': saved_at.strftime("%Y-%m-%d %H:%M"),
                'expires_at': expires_at.strftime("%Y-%m-%d %H:%M"),
                'days_left': days_left,
                'has_token': session_data.get('token') is not None,
                'message': f"Session tersimpan, {days_left} hari lagi expired"
            }
        except:
            return {
                'exists': False,
                'message': 'Error membaca session'
            }
