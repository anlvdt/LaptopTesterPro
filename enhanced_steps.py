#!/usr/bin/env python3
"""
Enhanced Steps for LaptopTester Pro
Includes configuration assessment and BIOS guidance
"""

import customtkinter as ctk
import psutil
import platform
import subprocess
import threading
import webbrowser
from tkinter import messagebox

# Import from main file
from main import BaseStepFrame, Theme, get_text, CURRENT_LANG

class PhysicalInspectionGuideStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = "🔍 Hướng Dẫn Kiểm Tra Ngoại Quan" if CURRENT_LANG == "vi" else "🔍 Physical Inspection Guide"
        why_text = "Kiểm tra ngoại quan là bước đầu tiên và quan trọng nhất. Nhiều vấn đề phần cứng có thể phát hiện qua mắt thường trước khi chạy phần mềm." if CURRENT_LANG == "vi" else "Physical inspection is the first and most important step. Many hardware issues can be detected visually before running software."
        how_text = "Làm theo checklist dưới đây để kiểm tra từng bộ phận một cách có hệ thống." if CURRENT_LANG == "vi" else "Follow the checklist below to systematically inspect each component."
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.create_inspection_guide()
        
    def create_inspection_guide(self):
        # Main inspection checklist
        checklist_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        checklist_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        title_text = "📋 CHECKLIST KIỂM TRA NGOẠI QUAN" if CURRENT_LANG == "vi" else "📋 PHYSICAL INSPECTION CHECKLIST"
        ctk.CTkLabel(checklist_frame, text=title_text, font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Create inspection categories
        categories = self.get_inspection_categories()
        
        for category_name, items in categories.items():
            category_frame = ctk.CTkFrame(checklist_frame, fg_color=Theme.BACKGROUND, corner_radius=6)
            category_frame.pack(fill="x", padx=15, pady=8)
            
            ctk.CTkLabel(category_frame, text=category_name, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=15, pady=(10, 5))
            
            for item in items:
                item_frame = ctk.CTkFrame(category_frame, fg_color="transparent")
                item_frame.pack(fill="x", padx=15, pady=2)
                
                checkbox = ctk.CTkCheckBox(item_frame, text=item, font=Theme.BODY_FONT)
                checkbox.pack(anchor="w", padx=10, pady=2)
        
        # Critical warnings
        warning_frame = ctk.CTkFrame(checklist_frame, fg_color=Theme.ERROR, corner_radius=8)
        warning_frame.pack(fill="x", padx=15, pady=15)
        
        warning_title = "⚠️ CẢNH BÁO QUAN TRỌNG" if CURRENT_LANG == "vi" else "⚠️ CRITICAL WARNINGS"
        ctk.CTkLabel(warning_frame, text=warning_title, font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=(10, 5))
        
        warnings = self.get_critical_warnings()
        for warning in warnings:
            ctk.CTkLabel(warning_frame, text=f"• {warning}", font=Theme.BODY_FONT, text_color="white").pack(anchor="w", padx=15, pady=2)
        
        ctk.CTkLabel(warning_frame, text="", font=Theme.SMALL_FONT).pack(pady=5)
        
        self.show_result_choices()
    
    def get_inspection_categories(self):
        if CURRENT_LANG == "vi":
            return {
                "🖥️ MÀN HÌNH": [
                    "Kiểm tra vết nứt, vết xước trên màn hình",
                    "Thử mở/đóng màn hình - bản lề có chắc chắn không?",
                    "Màn hình có bị lỏng, rung lắc khi di chuyển không?",
                    "Viền màn hình có bị cong vênh, tróc sơn không?",
                    "Webcam và micro có bị che khuất không?"
                ],
                "⌨️ BÀN PHÍM & TOUCHPAD": [
                    "Các phím có bị lõm, mất chữ, dính không?",
                    "Thử nhấn từng phím - có phím nào cứng, không nhấn được?",
                    "Touchpad có bị trầy xước, không nhạy không?",
                    "Nút chuột trái/phải có hoạt động không?",
                    "Đèn LED bàn phím có sáng không? (nếu có)"
                ],
                "🔌 CỔNG KẾT NỐI": [
                    "Kiểm tra tất cả cổng USB - có bị lỏng, gãy không?",
                    "Cổng sạc có bị hỏng, tiếp xúc kém không?",
                    "Cổng HDMI, audio jack có hoạt động không?",
                    "Cổng mạng RJ45 (nếu có) có bị hỏng không?",
                    "Các cổng có dấu hiệu cháy, oxy hóa không?"
                ],
                "🏠 VỎ MÁY & TỔNG THỂ": [
                    "Vỏ máy có bị nứt, vỡ, cong vênh không?",
                    "Các góc máy có bị va đập mạnh không?",
                    "Nắp máy đóng/mở có khít không?",
                    "Có mùi cháy khét bất thường không?",
                    "Máy có dấu hiệu từng bị vào nước không?"
                ],
                "🔋 PIN & NGUỒN": [
                    "Pin có bị phồng, cong vênh không?",
                    "Adapter nguồn có dây bị đứt, cháy không?",
                    "Đèn báo sạc có hoạt động không?",
                    "Pin có tháo ra được không? (nếu có thể tháo)",
                    "Thông tin trên nhãn pin có rõ ràng không?"
                ]
            }
        else:
            return {
                "🖥️ DISPLAY": [
                    "Check for cracks, scratches on screen",
                    "Test opening/closing - are hinges secure?",
                    "Does screen wobble or shake when moved?",
                    "Is screen bezel warped or paint peeling?",
                    "Are webcam and microphone unobstructed?"
                ],
                "⌨️ KEYBOARD & TOUCHPAD": [
                    "Are keys worn, missing letters, or sticky?",
                    "Test each key - any stiff or non-responsive keys?",
                    "Is touchpad scratched or unresponsive?",
                    "Do left/right mouse buttons work?",
                    "Does keyboard backlight work? (if available)"
                ],
                "🔌 PORTS & CONNECTIONS": [
                    "Check all USB ports - any loose or broken?",
                    "Is charging port damaged or making poor contact?",
                    "Do HDMI, audio jack work properly?",
                    "Is RJ45 network port functional? (if available)",
                    "Any signs of burning or oxidation on ports?"
                ],
                "🏠 CASE & OVERALL": [
                    "Is case cracked, broken, or warped?",
                    "Are corners heavily impacted?",
                    "Does lid close/open properly?",
                    "Any unusual burning smell?",
                    "Any signs of water damage?"
                ],
                "🔋 BATTERY & POWER": [
                    "Is battery swollen or warped?",
                    "Is power adapter cable cut or burned?",
                    "Does charging indicator light work?",
                    "Can battery be removed? (if removable)",
                    "Is battery label information clear?"
                ]
            }
    
    def get_critical_warnings(self):
        if CURRENT_LANG == "vi":
            return [
                "Pin phồng = NGUY HIỂM! Có thể phát nổ, không nên mua",
                "Mùi cháy khét = Có thể cháy mạch, rất nguy hiểm",
                "Vết nước/ẩm ướt = Bo mạch có thể bị ăn mòn không phục hồi",
                "Màn hình nứt = Chi phí sửa chữa rất cao (3-5 triệu)",
                "Bản lề lỏng = Sẽ ngày càng hỏng nặng hơn theo thời gian"
            ]
        else:
            return [
                "Swollen battery = DANGEROUS! May explode, avoid purchase",
                "Burning smell = Possible circuit damage, very dangerous",
                "Water damage = Motherboard may be irreversibly corroded",
                "Cracked screen = Very expensive repair cost ($200-400)",
                "Loose hinges = Will progressively worsen over time"
            ]
    
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        question_text = "Sau khi kiểm tra ngoại quan, laptop có vấn đề nghiêm trọng nào không?" if CURRENT_LANG == "vi" else "After physical inspection, does the laptop have any serious issues?"
        ctk.CTkLabel(result_frame, text=question_text, font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        good_text = "✓ Ngoại quan tốt" if CURRENT_LANG == "vi" else "✓ Good condition"
        good_result = "Ngoại quan tốt" if CURRENT_LANG == "vi" else "Good physical condition"
        ctk.CTkButton(button_bar, text=good_text, 
                     command=lambda: self.mark_completed({"Kết quả": good_result, "Trạng thái": "Tốt"}, auto_advance=True), 
                     fg_color=Theme.SUCCESS, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        
        issues_text = "⚠️ Có vấn đề" if CURRENT_LANG == "vi" else "⚠️ Has issues"
        issues_result = "Có vấn đề ngoại quan" if CURRENT_LANG == "vi" else "Physical issues detected"
        ctk.CTkButton(button_bar, text=issues_text, 
                     command=lambda: self.mark_completed({"Kết quả": issues_result, "Trạng thái": "Lỗi"}, auto_advance=True), 
                     fg_color=Theme.ERROR, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)


class BIOSAccessGuideStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = "🔒 Kiểm Tra Truy Cập BIOS" if CURRENT_LANG == "vi" else "🔒 BIOS Access Check"
        why_text = "BIOS bị khóa là vấn đề nghiêm trọng nhất. Laptop bị khóa BIOS không thể cài lại Windows, nâng cấp phần cứng, hoặc sửa chữa. Đây là 'án tử' của laptop." if CURRENT_LANG == "vi" else "Locked BIOS is the most serious issue. A BIOS-locked laptop cannot reinstall Windows, upgrade hardware, or be repaired. This is a 'death sentence' for laptops."
        how_text = "Thực hiện các bước kiểm tra dưới đây để đảm bảo BIOS không bị khóa." if CURRENT_LANG == "vi" else "Follow the steps below to ensure BIOS is not locked."
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.create_bios_guide()
        
    def create_bios_guide(self):
        # BIOS access guide
        guide_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        guide_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        title_text = "🔒 HƯỚNG DẪN KIỂM TRA BIOS" if CURRENT_LANG == "vi" else "🔒 BIOS CHECK GUIDE"
        ctk.CTkLabel(guide_frame, text=title_text, font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Step-by-step instructions
        steps_frame = ctk.CTkFrame(guide_frame, fg_color=Theme.BACKGROUND, corner_radius=6)
        steps_frame.pack(fill="x", padx=15, pady=10)
        
        steps_title = "📋 CÁC BƯỚC THỰC HIỆN" if CURRENT_LANG == "vi" else "📋 STEP-BY-STEP INSTRUCTIONS"
        ctk.CTkLabel(steps_frame, text=steps_title, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(10, 5))
        
        steps = self.get_bios_steps()
        for i, step in enumerate(steps, 1):
            step_frame = ctk.CTkFrame(steps_frame, fg_color=Theme.FRAME, corner_radius=4)
            step_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(step_frame, text=f"{i}. {step}", font=Theme.BODY_FONT, wraplength=700, justify="left").pack(anchor="w", padx=15, pady=10)
        
        # Common BIOS keys
        keys_frame = ctk.CTkFrame(guide_frame, fg_color=Theme.INFO, corner_radius=8)
        keys_frame.pack(fill="x", padx=15, pady=10)
        
        keys_title = "⌨️ PHÍM VÀO BIOS THÔNG DỤNG" if CURRENT_LANG == "vi" else "⌨️ COMMON BIOS KEYS"
        ctk.CTkLabel(keys_frame, text=keys_title, font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=(10, 5))
        
        bios_keys = self.get_bios_keys()
        for brand, key in bios_keys.items():
            ctk.CTkLabel(keys_frame, text=f"• {brand}: {key}", font=Theme.BODY_FONT, text_color="white").pack(anchor="w", padx=15, pady=2)
        
        ctk.CTkLabel(keys_frame, text="", font=Theme.SMALL_FONT).pack(pady=5)
        
        # Warning about locked BIOS
        warning_frame = ctk.CTkFrame(guide_frame, fg_color=Theme.ERROR, corner_radius=8)
        warning_frame.pack(fill="x", padx=15, pady=15)
        
        warning_title = "🚨 CẢNH BÁO BIOS BỊ KHÓA" if CURRENT_LANG == "vi" else "🚨 LOCKED BIOS WARNING"
        ctk.CTkLabel(warning_frame, text=warning_title, font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=(10, 5))
        
        warnings = self.get_bios_warnings()
        for warning in warnings:
            ctk.CTkLabel(warning_frame, text=f"• {warning}", font=Theme.BODY_FONT, text_color="white").pack(anchor="w", padx=15, pady=2)
        
        ctk.CTkLabel(warning_frame, text="", font=Theme.SMALL_FONT).pack(pady=5)
        
        self.show_result_choices()
    
    def get_bios_steps(self):
        if CURRENT_LANG == "vi":
            return [
                "Khởi động lại máy tính (hoặc bật máy nếu đang tắt)",
                "Ngay khi thấy logo hãng (Dell, HP, Lenovo...), nhấn liên tục phím BIOS",
                "Nếu vào được BIOS: Kiểm tra có yêu cầu mật khẩu không?",
                "Thử thay đổi một cài đặt đơn giản (như thời gian) để test quyền ghi",
                "Kiểm tra mục Security/Password - có bị khóa không?",
                "Thử thoát BIOS và vào lại để đảm bảo không bị khóa tạm thời"
            ]
        else:
            return [
                "Restart the computer (or turn on if it's off)",
                "As soon as you see the brand logo (Dell, HP, Lenovo...), repeatedly press the BIOS key",
                "If BIOS opens: Check if password is required?",
                "Try changing a simple setting (like time) to test write permissions",
                "Check Security/Password section - is it locked?",
                "Try exiting BIOS and re-entering to ensure it's not temporarily locked"
            ]
    
    def get_bios_keys(self):
        return {
            "Dell": "F2 hoặc F12",
            "HP": "F10 hoặc ESC",
            "Lenovo": "F1, F2 hoặc Enter",
            "ASUS": "F2 hoặc Delete",
            "Acer": "F2 hoặc Delete",
            "MSI": "Delete hoặc F2",
            "Toshiba": "F2 hoặc F12",
            "Samsung": "F2 hoặc F10"
        }
    
    def get_bios_warnings(self):
        if CURRENT_LANG == "vi":
            return [
                "Không vào được BIOS = Có thể bị khóa hoàn toàn",
                "Yêu cầu mật khẩu BIOS = Không thể thay đổi cài đặt",
                "Không thể thay đổi cài đặt = BIOS bị khóa ghi",
                "Laptop công ty/trường học thường bị khóa BIOS",
                "BIOS bị khóa = KHÔNG NÊN MUA với bất kỳ giá nào!"
            ]
        else:
            return [
                "Cannot access BIOS = May be completely locked",
                "BIOS password required = Cannot change settings",
                "Cannot modify settings = BIOS write-locked",
                "Corporate/school laptops often have locked BIOS",
                "Locked BIOS = DO NOT BUY at any price!"
            ]
    
    def show_result_choices(self):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        question_text = "Sau khi kiểm tra, BIOS có bị khóa không?" if CURRENT_LANG == "vi" else "After checking, is the BIOS locked?"
        ctk.CTkLabel(result_frame, text=question_text, font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        unlocked_text = "✓ BIOS mở được" if CURRENT_LANG == "vi" else "✓ BIOS accessible"
        unlocked_result = "BIOS không bị khóa" if CURRENT_LANG == "vi" else "BIOS not locked"
        ctk.CTkButton(button_bar, text=unlocked_text, 
                     command=lambda: self.mark_completed({"Kết quả": unlocked_result, "Trạng thái": "Tốt"}, auto_advance=True), 
                     fg_color=Theme.SUCCESS, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        
        locked_text = "🔒 BIOS bị khóa" if CURRENT_LANG == "vi" else "🔒 BIOS locked"
        locked_result = "BIOS bị khóa - NGUY HIỂM!" if CURRENT_LANG == "vi" else "BIOS locked - DANGEROUS!"
        ctk.CTkButton(button_bar, text=locked_text, 
                     command=lambda: self.mark_completed({"Kết quả": locked_result, "Trạng thái": "Lỗi"}, auto_advance=True), 
                     fg_color=Theme.ERROR, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        
        skip_text = "⏭️ Bỏ qua" if CURRENT_LANG == "vi" else "⏭️ Skip"
        skip_result = "Chưa kiểm tra BIOS" if CURRENT_LANG == "vi" else "BIOS check skipped"
        ctk.CTkButton(button_bar, text=skip_text, 
                     command=lambda: self.mark_completed({"Kết quả": skip_result, "Trạng thái": "skip"}, auto_advance=True), 
                     fg_color=Theme.SKIP, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)


class ConfigurationAssessmentStep(BaseStepFrame):
    def __init__(self, master, **kwargs):
        title = "🎯 Đánh Giá Khả Năng Cấu Hình" if CURRENT_LANG == "vi" else "🎯 Configuration Capability Assessment"
        why_text = "Dựa trên cấu hình phần cứng đã kiểm tra, bước này sẽ đánh giá laptop có thể đảm đương những tác vụ gì và phù hợp với đối tượng người dùng nào." if CURRENT_LANG == "vi" else "Based on the hardware configuration tested, this step evaluates what tasks the laptop can handle and which user groups it's suitable for."
        how_text = "Hệ thống sẽ tự động phân tích cấu hình và đưa ra khuyến nghị sử dụng phù hợp." if CURRENT_LANG == "vi" else "The system will automatically analyze the configuration and provide appropriate usage recommendations."
        super().__init__(master, title, why_text, how_text, **kwargs)
        self.analyze_configuration()
        
    def analyze_configuration(self):
        # Get hardware info from previous steps - try all possible keys
        hw_results = {}
        system_results = {}
        
        # Debug: Print all available keys
        print(f"[DEBUG] All available result keys: {list(self.all_results.keys())}")
        
        # Find hardware fingerprint step (Step 3) by checking all keys
        for key, result in self.all_results.items():
            print(f"[DEBUG] Checking key: '{key}' -> {type(result)}")
            if any(pattern in key.lower() for pattern in ['hardware', 'fingerprint', 'định danh', 'phần cứng']):
                hw_results = result
                print(f"[DEBUG] Found hardware match: {key}")
                break
        
        # If not found, try exact key matching for Step 3 (Hardware Fingerprint)
        if not hw_results:
            possible_hw_keys = [
                "🏷️ Định danh phần cứng",
                "🏷️ Hardware Fingerprint", 
                "Hardware Fingerprint",
                "Định danh phần cứng",
                get_text("hardware_fingerprint")  # Use the same key as in step definition
            ]
            for key in possible_hw_keys:
                if key in self.all_results:
                    hw_results = self.all_results[key]
                    print(f"[DEBUG] Found hardware by exact key: {key}")
                    break
        
        # Find system info step (Step 5)
        for key, result in self.all_results.items():
            if any(pattern in key.lower() for pattern in ['system', 'info', 'thông tin', 'hệ thống']):
                system_results = result
                break
        
        # If not found, try exact key matching for system info (Step 5)
        if not system_results:
            possible_sys_keys = [
                "⚙️ Thông tin hệ thống",
                "⚙️ System Information",
                "System Information", 
                "Thông tin hệ thống",
                get_text("system_info")  # Use the same key as in step definition
            ]
            for key in possible_sys_keys:
                if key in self.all_results:
                    system_results = self.all_results[key]
                    print(f"[DEBUG] Found system by exact key: {key}")
                    break
        
        print(f"[DEBUG] Found hardware data: {bool(hw_results)}")
        print(f"[DEBUG] Found system data: {bool(system_results)}")
        if hw_results:
            print(f"[DEBUG] Hardware details length: {len(hw_results.get('Chi tiết', '') or hw_results.get('Details', ''))}")
        
        # Extract configuration details with fallback
        config_info = self.extract_config_info(hw_results, system_results)
        
        # If extraction failed, try direct system detection
        if config_info['cpu'] == 'Unknown' or config_info['ram'] == 0:
            config_info = self.fallback_system_detection(config_info)
        
        print(f"[DEBUG] Final config: {config_info}")
        
        # Create assessment display
        assessment_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
        assessment_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        title_text = "🎯 PHÂN TÍCH CẤU HÌNH" if CURRENT_LANG == "vi" else "🎯 CONFIGURATION ANALYSIS"
        ctk.CTkLabel(assessment_frame, text=title_text, font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
        
        # Display current configuration
        self.display_current_config(assessment_frame, config_info)
        
        # Performance assessment
        performance_score = self.calculate_performance_score(config_info)
        self.display_performance_assessment(assessment_frame, performance_score, config_info)
        
        # Usage recommendations
        self.display_usage_recommendations(assessment_frame, performance_score, config_info)
        
        # Upgrade suggestions
        self.display_upgrade_suggestions(assessment_frame, config_info)
        
        self.show_result_choices(performance_score)
    

    
    def extract_config_info(self, hw_results, system_results):
        config = {
            'cpu': 'Unknown',
            'ram': 0,
            'gpu': 'Unknown',
            'storage': 'Unknown',
            'cpu_score': 0,
            'ram_score': 0,
            'gpu_score': 0,
            'storage_score': 0
        }
        
        # Method 1: Extract from hardware fingerprint details
        hw_details = hw_results.get("Chi tiết", "") or hw_results.get("Details", "")
        print(f"[DEBUG] Hardware details found: {len(hw_details)} chars")
        
        # Method 1a: Try to get from cached BIOS info first (from Step 3 - Hardware Fingerprint)
        if '_bios_cpu_info' in self.all_results:
            bios_cpu = self.all_results['_bios_cpu_info']
            if bios_cpu and bios_cpu != 'N/A':
                config['cpu'] = bios_cpu
                print(f"[DEBUG] Found CPU from BIOS cache (Step 3): {config['cpu']}")
        
        # Method 1b: Extract from Step 3 (Hardware Fingerprint) details
        if hw_details:
            lines = hw_details.split('\n')
            for line in lines:
                line = line.strip()
                print(f"[DEBUG] Processing line: {line}")
                
                # CPU detection - exact patterns
                if line.lower().startswith('cpu:') or line.lower().startswith('processor:') or 'model laptop:' in line.lower():
                    parts = line.split(':', 1)
                    if len(parts) > 1 and parts[1].strip() and parts[1].strip() != 'N/A':
                        if config['cpu'] == 'Unknown':
                            config['cpu'] = parts[1].strip()
                            print(f"[DEBUG] Found CPU: {config['cpu']}")
                
                # RAM detection - exact patterns
                elif (line.lower().startswith('ram:') or line.lower().startswith('memory:') or line.lower().startswith('bộ nhớ:')) and 'gb' in line.lower():
                    import re
                    ram_match = re.search(r'(\d+(?:\.\d+)?)\s*GB', line, re.IGNORECASE)
                    if ram_match:
                        config['ram'] = float(ram_match.group(1))
                        print(f"[DEBUG] Found RAM: {config['ram']}GB")
                
                # GPU detection - exact patterns
                elif line.lower().startswith('gpu:') or line.lower().startswith('graphics:') or line.lower().startswith('video controller:'):
                    parts = line.split(':', 1)
                    if len(parts) > 1 and parts[1].strip() and parts[1].strip() != 'N/A':
                        config['gpu'] = parts[1].strip()
                        print(f"[DEBUG] Found GPU: {config['gpu']}")
                
                # Storage detection - exact patterns
                elif line.lower().startswith('model ổ cứng:') or line.lower().startswith('hard drive model:') or line.lower().startswith('disk drive:'):
                    parts = line.split(':', 1)
                    if len(parts) > 1 and parts[1].strip() and parts[1].strip() != 'N/A':
                        config['storage'] = parts[1].strip()
                        print(f"[DEBUG] Found Storage: {config['storage']}")
        
        # Method 2: Try system info results from Step 5 (System Information)
        if system_results and (config['cpu'] == 'Unknown' or config['ram'] == 0):
            sys_details = system_results.get("Chi tiết", "") or system_results.get("Details", "")
            if sys_details:
                lines = sys_details.split('\n')
                for line in lines:
                    line = line.strip()
                    if config['cpu'] == 'Unknown' and 'cpu' in line.lower():
                        parts = line.split(':', 1)
                        if len(parts) > 1 and parts[1].strip() != 'N/A':
                            config['cpu'] = parts[1].strip()
                            print(f"[DEBUG] Found CPU from Step 5 (System Info): {config['cpu']}")
                    
                    if config['ram'] == 0 and 'ram' in line.lower() and 'gb' in line.lower():
                        import re
                        ram_match = re.search(r'(\d+(?:\.\d+)?)\s*GB', line, re.IGNORECASE)
                        if ram_match:
                            config['ram'] = float(ram_match.group(1))
                            print(f"[DEBUG] Found RAM from Step 5 (System Info): {config['ram']}GB")
        
        # Method 3: Direct system detection as fallback
        if config['cpu'] == 'Unknown' or config['ram'] == 0:
            print("[DEBUG] Using fallback system detection")
            try:
                if config['ram'] == 0:
                    config['ram'] = round(psutil.virtual_memory().total / (1024**3), 1)
                    print(f"[DEBUG] Fallback RAM: {config['ram']}GB")
                
                if config['cpu'] == 'Unknown':
                    cpu_info = platform.processor()
                    if cpu_info and cpu_info.strip():
                        config['cpu'] = cpu_info
                        print(f"[DEBUG] Fallback CPU: {config['cpu']}")
                    else:
                        config['cpu'] = f"{psutil.cpu_count()} cores CPU"
            except Exception as e:
                print(f"[DEBUG] Fallback error: {e}")
        
        # Calculate performance scores
        config['cpu_score'] = self.score_cpu(config['cpu'])
        config['ram_score'] = self.score_ram(config['ram'])
        config['gpu_score'] = self.score_gpu(config['gpu'])
        
        return config
    
    def fallback_system_detection(self, config):
        """Fallback system detection when hardware fingerprint fails"""
        try:
            import psutil
            import platform
            
            # Get RAM if not found
            if config['ram'] == 0:
                config['ram'] = round(psutil.virtual_memory().total / (1024**3), 1)
                config['ram_score'] = self.score_ram(config['ram'])
            
            # Get CPU if not found
            if config['cpu'] == 'Unknown':
                cpu_info = platform.processor()
                if cpu_info:
                    config['cpu'] = cpu_info
                    config['cpu_score'] = self.score_cpu(cpu_info)
                else:
                    # Try psutil cpu info
                    config['cpu'] = f"{psutil.cpu_count()} cores CPU"
                    config['cpu_score'] = 50  # Default score
            
            # Try to get GPU info from system
            if config['gpu'] == 'Unknown':
                try:
                    if platform.system() == "Windows":
                        import subprocess
                        result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                              capture_output=True, text=True, timeout=5)
                        if result.stdout:
                            gpu_lines = [line.strip() for line in result.stdout.split('\n') if line.strip() and 'Name' not in line]
                            if gpu_lines:
                                config['gpu'] = gpu_lines[0]
                                config['gpu_score'] = self.score_gpu(gpu_lines[0])
                except:
                    pass
        
        except Exception as e:
            print(f"[DEBUG] Fallback detection error: {e}")
        
        return config
    
    def score_cpu(self, cpu_text):
        cpu_lower = cpu_text.lower()
        
        # Intel scoring
        if 'i9' in cpu_lower or 'i7' in cpu_lower:
            if any(gen in cpu_lower for gen in ['12th', '11th', '10th']):
                return 90  # High-end modern
            elif any(gen in cpu_lower for gen in ['9th', '8th', '7th']):
                return 75  # High-end older
            else:
                return 60  # High-end very old
        elif 'i5' in cpu_lower:
            if any(gen in cpu_lower for gen in ['12th', '11th', '10th']):
                return 75  # Mid-range modern
            elif any(gen in cpu_lower for gen in ['9th', '8th', '7th']):
                return 60  # Mid-range older
            else:
                return 45  # Mid-range old
        elif 'i3' in cpu_lower:
            if any(gen in cpu_lower for gen in ['12th', '11th', '10th']):
                return 55  # Entry modern
            else:
                return 35  # Entry old
        
        # AMD scoring
        elif 'ryzen 9' in cpu_lower or 'ryzen 7' in cpu_lower:
            if any(gen in cpu_lower for gen in ['5000', '4000']):
                return 85  # High-end modern AMD
            else:
                return 70  # High-end older AMD
        elif 'ryzen 5' in cpu_lower:
            if any(gen in cpu_lower for gen in ['5000', '4000']):
                return 70  # Mid-range modern AMD
            else:
                return 55  # Mid-range older AMD
        elif 'ryzen 3' in cpu_lower:
            return 50  # Entry AMD
        
        # Other processors
        elif any(old in cpu_lower for old in ['celeron', 'pentium', 'atom']):
            return 25  # Very low-end
        
        return 40  # Unknown/default
    
    def score_ram(self, ram_gb):
        if ram_gb >= 32:
            return 95  # Excellent
        elif ram_gb >= 16:
            return 85  # Very good
        elif ram_gb >= 8:
            return 70  # Good
        elif ram_gb >= 4:
            return 45  # Acceptable
        else:
            return 25  # Poor
    
    def score_gpu(self, gpu_text):
        gpu_lower = gpu_text.lower()
        
        # NVIDIA scoring
        if 'rtx' in gpu_lower:
            if any(model in gpu_lower for model in ['4090', '4080', '4070']):
                return 95  # Top tier
            elif any(model in gpu_lower for model in ['3080', '3070', '3060']):
                return 85  # High tier
            elif any(model in gpu_lower for model in ['2080', '2070', '2060']):
                return 75  # Good tier
            else:
                return 65  # Entry RTX
        elif 'gtx' in gpu_lower:
            if any(model in gpu_lower for model in ['1660', '1650']):
                return 55  # Entry gaming
            elif any(model in gpu_lower for model in ['1080', '1070']):
                return 70  # Older high-end
            else:
                return 45  # Older mid-range
        
        # AMD scoring
        elif 'rx' in gpu_lower:
            if any(model in gpu_lower for model in ['6800', '6700', '6600']):
                return 80  # Modern AMD high
            elif any(model in gpu_lower for model in ['5700', '5600', '5500']):
                return 65  # Older AMD
            else:
                return 50  # Entry AMD
        
        # Integrated graphics
        elif any(integrated in gpu_lower for integrated in ['intel', 'uhd', 'iris', 'vega']):
            if 'iris' in gpu_lower or 'vega' in gpu_lower:
                return 40  # Better integrated
            else:
                return 25  # Basic integrated
        
        return 30  # Unknown/default
    
    def calculate_performance_score(self, config):
        # Weighted average: CPU 40%, RAM 25%, GPU 35%
        total_score = (config['cpu_score'] * 0.4 + 
                      config['ram_score'] * 0.25 + 
                      config['gpu_score'] * 0.35)
        return round(total_score)
    
    def display_current_config(self, parent, config):
        config_frame = ctk.CTkFrame(parent, fg_color=Theme.BACKGROUND, corner_radius=6)
        config_frame.pack(fill="x", padx=15, pady=10)
        
        title_text = "💻 CẤU HÌNH HIỆN TẠI" if CURRENT_LANG == "vi" else "💻 CURRENT CONFIGURATION"
        ctk.CTkLabel(config_frame, text=title_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(10, 5))
        
        # Display components with scores
        components = [
            ("🔧 CPU", config['cpu'], config['cpu_score']),
            ("💾 RAM", f"{config['ram']} GB" if config['ram'] > 0 else "Không xác định", config['ram_score']),
            ("🎮 GPU", config['gpu'], config['gpu_score'])
        ]
        
        if config.get('storage', 'Unknown') != 'Unknown':
            components.append(("💿 Storage", config['storage'], 50))
        
        for icon_name, value, score in components:
            comp_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
            comp_frame.pack(fill="x", padx=10, pady=2)
            
            # Component info with truncation
            display_value = str(value)[:47] + "..." if len(str(value)) > 50 else str(value)
            ctk.CTkLabel(comp_frame, text=f"{icon_name}: {display_value}", font=Theme.BODY_FONT).pack(side="left", anchor="w")
            
            # Score indicator
            if score > 0:
                score_color = Theme.SUCCESS if score >= 70 else Theme.WARNING if score >= 50 else Theme.ERROR
                ctk.CTkLabel(comp_frame, text=f"({score}/100)", font=Theme.BODY_FONT, text_color=score_color).pack(side="right")
            else:
                ctk.CTkLabel(comp_frame, text="(N/A)", font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY).pack(side="right")
    
    def display_performance_assessment(self, parent, score, config):
        perf_frame = ctk.CTkFrame(parent, corner_radius=8)
        perf_frame.pack(fill="x", padx=15, pady=10)
        
        # Determine performance tier
        if score >= 80:
            tier = "HIGH-END" if CURRENT_LANG == "en" else "CAO CẤP"
            tier_color = Theme.SUCCESS
            tier_desc = "Máy tính hiệu năng cao" if CURRENT_LANG == "vi" else "High-performance computer"
        elif score >= 60:
            tier = "MID-RANGE" if CURRENT_LANG == "en" else "TRUNG BÌNH"
            tier_color = Theme.INFO
            tier_desc = "Máy tính tầm trung" if CURRENT_LANG == "vi" else "Mid-range computer"
        elif score >= 40:
            tier = "ENTRY-LEVEL" if CURRENT_LANG == "en" else "CƠ BẢN"
            tier_color = Theme.WARNING
            tier_desc = "Máy tính cơ bản" if CURRENT_LANG == "vi" else "Entry-level computer"
        else:
            tier = "LOW-END" if CURRENT_LANG == "en" else "YẾU"
            tier_color = Theme.ERROR
            tier_desc = "Máy tính hiệu năng thấp" if CURRENT_LANG == "vi" else "Low-performance computer"
        
        perf_frame.configure(fg_color=tier_color)
        
        ctk.CTkLabel(perf_frame, text=f"🏆 {tier} ({score}/100)", font=Theme.HEADING_FONT, text_color="white").pack(pady=(15, 5))
        ctk.CTkLabel(perf_frame, text=tier_desc, font=Theme.BODY_FONT, text_color="white").pack(pady=(0, 15))
    
    def display_usage_recommendations(self, parent, score, config):
        usage_frame = ctk.CTkFrame(parent, fg_color=Theme.FRAME, corner_radius=6)
        usage_frame.pack(fill="x", padx=15, pady=10)
        
        title_text = "🎯 KHUYẾN NGHỊ SỬ DỤNG" if CURRENT_LANG == "vi" else "🎯 USAGE RECOMMENDATIONS"
        ctk.CTkLabel(usage_frame, text=title_text, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=(10, 5))
        
        recommendations = self.get_usage_recommendations(score, config)
        
        for category, tasks in recommendations.items():
            cat_frame = ctk.CTkFrame(usage_frame, fg_color=Theme.BACKGROUND, corner_radius=4)
            cat_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(cat_frame, text=category, font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=(5, 2))
            
            for task, suitable in tasks.items():
                icon = "✅" if suitable else "❌"
                color = Theme.SUCCESS if suitable else Theme.ERROR
                ctk.CTkLabel(cat_frame, text=f"{icon} {task}", font=Theme.SMALL_FONT, text_color=color).pack(anchor="w", padx=20, pady=1)
            
            ctk.CTkLabel(cat_frame, text="", font=Theme.SMALL_FONT).pack(pady=2)
    
    def get_usage_recommendations(self, score, config):
        if CURRENT_LANG == "vi":
            base_tasks = {
                "📄 Văn phòng cơ bản": {
                    "Word, Excel, PowerPoint": score >= 30,
                    "Email, web browsing": score >= 25,
                    "PDF, in ấn": score >= 30,
                    "Zoom, Teams meeting": score >= 35
                },
                "🎨 Đồ họa & Thiết kế": {
                    "Photoshop cơ bản": score >= 50,
                    "Illustrator, CorelDraw": score >= 55,
                    "Video editing (1080p)": score >= 60,
                    "3D modeling": score >= 70,
                    "4K video editing": score >= 80
                },
                "🎮 Gaming": {
                    "Game nhẹ (LOL, CS:GO)": config['gpu_score'] >= 40,
                    "Game AAA (Medium)": config['gpu_score'] >= 60,
                    "Game AAA (High)": config['gpu_score'] >= 75,
                    "VR Gaming": config['gpu_score'] >= 80
                },
                "💻 Lập trình": {
                    "Code editor, IDE": score >= 40,
                    "Web development": score >= 45,
                    "Mobile app dev": score >= 55,
                    "Machine Learning": score >= 70,
                    "Docker, VM": config['ram'] >= 16
                }
            }
        else:
            base_tasks = {
                "📄 Basic Office": {
                    "Word, Excel, PowerPoint": score >= 30,
                    "Email, web browsing": score >= 25,
                    "PDF, printing": score >= 30,
                    "Zoom, Teams meeting": score >= 35
                },
                "🎨 Graphics & Design": {
                    "Basic Photoshop": score >= 50,
                    "Illustrator, CorelDraw": score >= 55,
                    "Video editing (1080p)": score >= 60,
                    "3D modeling": score >= 70,
                    "4K video editing": score >= 80
                },
                "🎮 Gaming": {
                    "Light games (LOL, CS:GO)": config['gpu_score'] >= 40,
                    "AAA games (Medium)": config['gpu_score'] >= 60,
                    "AAA games (High)": config['gpu_score'] >= 75,
                    "VR Gaming": config['gpu_score'] >= 80
                },
                "💻 Programming": {
                    "Code editor, IDE": score >= 40,
                    "Web development": score >= 45,
                    "Mobile app dev": score >= 55,
                    "Machine Learning": score >= 70,
                    "Docker, VM": config['ram'] >= 16
                }
            }
        
        return base_tasks
    
    def display_upgrade_suggestions(self, parent, config):
        upgrade_frame = ctk.CTkFrame(parent, fg_color=Theme.INFO, corner_radius=8)
        upgrade_frame.pack(fill="x", padx=15, pady=15)
        
        title_text = "🔧 GỢI Ý NÂNG CẤP" if CURRENT_LANG == "vi" else "🔧 UPGRADE SUGGESTIONS"
        ctk.CTkLabel(upgrade_frame, text=title_text, font=Theme.SUBHEADING_FONT, text_color="white").pack(pady=(10, 5))
        
        suggestions = self.get_upgrade_suggestions(config)
        
        if suggestions:
            for suggestion in suggestions:
                ctk.CTkLabel(upgrade_frame, text=f"• {suggestion}", font=Theme.BODY_FONT, text_color="white").pack(anchor="w", padx=15, pady=2)
        else:
            no_upgrade_text = "Cấu hình đã tối ưu, không cần nâng cấp" if CURRENT_LANG == "vi" else "Configuration is optimal, no upgrades needed"
            ctk.CTkLabel(upgrade_frame, text=no_upgrade_text, font=Theme.BODY_FONT, text_color="white").pack(padx=15, pady=5)
        
        ctk.CTkLabel(upgrade_frame, text="", font=Theme.SMALL_FONT).pack(pady=5)
    
    def get_upgrade_suggestions(self, config):
        suggestions = []
        
        if CURRENT_LANG == "vi":
            if config['ram'] < 8:
                suggestions.append(f"Nâng cấp RAM lên 8GB+ (hiện tại: {config['ram']}GB)")
            elif config['ram'] < 16:
                suggestions.append(f"Nâng cấp RAM lên 16GB để đa nhiệm tốt hơn")
            
            if config['gpu_score'] < 50:
                suggestions.append("Cân nhắc laptop có GPU rời để gaming/đồ họa")
            
            if config['cpu_score'] < 60:
                suggestions.append("CPU hiệu năng thấp, khó nâng cấp - cân nhắc máy khác")
            
            suggestions.append("Thêm SSD nếu đang dùng HDD để tăng tốc độ")
        else:
            if config['ram'] < 8:
                suggestions.append(f"Upgrade RAM to 8GB+ (current: {config['ram']}GB)")
            elif config['ram'] < 16:
                suggestions.append(f"Upgrade RAM to 16GB for better multitasking")
            
            if config['gpu_score'] < 50:
                suggestions.append("Consider laptop with dedicated GPU for gaming/graphics")
            
            if config['cpu_score'] < 60:
                suggestions.append("Low CPU performance, hard to upgrade - consider other laptop")
            
            suggestions.append("Add SSD if using HDD to improve speed")
        
        return suggestions
    
    def show_result_choices(self, performance_score):
        result_frame = ctk.CTkFrame(self.action_frame)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        # Auto-complete with analysis results
        result_details = f"Phân tích hoàn thành (Score: {performance_score}/100)" if CURRENT_LANG == "vi" else f"Analysis completed (Score: {performance_score}/100)"
        self.mark_completed({"Kết quả": result_details, "Trạng thái": "Tốt"}, auto_advance=False)
        
        question_text = "Cấu hình này có phù hợp với nhu cầu của bạn không?" if CURRENT_LANG == "vi" else "Does this configuration meet your needs?"
        ctk.CTkLabel(result_frame, text=question_text, font=Theme.SUBHEADING_FONT).pack(pady=15)
        
        button_bar = ctk.CTkFrame(result_frame, fg_color="transparent")
        button_bar.pack(pady=15)
        
        suitable_text = "✓ Phù hợp" if CURRENT_LANG == "vi" else "✓ Suitable"
        ctk.CTkButton(button_bar, text=suitable_text, 
                     command=lambda: self.go_to_next_step_callback(), 
                     fg_color=Theme.SUCCESS, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)
        
        unsuitable_text = "❌ Không phù hợp" if CURRENT_LANG == "vi" else "❌ Not suitable"
        ctk.CTkButton(button_bar, text=unsuitable_text, 
                     command=lambda: self.go_to_next_step_callback(), 
                     fg_color=Theme.ERROR, height=32, font=Theme.BUTTON_FONT).pack(side="left", padx=10)