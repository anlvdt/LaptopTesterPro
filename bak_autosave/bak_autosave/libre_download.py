import os
import urllib.request
import zipfile
import shutil

LHM_URLS = [
    # Nguồn chính (GitHub Releases)
    "https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/download/v0.9.2/LibreHardwareMonitor.zip",
    # Nguồn dự phòng (mirror, có thể thay đổi)
    "https://files.laptopchecker.net/LibreHardwareMonitor.zip"
]

LHM_DIR = os.path.join(os.path.dirname(__file__), "bin", "LibreHardwareMonitor")
LHM_ZIP = os.path.join(LHM_DIR, "LibreHardwareMonitor.zip")


def ensure_librehardwaremonitor():
    if os.path.exists(os.path.join(LHM_DIR, "LibreHardwareMonitor.exe")):
        return True
    os.makedirs(LHM_DIR, exist_ok=True)
    for url in LHM_URLS:
        try:
            print(f"Đang tải LibreHardwareMonitor từ: {url}")
            urllib.request.urlretrieve(url, LHM_ZIP)
            print("Tải thành công, giải nén...")
            with zipfile.ZipFile(LHM_ZIP, 'r') as zip_ref:
                zip_ref.extractall(LHM_DIR)
            os.remove(LHM_ZIP)
            print("Đã cài đặt LibreHardwareMonitor!")
            return True
        except Exception as e:
            print(f"Lỗi tải từ {url}: {e}")
    print("Không thể tải LibreHardwareMonitor từ bất kỳ nguồn nào!")
    return False

if __name__ == "__main__":
    ok = ensure_librehardwaremonitor()
    if ok:
        print("LibreHardwareMonitor đã sẵn sàng!")
    else:
        print("Lỗi: Không thể chuẩn bị LibreHardwareMonitor!")
