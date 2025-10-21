#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Translation Wrapper
Wrapper function để tự động dịch text dựa trên CURRENT_LANG
"""

from translator import translate

# Global language variable (will be set from main app)
CURRENT_LANG = "vi"

def t(text):
    """
    Translation wrapper function
    Tự động dịch text dựa trên CURRENT_LANG
    
    Args:
        text: Text cần dịch (có thể là tiếng Việt hoặc tiếng Anh)
    
    Returns:
        Text đã dịch theo ngôn ngữ hiện tại
    """
    global CURRENT_LANG
    
    # Nếu đang ở chế độ tiếng Anh, dịch sang tiếng Anh
    if CURRENT_LANG == "en":
        # Mapping tiếng Việt -> Anh
        vi_to_en = {
            # Common
            "Đang tải...": "Loading...",
            "Đang kiểm tra...": "Checking...",
            "Đang đọc...": "Reading...",
            "Sẵn sàng": "Ready",
            "Hoàn thành": "Completed",
            "Bỏ qua": "Skip",
            "Tiếp tục": "Continue",
            "Trước": "Previous",
            "Tiếp theo": "Next",
            "Tốt": "Good",
            "Lỗi": "Error",
            "Cảnh báo": "Warning",
            
            # Test steps
            "Kiểm Tra Ngoại Hình": "Physical Inspection",
            "Kiểm tra ngoại hình": "Physical inspection",
            "Định Danh Phần Cứng": "Hardware Fingerprint",
            "Bản Quyền Windows": "Windows License",
            "Bản quyền Windows": "Windows license",
            "Cấu Hình Hệ Thống": "System Configuration",
            "Sức Khỏe Ổ Cứng": "Hard Drive Health",
            "Kiểm Tra Màn Hình": "Screen Test",
            "Bàn Phím & Touchpad": "Keyboard & Touchpad",
            "Bàn phím & Touchpad": "Keyboard & Touchpad",
            "Pin Laptop": "Battery Health",
            "Loa & Micro": "Audio Test",
            "Webcam": "Webcam",
            
            # Results
            "Kết quả": "Result",
            "Trạng thái": "Status",
            "Chi tiết": "Details",
            "Đã hiển thị checklist": "Checklist displayed",
            "Sẵn sàng": "Ready",
            
            # Actions
            "Bắt đầu Test": "Start Test",
            "Dừng Test": "Stop Test",
            "Xóa vết vẽ": "Clear Drawing",
            "Bắt đầu": "Start",
            "Dừng": "Stop",
            
            # Questions
            "Dựa trên checklist trên, tình trạng vật lý tổng thể của máy như thế nào?": "Based on the checklist above, what is the overall physical condition of the machine?",
            "Các cài đặt trong BIOS có chính xác và an toàn không?": "Are the BIOS settings correct and safe?",
            "Định danh phần cứng đã hoàn thành. Bạn có muốn tiếp tục?": "Hardware fingerprinting completed. Do you want to continue?",
            "Kiểm tra bản quyền đã hoàn thành. Bạn có muốn tiếp tục?": "License check completed. Do you want to continue?",
            
            # Buttons
            "Rất tốt - Như mới": "Excellent - Like new",
            "Tốt - Vết nhỏ": "Good - Minor marks",
            "Trung bình - Có lỗi nhỏ": "Average - Minor issues",
            "Kém - Nhiều vấn đề": "Poor - Many issues",
            "Có, mọi cài đặt đều đúng": "Yes, all settings are correct",
            "Không, có cài đặt sai/bị khóa": "No, incorrect settings/locked",
            
            # More phrases
            "Checklist Kiểm Tra Ngoại Hình": "Physical Inspection Checklist",
            "Checklist Định Danh Phần Cứng": "Hardware Fingerprint Checklist",
            "Checklist Kiểm Tra Bản Quyền": "License Check Checklist",
        }
        
        # Tìm trong mapping
        if text in vi_to_en:
            return vi_to_en[text]
        
        # Nếu không tìm thấy, dùng translator
        return translate(text)
    
    # Nếu đang ở chế độ tiếng Việt, giữ nguyên
    return text

def set_language(lang):
    """Set ngôn ngữ hiện tại"""
    global CURRENT_LANG
    CURRENT_LANG = lang
