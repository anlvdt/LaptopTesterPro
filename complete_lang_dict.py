#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Language Dictionary
Dictionary đầy đủ cho tất cả text trong ứng dụng
"""

COMPLETE_LANG = {
    "vi": {
        # Existing translations...
        "title": "LaptopTester Pro - Kiểm tra laptop toàn diện",
        
        # Add all missing translations
        "checklist_physical": "Checklist Kiểm Tra Ngoại Hình",
        "checklist_hardware": "Checklist Định Danh Phần Cứng",
        "checklist_license": "Checklist Kiểm Tra Bản Quyền",
        
        "question_physical": "Dựa trên checklist trên, tình trạng vật lý tổng thể của máy như thế nào?",
        "question_bios": "Các cài đặt trong BIOS có chính xác và an toàn không?",
        "question_hardware_done": "Định danh phần cứng đã hoàn thành. Bạn có muốn tiếp tục?",
        "question_license_done": "Kiểm tra bản quyền đã hoàn thành. Bạn có muốn tiếp tục?",
        
        "btn_excellent": "Rất tốt - Như mới",
        "btn_good_minor": "Tốt - Vết nhỏ",
        "btn_average": "Trung bình - Có lỗi nhỏ",
        "btn_poor": "Kém - Nhiều vấn đề",
        "btn_yes_correct": "Có, mọi cài đặt đều đúng",
        "btn_no_incorrect": "Không, có cài đặt sai/bị khóa",
        
        "result_displayed_checklist": "Đã hiển thị checklist",
        "result_ready": "Sẵn sàng",
        "result_excellent": "Rất tốt - Như mới",
        "result_good_minor": "Tốt - Có vết sử dụng nhỏ",
        "result_average": "Trung bình - Có lỗi nhỏ cần lưu ý",
        "result_poor": "Kém - Nhiều vấn đề nghiêm trọng",
        "result_correct_settings": "Cài đặt chính xác",
        "result_bios_issues": "Có vấn đề với cài đặt BIOS",
    },
    "en": {
        "title": "LaptopTester Pro - Comprehensive Laptop Testing",
        
        "checklist_physical": "Physical Inspection Checklist",
        "checklist_hardware": "Hardware Fingerprint Checklist",
        "checklist_license": "License Check Checklist",
        
        "question_physical": "Based on the checklist above, what is the overall physical condition of the machine?",
        "question_bios": "Are the BIOS settings correct and safe?",
        "question_hardware_done": "Hardware fingerprinting completed. Do you want to continue?",
        "question_license_done": "License check completed. Do you want to continue?",
        
        "btn_excellent": "Excellent - Like new",
        "btn_good_minor": "Good - Minor marks",
        "btn_average": "Average - Minor issues",
        "btn_poor": "Poor - Many issues",
        "btn_yes_correct": "Yes, all settings are correct",
        "btn_no_incorrect": "No, incorrect settings/locked",
        
        "result_displayed_checklist": "Checklist displayed",
        "result_ready": "Ready",
        "result_excellent": "Excellent - Like new",
        "result_good_minor": "Good - Minor wear marks",
        "result_average": "Average - Minor issues to note",
        "result_poor": "Poor - Many serious issues",
        "result_correct_settings": "Settings correct",
        "result_bios_issues": "BIOS settings issues",
    }
}

# Print để copy vào main file
if __name__ == "__main__":
    print("Copy this into main_enhanced_auto.py LANG dictionary:")
    print("\nAdd to 'vi' section:")
    for key, value in COMPLETE_LANG["vi"].items():
        if key not in ["title"]:  # Skip existing
            print(f'        "{key}": "{value}",')
    
    print("\nAdd to 'en' section:")
    for key, value in COMPLETE_LANG["en"].items():
        if key not in ["title"]:  # Skip existing
            print(f'        "{key}": "{value}",')
