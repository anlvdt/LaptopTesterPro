import os
import sys
import subprocess

def build_exe():
    print("Building LaptopTester.exe...")
    
    # Install PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create directories
    os.makedirs("assets", exist_ok=True)
    os.makedirs("bin", exist_ok=True)
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=LaptopTester", 
        "laptoptester.py"
    ]
    
    print("Building... This may take several minutes...")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        exe_path = os.path.join("dist", "LaptopTester.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"SUCCESS! EXE created: {exe_path}")
            print(f"Size: {size_mb:.1f} MB")
        else:
            print("ERROR: EXE file not found")
    else:
        print("ERROR: Build failed")

if __name__ == "__main__":
    build_exe()
    input("Press Enter to exit...")