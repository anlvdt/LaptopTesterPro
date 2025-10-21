"""
Translation Patch for LaptopTester v2.5
Adds missing translations for checklist titles, guide sections, and report headers
"""

MISSING_TRANSLATIONS = {
    "vi": {
        # Checklist titles
        "checklist_hardware": "📋 Checklist Định Danh Phần Cứng",
        "checklist_license": "📋 Checklist Kiểm Tra Bản Quyền",
        "checklist_physical": "🔍 Checklist Kiểm Tra Ngoại Hình Chi Tiết",
        "checklist_bios": "⚙️ Checklist Kiểm Tra BIOS Chi Tiết",
        
        # Section headers
        "case_hinges": "💻 Vỏ Máy & Bản Lề:",
        "ports": "🔌 Cổng Kết Nối:",
        "screws_warranty": "🔩 Ốc Vít & Tem Bảo Hành:",
        "thinkpad_special": "🔴 LENOVO THINKPAD - KIỂM TRA ĐẶC BIỆT:",
        
        # BIOS sections
        "bios_access": "🔑 Cách Vào BIOS:",
        "cpu_performance": "⚡ Hiệu Năng CPU:",
        "ram_settings": "💾 RAM:",
        "bios_password_warning": "⛔ CẢNH BÁO NGHIÊM TRỌNG - MẬT KHẨU BIOS",
        "security_other": "🔒 BẢO MẬT KHÁC:",
        "thinkpad_settings": "🔴 THINKPAD - CÀI ĐẶT KHÁC:",
        
        # Battery sections
        "battery_analysis": "📊 Phân Tích Chi Tiết",
        "battery_care": "💡 LỜI KHUYÊN VỀ SỨC KHỎE PIN",
        "battery_tips": "📋 CÁCH SẠC VÀ SỬ DỤNG PIN ĐÚNG CÁCH:",
        "battery_avoid": "❌ NHỮNG ĐIỀU CẦN TRÁNH:",
        
        # Report sections
        "test_results": "📊 Kết Quả Test",
        "professional_tools": "CÔNG CỤ CHUYÊN NGHIỆP BỔ SUNG",
        "tools_description": "Để kiểm tra sâu hơn, hãy sử dụng các công cụ chuyên nghiệp sau:",
    },
    "en": {
        # Checklist titles
        "checklist_hardware": "📋 Hardware Fingerprint Checklist",
        "checklist_license": "📋 License Check Checklist",
        "checklist_physical": "🔍 Detailed Physical Inspection Checklist",
        "checklist_bios": "⚙️ Detailed BIOS Check Checklist",
        
        # Section headers
        "case_hinges": "💻 Case & Hinges:",
        "ports": "🔌 Ports:",
        "screws_warranty": "🔩 Screws & Warranty Seals:",
        "thinkpad_special": "🔴 LENOVO THINKPAD - SPECIAL CHECKS:",
        
        # BIOS sections
        "bios_access": "🔑 How to Access BIOS:",
        "cpu_performance": "⚡ CPU Performance:",
        "ram_settings": "💾 RAM:",
        "bios_password_warning": "⛔ CRITICAL WARNING - BIOS PASSWORD",
        "security_other": "🔒 OTHER SECURITY:",
        "thinkpad_settings": "🔴 THINKPAD - OTHER SETTINGS:",
        
        # Battery sections
        "battery_analysis": "📊 Detailed Analysis",
        "battery_care": "💡 BATTERY HEALTH ADVICE",
        "battery_tips": "📋 PROPER CHARGING AND USAGE:",
        "battery_avoid": "❌ THINGS TO AVOID:",
        
        # Report sections
        "test_results": "📊 Test Results",
        "professional_tools": "ADDITIONAL PROFESSIONAL TOOLS",
        "tools_description": "For deeper inspection, use these professional tools:",
    }
}

# Lines to replace in main_enhanced_auto.py
REPLACEMENTS = [
    # Line 1030
    ('ctk.CTkLabel(checklist_frame, text="📋 Checklist Định Danh Phần Cứng"',
     'checklist_title = "📋 Checklist Định Danh Phần Cứng" if CURRENT_LANG == "vi" else "📋 Hardware Fingerprint Checklist"\n        ctk.CTkLabel(checklist_frame, text=checklist_title'),
    
    # Line 1462
    ('ctk.CTkLabel(checklist_frame, text="📋 Checklist Kiểm Tra Bản Quyền"',
     'checklist_title = "📋 Checklist Kiểm Tra Bản Quyền" if CURRENT_LANG == "vi" else "📋 License Check Checklist"\n        ctk.CTkLabel(checklist_frame, text=checklist_title'),
    
    # Line 2762
    ('ctk.CTkLabel(checklist_frame, text="🔍 Checklist Kiểm Tra Ngoại Hình Chi Tiết"',
     'checklist_title = "🔍 Checklist Kiểm Tra Ngoại Hình Chi Tiết" if CURRENT_LANG == "vi" else "🔍 Detailed Physical Inspection Checklist"\n        ctk.CTkLabel(checklist_frame, text=checklist_title'),
    
    # Line 2847
    ('ctk.CTkLabel(checklist_frame, text="⚙️ Checklist Kiểm Tra BIOS Chi Tiết"',
     'checklist_title = "⚙️ Checklist Kiểm Tra BIOS Chi Tiết" if CURRENT_LANG == "vi" else "⚙️ Detailed BIOS Check Checklist"\n        ctk.CTkLabel(checklist_frame, text=checklist_title'),
]

print("Translation Patch Ready!")
print(f"Total missing translations: {len(MISSING_TRANSLATIONS['vi'])}")
print(f"Total replacements needed: {len(REPLACEMENTS)}")
