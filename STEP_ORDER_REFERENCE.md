# LaptopTester Enhanced - Step Order Reference

## Current Step Sequence (Enhanced Version):

### Basic Mode Steps:
1. **🔍 Kiểm tra ngoại quan** (Physical Inspection) - `PhysicalInspectionGuideStep`
2. **🔒 Kiểm tra BIOS** (BIOS Check) - `BIOSAccessGuideStep`  
3. **🏷️ Định danh phần cứng** (Hardware Fingerprint) - `HardwareFingerprintStep`
4. **🔑 Kiểm tra bản quyền** (License Check) - `LicenseCheckStep`
5. **⚙️ Thông tin hệ thống** (System Information) - `SystemInfoStep`
6. **🎯 Phân tích cấu hình** (Configuration Analysis) - `ConfigurationAssessmentStep`
7. **💿 Sức khỏe ổ cứng** (Hard Drive Health) - `HardDriveHealthStep`
8. **📺 Kiểm tra màn hình** (Screen Test) - `ScreenTestStep`
9. **⌨️ Bàn phím** (Keyboard Test) - `KeyboardTestStep`
10. **🔋 Pin laptop** (Battery Health) - `BatteryHealthStep`
11. **🔊 Âm thanh** (Audio Test) - `AudioTestStep`
12. **📷 Webcam** (Webcam Test) - `WebcamTestStep`
13. **🔥 CPU Stress Test** - `CPUStressTestStep`
14. **💾 Tốc độ ổ cứng** (Hard Drive Speed) - `HardDriveSpeedStep`
15. **🎮 GPU Stress Test** - `GPUStressTestStep`

### Expert Mode Additional Steps:
16. **🔥 Test Tổng Hợp** (Combined Stress Test) - `CombinedStressTestStep`
17. **💿 Kiểm Tra Ổ Cứng Nâng Cao** (Advanced Disk Health) - `AdvancedDiskHealthStep`
18. **🛡️ Quét Bảo Mật** (Security Scan) - `SecurityScanStep`

## Data Flow Dependencies:

### Step 6 (Configuration Analysis) depends on:
- **Step 3** (Hardware Fingerprint): CPU, RAM, GPU, Storage info
- **Step 5** (System Information): Cross-reference data
- **BIOS Cache** (`_bios_cpu_info`): CPU information from Step 3

### Key Data Sources:
- **Hardware specs**: Step 3 → Step 6
- **System validation**: Step 5 → Step 6  
- **BIOS info**: Step 3 cache → Step 6

## Important Notes:
- ConfigurationAssessmentStep (Step 6) must look for data from Step 3, not Step 1
- Hardware Fingerprint is now Step 3 in the enhanced version
- System Information is Step 5 for cross-validation
- BIOS cache from Step 3 is the primary CPU source