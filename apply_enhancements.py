#!/usr/bin/env python3
"""
Script tự động áp dụng các cải tiến vào main.py
Giữ nguyên UI/UX, chỉ thêm security và bug fixes
"""

import os
import shutil
from datetime import datetime

def backup_main():
    """Backup main.py hiện tại"""
    source = "backup_old_files/main.py"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"backup_old_files/main_backup_{timestamp}.py"
    
    print(f"📦 Backing up {source} to {backup}")
    shutil.copy2(source, backup)
    print("✅ Backup completed")
    return backup

def create_enhanced_main():
    """Tạo main.py được cải tiến"""
    
    print("\n🚀 Creating enhanced main.py...")
    
    # Đọc main.py gốc
    with open("backup_old_files/main.py", "r", encoding="utf-8") as f:
        original_content = f.read()
    
    # Thêm security imports
    security_imports = '''
# ============================================================================
# SECURITY ENHANCEMENTS - Added by apply_enhancements.py
# ============================================================================
import shlex
from typing import List, Dict, Any, Optional

class SecurityError(Exception):
    """Custom security exception"""
    pass

class SecureCommandExecutor:
    """Thực thi command an toàn"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.allowed_commands = {
            'windows': ['cscript', 'powercfg', 'wmic', 'systeminfo'],
            'linux': ['lscpu', 'lshw', 'dmidecode', 'smartctl']
        }
    
    def execute_safe(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Thực thi command với validation"""
        try:
            # Validate command
            if not self._validate_command(command):
                raise SecurityError(f"Command not allowed: {command}")
            
            # Sanitize
            sanitized_cmd = self._sanitize_command(command)
            
            # Execute
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
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _validate_command(self, command: str) -> bool:
        """Validate command"""
        if not command:
            return False
        parts = shlex.split(command)
        if not parts:
            return False
        base_cmd = parts[0].lower()
        return base_cmd in self.allowed_commands.get('windows', [])
    
    def _sanitize_command(self, command: str) -> List[str]:
        """Sanitize command"""
        parts = shlex.split(command)
        dangerous = ['|', '&', ';', '>', '<', '`', '$']
        for part in parts:
            if any(c in part for c in dangerous):
                raise SecurityError(f"Dangerous char in: {part}")
        return parts

# Global secure executor
_secure_executor = SecureCommandExecutor()

'''
    
    # Tìm vị trí insert (sau imports)
    import_end = original_content.find("# Configuration")
    if import_end == -1:
        import_end = original_content.find("CURRENT_LANG")
    
    # Insert security code
    enhanced_content = (
        original_content[:import_end] +
        security_imports +
        "\n" +
        original_content[import_end:]
    )
    
    # Thay thế subprocess calls nguy hiểm
    replacements = [
        # LicenseCheckStep
        (
            'subprocess.check_output("cscript //Nologo C:\\\\\\\\Windows\\\\\\\\System32\\\\\\\\slmgr.vbs /xpr", shell=False',
            '_secure_executor.execute_safe("cscript C:\\\\\\\\Windows\\\\\\\\System32\\\\\\\\slmgr.vbs /xpr")["stdout"]'
        ),
    ]
    
    for old, new in replacements:
        if old in enhanced_content:
            enhanced_content = enhanced_content.replace(old, new)
            print(f"✅ Replaced: {old[:50]}...")
    
    # Ghi file mới
    output_file = "backup_old_files/main_enhanced_auto.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(enhanced_content)
    
    print(f"✅ Created {output_file}")
    return output_file

def create_security_module():
    """Tạo module security riêng"""
    
    print("\n🔒 Creating security_utils.py...")
    
    security_code = '''"""
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
'''
    
    with open("security_utils.py", "w", encoding="utf-8") as f:
        f.write(security_code)
    
    print("✅ Created security_utils.py")

def main():
    """Main function"""
    
    print("=" * 70)
    print("🚀 LaptopTester Enhancement Script")
    print("=" * 70)
    
    # Backup
    backup_file = backup_main()
    
    # Create enhanced version
    enhanced_file = create_enhanced_main()
    
    # Create security module
    create_security_module()
    
    print("\n" + "=" * 70)
    print("✅ HOÀN THÀNH!")
    print("=" * 70)
    print(f"\n📦 Backup: {backup_file}")
    print(f"🚀 Enhanced: {enhanced_file}")
    print(f"🔒 Security: security_utils.py")
    
    print("\n📝 NEXT STEPS:")
    print("1. Review enhanced file: backup_old_files/main_enhanced_auto.py")
    print("2. Test security fixes")
    print("3. If OK, replace main.py:")
    print("   copy backup_old_files\\main_enhanced_auto.py backup_old_files\\main.py")
    print("\n⚠️  IMPORTANT: Test thoroughly before using in production!")

if __name__ == "__main__":
    main()
