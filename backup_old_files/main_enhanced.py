#!/usr/bin/env python3
"""
LaptopTester Pro - Enhanced Version
Consolidated main file with security fixes and UI improvements
"""

import os
import sys
import subprocess
import shlex
from pathlib import Path

# Security imports
import logging
from typing import List, Dict, Any, Optional

# Import original main.py components
# (Giữ nguyên toàn bộ imports và classes từ main.py gốc)

# ============================================================================
# SECURITY ENHANCEMENTS
# ============================================================================

class SecurityManager:
    """Quản lý bảo mật - từ security_fixes.py"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.allowed_commands = {
            'windows': [
                'cscript', 'powercfg', 'wmic', 'systeminfo',
                'dxdiag', 'msinfo32'
            ],
            'linux': [
                'lscpu', 'lshw', 'dmidecode', 'smartctl',
                'hdparm', 'sensors'
            ]
        }
        
    def validate_command(self, command: str, platform: str = 'windows') -> bool:
        """Validate command trước khi thực thi"""
        if not command or not isinstance(command, str):
            return False
            
        cmd_parts = shlex.split(command)
        if not cmd_parts:
            return False
            
        base_command = cmd_parts[0].lower()
        allowed = self.allowed_commands.get(platform, [])
        
        return base_command in allowed

class SecureCommandExecutor:
    """Thực thi command an toàn - từ security_fixes.py"""
    
    def __init__(self):
        self.security_manager = SecurityManager()
        self.logger = logging.getLogger(__name__)
    
    def execute_safe(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Thực thi command với các biện pháp bảo mật"""
        try:
            if not self.security_manager.validate_command(command):
                raise SecurityError(f"Command not allowed: {command}")
            
            sanitized_cmd = self._sanitize_command(command)
            
            result = subprocess.run(
                sanitized_cmd,
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timeout: {command}")
            return {'success': False, 'error': 'Command timeout'}
        except Exception as e:
            self.logger.error(f"Command execution error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _sanitize_command(self, command: str) -> List[str]:
        """Sanitize command để tránh injection"""
        try:
            parts = shlex.split(command)
        except ValueError:
            raise SecurityError("Invalid command syntax")
        
        dangerous_chars = ['|', '&', ';', '>', '<', '`', '$', '(', ')']
        for part in parts:
            if any(char in part for char in dangerous_chars):
                raise SecurityError(f"Dangerous character in command: {part}")
        
        return parts

class SecurityError(Exception):
    """Custom security exception"""
    pass

# ============================================================================
# UI IMPROVEMENTS
# ============================================================================

class NotificationToast:
    """Modern toast notifications - từ ui_improvements.py"""
    
    def __init__(self, parent):
        self.parent = parent
        self.toasts = []
    
    def show(self, message, type="info", duration=3000):
        """Show toast notification"""
        import customtkinter as ctk
        import threading
        import time
        
        colors = {
            "info": Theme.INFO,
            "success": Theme.SUCCESS,
            "warning": Theme.WARNING,
            "error": Theme.ERROR
        }
        
        toast = ctk.CTkFrame(
            self.parent,
            fg_color=colors.get(type, Theme.INFO),
            corner_radius=Theme.CORNER_RADIUS,
            width=300,
            height=60
        )
        
        y_offset = len(self.toasts) * 70 + Theme.PADDING
        toast.place(x=self.parent.winfo_width() - 320, y=y_offset)
        
        ctk.CTkLabel(
            toast,
            text=message,
            font=Theme.BODY_FONT,
            text_color="white",
            wraplength=280
        ).pack(expand=True, padx=Theme.PADDING, pady=Theme.SPACING)
        
        self.toasts.append(toast)
        
        def remove_toast():
            time.sleep(duration / 1000)
            try:
                toast.destroy()
                self.toasts.remove(toast)
            except:
                pass
        
        threading.Thread(target=remove_toast, daemon=True).start()

# ============================================================================
# ENHANCED FEATURES
# ============================================================================

class SystemMonitor:
    """Real-time system monitoring - từ enhanced_features.py"""
    
    def __init__(self, parent):
        self.parent = parent
        self.is_monitoring = False
        self.data_points = {
            'cpu': [],
            'memory': [],
            'temperature': [],
            'timestamps': []
        }
        self.max_points = 60

# ============================================================================
# MAIN APPLICATION (Giữ nguyên từ main.py gốc)
# ============================================================================

# Copy toàn bộ code từ main.py gốc vào đây, chỉ thay thế:
# 1. subprocess.run() -> SecureCommandExecutor().execute_safe()
# 2. Thêm NotificationToast cho user feedback
# 3. Thêm SystemMonitor cho advanced monitoring

# [Giữ nguyên toàn bộ code từ main.py gốc]

if __name__ == "__main__":
    # Initialize security
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/laptoptester_secure.log'),
            logging.StreamHandler()
        ]
    )
    
    # Run application
    app = LaptopTesterApp()
    app.mainloop()
