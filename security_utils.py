"""
Security utilities for LaptopTester
"""

import subprocess
import shlex
import logging
from typing import List, Dict, Any

class SecurityError(Exception):
    pass

class SecureCommandExecutor:
    """Thực thi command an toàn"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.allowed_commands = {
            'windows': ['cscript', 'powercfg', 'wmic', 'systeminfo', 'dxdiag'],
            'linux': ['lscpu', 'lshw', 'dmidecode', 'smartctl', 'hdparm']
        }
    
    def execute_safe(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Thực thi command với validation"""
        try:
            if not self._validate_command(command):
                raise SecurityError(f"Command not allowed: {command}")
            
            sanitized_cmd = self._sanitize_command(command)
            
            result = subprocess.run(
                sanitized_cmd,
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timeout: {command}")
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            self.logger.error(f"Command error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _validate_command(self, command: str) -> bool:
        """Validate command"""
        if not command or not isinstance(command, str):
            return False
        
        try:
            parts = shlex.split(command)
        except ValueError:
            return False
        
        if not parts:
            return False
        
        base_cmd = parts[0].lower()
        allowed = self.allowed_commands.get('windows', [])
        
        return base_cmd in allowed
    
    def _sanitize_command(self, command: str) -> List[str]:
        """Sanitize command"""
        try:
            parts = shlex.split(command)
        except ValueError:
            raise SecurityError("Invalid command syntax")
        
        dangerous_chars = ['|', '&', ';', '>', '<', '`', '$', '(', ')']
        for part in parts:
            if any(char in part for char in dangerous_chars):
                raise SecurityError(f"Dangerous character in: {part}")
        
        return parts

# Global instance
secure_executor = SecureCommandExecutor()
