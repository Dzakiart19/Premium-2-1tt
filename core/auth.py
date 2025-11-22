"""
Modul autentikasi Facebook
Handle login, token extraction, dan validasi credentials
Updated November 2025 dengan metode modern
"""

import re
import requests
from typing import Tuple, Optional, Dict
from .utils import CookieParser


class FacebookAuth:
    """Class untuk handle autentikasi Facebook"""
    
    def __init__(self):
        self.session = requests.Session()
        self.cookie_raw = None  # Cookie mentah dari user
        self.cookie_dict = {}   # Cookie parsed ke dict (siap pakai)
        self.token = None
    
    def save_cookie(self, cookie: str) -> Tuple[bool, str, Optional[str]]:
        """
        Simpan cookie dan coba extract token dengan metode modern 2025
        
        Args:
            cookie: Cookie Facebook (string mentah dari browser)
            
        Returns:
            Tuple (success, message, token)
        """
        self.cookie_raw = cookie
        self.cookie_dict = CookieParser.parse(cookie)
        
        valid, error_msg = CookieParser.validate(self.cookie_dict)
        if not valid:
            return (False, f"❌ {error_msg}", None)
        
        try:
            token = self._extract_token_modern_2025()
            
            if token:
                self.token = token
                return (True, f"✅ Login berhasil! Token ditemukan.\nToken: {token[:50]}...", token)
            
            return (True, "⚠️ Cookie disimpan, tapi token tidak ditemukan. Beberapa fitur mungkin terbatas.", None)
            
        except Exception as e:
            return (False, f"❌ Error: {str(e)}", None)
    
    def _extract_token_modern_2025(self) -> Optional[str]:
        """
        Extract token menggunakan metode PERSIS dari run.py (WORKING DI TERMUX)
        
        Method dari run.py line 922-941 yang sudah terbukti 100% berhasil
        EXACT COPY dari kode yang working di termux!
        
        Menggunakan self.cookie_dict yang sudah diparsing saat save_cookie()
        
        Returns:
            Token atau None
        """
        try:
            # CRITICAL FIX: Gunakan cookie_dict yang sudah diparsing!
            # Sudah diparsing di save_cookie(), jadi langsung pakai!
            
            with requests.Session() as xyz:
                url = 'https://www.facebook.com/adsmanager/manage/campaigns'
                
                # Step 1: Get initial page (SAMA PERSIS LINE 929)
                req = xyz.get(url, cookies=self.cookie_dict)
                
                # Step 2: Extract act parameter (SAMA PERSIS LINE 930)
                set_match = re.search('act=(.*?)&nav_source', str(req.content))
                if set_match:
                    set_val = set_match.group(1)
                    
                    # Step 3: Build URL dengan act parameter (SAMA PERSIS LINE 931)
                    nek = '%s?act=%s&nav_source=no_referrer' % (url, set_val)
                    
                    # Step 4: Get detail page (SAMA PERSIS LINE 932)
                    roq = xyz.get(nek, cookies=self.cookie_dict)
                    
                    # Step 5: Extract token (SAMA PERSIS LINE 933)
                    tok_match = re.search('accessToken="(.*?)"', str(roq.content))
                    if tok_match:
                        token = tok_match.group(1)
                        if token and len(token) > 50:
                            return token
            
            return None
            
        except Exception as e:
            return None
    
    def _method_adsmanager(self, cookies=None, headers=None) -> Optional[str]:
        """Extract token dari Facebook Ads Manager (metode seperti run.py)"""
        try:
            url = 'https://www.facebook.com/adsmanager/manage/campaigns'
            
            if cookies:
                response = self.session.get(url, cookies=cookies, headers=headers, timeout=15)
            else:
                response = self.session.get(url, headers=headers, timeout=15)
            
            content = response.text
            
            act_match = re.search(r'act=(.*?)&nav_source', content)
            if act_match:
                act_id = act_match.group(1)
                detail_url = f'{url}?act={act_id}&nav_source=no_referrer'
                
                if cookies:
                    detail_response = self.session.get(detail_url, cookies=cookies, headers=headers, timeout=15)
                else:
                    detail_response = self.session.get(detail_url, headers=headers, timeout=15)
                
                content = detail_response.text
            
            token_patterns = [
                r'accessToken["\s:]+([A-Za-z0-9]+)',
                r'"accessToken":"(EAAG[A-Za-z0-9]+)"',
                r'"accessToken":"(EAAB[A-Za-z0-9]+)"',
                r'"access_token":"(EAAG[A-Za-z0-9]+)"',
                r'"access_token":"(EAAB[A-Za-z0-9]+)"',
                r'EAAG[\w]+',
                r'EAAB[\w]+',
                r'EAAI[\w]+',
                r'EAAH[\w]+',
                r'EAAL[\w]+'
            ]
            
            for pattern in token_patterns:
                match = re.search(pattern, content)
                if match:
                    token = match.group(1) if len(match.groups()) > 0 else match.group(0)
                    if token and len(token) > 50:
                        return token
            
            return None
            
        except Exception as e:
            return None
    
    def _method_business_locations(self, cookies=None, headers=None) -> Optional[str]:
        """Extract token dari Business Manager locations"""
        try:
            url = 'https://business.facebook.com/business_locations'
            
            if cookies:
                response = self.session.get(url, cookies=cookies, headers=headers, timeout=15)
            else:
                response = self.session.get(url, headers=headers, timeout=15)
            
            content = response.text
            
            token_patterns = [
                r'EAAG[\w]+',
                r'EAAB[\w]+',
                r'EAAI[\w]+',
                r'EAAH[\w]+',
                r'EAAL[\w]+'
            ]
            
            for pattern in token_patterns:
                match = re.search(pattern, content)
                if match:
                    token = match.group(0)
                    if len(token) > 50:
                        return token
            
            return None
            
        except Exception as e:
            return None
    
    def _method_mobile_basic(self, cookies=None, headers=None) -> Optional[str]:
        """Extract token dari mobile Facebook basic"""
        try:
            url = 'https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed'
            
            if cookies:
                response = self.session.get(url, cookies=cookies, headers=headers, timeout=15)
            else:
                response = self.session.get(url, headers=headers, timeout=15)
            
            content = response.text
            
            token_patterns = [
                r'EAAG[\w]+',
                r'EAAB[\w]+'
            ]
            
            for pattern in token_patterns:
                match = re.search(pattern, content)
                if match:
                    token = match.group(0)
                    if len(token) > 50:
                        return token
            
            return None
            
        except Exception as e:
            return None
    
    def _method_mbasic_home(self, cookies=None, headers=None) -> Optional[str]:
        """Extract token dari mbasic home page"""
        try:
            url = 'https://mbasic.facebook.com/home.php'
            
            if cookies:
                response = self.session.get(url, cookies=cookies, headers=headers, timeout=15)
            else:
                response = self.session.get(url, headers=headers, timeout=15)
            
            content = response.text
            
            token_patterns = [
                r'"accessToken":"(EAAG[\w]+)"',
                r'"accessToken":"(EAAB[\w]+)"',
                r'EAAG[\w]{100,}',
                r'EAAB[\w]{100,}'
            ]
            
            for pattern in token_patterns:
                match = re.search(pattern, content)
                if match:
                    token = match.group(1) if len(match.groups()) > 0 else match.group(0)
                    if token and len(token) > 50:
                        return token
            
            return None
            
        except Exception as e:
            return None
    
    def _method_cookie_direct(self, cookies=None, headers=None) -> Optional[str]:
        """Extract token langsung dari cookie jika ada (backup method)"""
        try:
            if cookies and isinstance(cookies, dict):
                for key, value in cookies.items():
                    if key.lower().startswith('eaa') and len(value) > 50:
                        return value
            
            return None
            
        except Exception as e:
            return None
    
    def validate_credentials(self) -> Tuple[bool, str]:
        """
        Validasi cookie dan token dengan Graph API v22.0
        
        Returns:
            Tuple (valid, message)
        """
        # CRITICAL FIX: Gunakan cookie_raw dan cookie_dict yang baru!
        if not self.cookie_raw and not self.cookie_dict:
            return (False, "Cookie tidak tersedia")
        
        try:
            if self.token:
                url = 'https://graph.facebook.com/v22.0/me'
                params = {'access_token': self.token}
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'id' in data:
                        return (True, f"Token valid! User: {data.get('name', 'Unknown')}")
            
            # Gunakan cookie_dict yang sudah diparsing
            if self.cookie_dict:
                url = 'https://www.facebook.com/me'
                response = self.session.get(url, cookies=self.cookie_dict, timeout=10, allow_redirects=False)
            else:
                # Fallback: gunakan raw cookie di header
                headers = {'Cookie': self.cookie_raw}
                url = 'https://www.facebook.com/me'
                response = self.session.get(url, headers=headers, timeout=10, allow_redirects=False)
            
            if response.status_code == 200:
                return (True, "Cookie valid")
            else:
                return (False, "Cookie mungkin sudah expired")
                
        except Exception as e:
            return (False, f"Error validasi: {str(e)}")
    
    def get_user_id(self) -> Optional[str]:
        """
        Dapatkan user ID dari cookie
        
        Returns:
            User ID atau None
        """
        # CRITICAL FIX: Gunakan cookie_dict yang sudah diparsing!
        try:
            # Coba dari cookie_dict terlebih dahulu
            if self.cookie_dict and 'c_user' in self.cookie_dict:
                return self.cookie_dict['c_user']
            
            # Fallback: parse dari raw
            if self.cookie_raw:
                match = re.search(r'c_user=(\d+)', self.cookie_raw)
                if match:
                    return match.group(1)
            
            return None
        except:
            return None
