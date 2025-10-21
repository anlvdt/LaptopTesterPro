"""
Security Fixes for LaptopTester
Khắc phục các lỗ hổng bảo mật nghiêm trọng
"""

import subprocess
import os
import re
import shlex
import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib
import secrets

class SecurityManager:
    """Quản lý bảo mật tổng thể"""
    
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
            
        # Kiểm tra command có trong whitelist
        cmd_parts = shlex.split(command)
        if not cmd_parts:
            return False
            
        base_command = cmd_parts[0].lower()
        allowed = self.allowed_commands.get(platform, [])
        
        return base_command in allowed

class SecureCommandExecutor:
    """Thực thi command an toàn"""
    
    def __init__(self):
        self.security_manager = SecurityManager()
        self.logger = logging.getLogger(__name__)
    
    def execute_safe(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Thực thi command với các biện pháp bảo mật"""
        try:
            # Validate command
            if not self.security_manager.validate_command(command):
                raise SecurityError(f"Command not allowed: {command}")
            
            # Sanitize command
            sanitized_cmd = self._sanitize_command(command)
            
            # Execute với subprocess an toàn
            result = subprocess.run(
                sanitized_cmd,
                shell=False,  # Không dùng shell=True
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                # Security settings
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
        # Sử dụng shlex để parse an toàn
        try:
            parts = shlex.split(command)
        except ValueError:
            raise SecurityError("Invalid command syntax")
        
        # Loại bỏ các ký tự nguy hiểm
        dangerous_chars = ['|', '&', ';', '>', '<', '`', '$', '(', ')']
        for part in parts:
            if any(char in part for char in dangerous_chars):
                raise SecurityError(f"Dangerous character in command: {part}")
        
        return parts

class SecurePathHandler:
    """Xử lý path an toàn"""
    
    @staticmethod
    def validate_path(path: str, base_dir: Optional[str] = None) -> bool:
        """Validate path để tránh path traversal"""
        if not path or not isinstance(path, str):
            return False
        
        try:
            # Normalize path
            normalized = os.path.normpath(path)
            
            # Kiểm tra path traversal
            if '..' in normalized or normalized.startswith('/'):
                return False
            
            # Nếu có base_dir, kiểm tra path nằm trong base_dir
            if base_dir:
                base_path = Path(base_dir).resolve()
                target_path = (base_path / normalized).resolve()
                
                # Kiểm tra target_path có nằm trong base_path không
                try:
                    target_path.relative_to(base_path)
                except ValueError:
                    return False
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def safe_join(base_dir: str, *paths) -> str:
        """Join paths an toàn"""
        base_path = Path(base_dir).resolve()
        
        for path in paths:
            if not SecurePathHandler.validate_path(path, base_dir):
                raise SecurityError(f"Invalid path: {path}")
        
        result_path = base_path.joinpath(*paths).resolve()
        
        # Đảm bảo result nằm trong base_dir
        try:
            result_path.relative_to(base_path)
        except ValueError:
            raise SecurityError("Path traversal detected")
        
        return str(result_path)

class SecureDatabaseManager:
    """Quản lý database an toàn"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Thực thi query với prepared statements"""
        try:
            # Validate query
            if not self._validate_query(query):
                raise SecurityError("Invalid or dangerous query")
            
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Sử dụng parameterized query
                cursor.execute(query, params)
                
                if query.strip().upper().startswith('SELECT'):
                    return [dict(row) for row in cursor.fetchall()]
                else:
                    conn.commit()
                    return []
                    
        except Exception as e:
            self.logger.error(f"Database error: {e}")
            raise
    
    def _validate_query(self, query: str) -> bool:
        """Validate SQL query"""
        if not query or not isinstance(query, str):
            return False
        
        # Kiểm tra các từ khóa nguy hiểm
        dangerous_keywords = [
            'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE',
            'EXEC', 'EXECUTE', 'xp_', 'sp_'
        ]
        
        query_upper = query.upper()
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False
        
        return True

class InputValidator:
    """Validate input từ người dùng"""
    
    @staticmethod
    def validate_filename(filename: str) -> bool:
        """Validate filename"""
        if not filename or not isinstance(filename, str):
            return False
        
        # Kiểm tra độ dài
        if len(filename) > 255:
            return False
        
        # Kiểm tra ký tự không hợp lệ
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        if any(char in filename for char in invalid_chars):
            return False
        
        # Kiểm tra reserved names (Windows)
        reserved_names = [
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        ]
        
        if filename.upper() in reserved_names:
            return False
        
        return True
    
    @staticmethod
    def validate_model_name(model_name: str) -> bool:
        """Validate laptop model name"""
        if not model_name or not isinstance(model_name, str):
            return False
        
        # Kiểm tra độ dài
        if len(model_name) > 100:
            return False
        
        # Chỉ cho phép alphanumeric, space, dash, underscore
        pattern = r'^[a-zA-Z0-9\s\-_]+$'
        return bool(re.match(pattern, model_name))
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize input string"""
        if not isinstance(input_str, str):
            return ""
        
        # Loại bỏ các ký tự điều khiển
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_str)
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        return sanitized

class CryptoManager:
    """Quản lý mã hóa"""
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Tạo token bảo mật"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_data(data: str, salt: Optional[str] = None) -> str:
        """Hash dữ liệu với salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        combined = f"{data}{salt}"
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        
        return f"{salt}:{hashed}"
    
    @staticmethod
    def verify_hash(data: str, hashed: str) -> bool:
        """Verify hash"""
        try:
            salt, expected_hash = hashed.split(':', 1)
            combined = f"{data}{salt}"
            actual_hash = hashlib.sha256(combined.encode()).hexdigest()
            
            return actual_hash == expected_hash
        except ValueError:
            return False

class SecurityError(Exception):
    """Custom security exception"""
    pass

class SecureLogger:
    """Logger bảo mật"""
    
    def __init__(self, name: str, log_file: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # File handler với rotation
        from logging.handlers import RotatingFileHandler
        handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        
        # Secure formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
    
    def log_security_event(self, event: str, details: Dict[str, Any]):
        """Log security events"""
        sanitized_details = self._sanitize_log_data(details)
        self.logger.warning(f"SECURITY: {event} - {sanitized_details}")
    
    def _sanitize_log_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize log data"""
        sanitized = {}
        
        for key, value in data.items():
            # Loại bỏ sensitive data
            if any(sensitive in key.lower() for sensitive in ['password', 'token', 'key']):
                sanitized[key] = '[REDACTED]'
            else:
                sanitized[key] = str(value)[:100]  # Limit length
        
        return sanitized

# Secure wrapper functions
def secure_subprocess_run(command: List[str], **kwargs) -> subprocess.CompletedProcess:
    """Wrapper an toàn cho subprocess.run"""
    executor = SecureCommandExecutor()
    
    # Validate command
    cmd_str = ' '.join(command)
    if not executor.security_manager.validate_command(cmd_str):
        raise SecurityError(f"Command not allowed: {cmd_str}")
    
    # Set secure defaults
    secure_kwargs = {
        'shell': False,
        'check': False,
        'timeout': kwargs.get('timeout', 30),
        'capture_output': True,
        'text': True
    }
    
    # Override với kwargs được cung cấp (nhưng không cho phép shell=True)
    for key, value in kwargs.items():
        if key != 'shell':  # Không cho phép override shell
            secure_kwargs[key] = value
    
    return subprocess.run(command, **secure_kwargs)

def secure_file_write(file_path: str, content: str, base_dir: str):
    """Ghi file an toàn"""
    # Validate path
    if not SecurePathHandler.validate_path(file_path, base_dir):
        raise SecurityError(f"Invalid file path: {file_path}")
    
    # Safe join
    safe_path = SecurePathHandler.safe_join(base_dir, file_path)
    
    # Write file
    with open(safe_path, 'w', encoding='utf-8') as f:
        f.write(content)

def secure_file_read(file_path: str, base_dir: str) -> str:
    """Đọc file an toàn"""
    # Validate path
    if not SecurePathHandler.validate_path(file_path, base_dir):
        raise SecurityError(f"Invalid file path: {file_path}")
    
    # Safe join
    safe_path = SecurePathHandler.safe_join(base_dir, file_path)
    
    # Check file exists và readable
    if not os.path.isfile(safe_path):
        raise FileNotFoundError(f"File not found: {safe_path}")
    
    # Read file
    with open(safe_path, 'r', encoding='utf-8') as f:
        return f.read()

# Export classes và functions
__all__ = [
    'SecurityManager',
    'SecureCommandExecutor', 
    'SecurePathHandler',
    'SecureDatabaseManager',
    'InputValidator',
    'CryptoManager',
    'SecurityError',
    'SecureLogger',
    'secure_subprocess_run',
    'secure_file_write',
    'secure_file_read'
]