"""
Enhanced Physical Inspection and BIOS Check Guide
Hướng dẫn chi tiết kiểm tra ngoại quan và BIOS - Đặc biệt cảnh báo ThinkPad bị khóa
"""

PHYSICAL_INSPECTION_GUIDE = {
    "vi": {
        "title": "🔍 HƯỚNG DẪN KIỂM TRA NGOẠI QUAN CHI TIẾT",
        "why": "Tình trạng vật lý phản ánh cách sử dụng và bảo quản của chủ cũ. Máy bị rơi, vào nước, hoặc sửa chữa kém có thể gây lỗi không lường trước.",
        "sections": {
            "exterior": {
                "title": "💻 BÊN NGOÀI",
                "items": [
                    "• Vỏ máy: Kiểm tra vết nứt, rạn nứt, móp méo ở góc",
                    "• Bản lề: Mở/đóng 10-15 lần, nghe tiếng kêu lạ",
                    "• Bản lề phải chặt, giữ được góc mở, không rơ",
                    "• Bàn phím: Nhấn từng phím, không được lỏng/kẹt",
                    "• Touchpad: Bề mặt phẳng, không lồi, click êm",
                    "• Cổng kết nối: USB, HDMI, audio - cắm thử, không lỏng",
                    "• Lỗ thoát khí: Không bị bịt tắc bởi bụi"
                ]
            },
            "hardware": {
                "title": "🔩 PHẦN CỨNG",
                "items": [
                    "• Ốc vít: Không bị toét đầu (dấu hiệu tháo lắp)",
                    "• Tem bảo hành: Còn nguyên, không bị bóc",
                    "• Serial number: Khớp với BIOS và sticker",
                    "• Đèn LED: Sáng bình thường khi cắm sạc",
                    "• Lưới thoát khí: Sạch, không bụi dày"
                ]
            },
            "ports": {
                "title": "🔌 CỔNG KẾT NỐI",
                "items": [
                    "• Cổng sạc: Cắm và lay nhẹ - KHÔNG được lỏng",
                    "• Cổng lỏng = thay mainboard (chi phí cao!)",
                    "• USB: Cắm USB, kiểm tra nhận diện",
                    "• HDMI: Nếu có, cắm màn hình ngoài test",
                    "• Audio jack: Cắm tai nghe, nghe 2 bên"
                ]
            },
            "thinkpad_specific": {
                "title": "⚠️ ĐẶC BIỆT VỚI THINKPAD",
                "items": [
                    "• Kiểm tra tem Lenovo chính hãng dưới đáy",
                    "• Xem sticker có bị bóc/dán lại không",
                    "• ThinkPad doanh nghiệp thường có asset tag",
                    "• Kiểm tra kỹ vì ThinkPad dễ bị khóa BIOS",
                    "• Hỏi rõ nguồn gốc: cá nhân hay thanh lý công ty"
                ]
            },
            "warning_signs": {
                "title": "🚨 DẤU HIỆU CẢNH BÁO",
                "items": [
                    "• Bản lề rất lỏng hoặc kêu kèn kẹt",
                    "• Cổng sạc lỏng, không giữ chặt",
                    "• Vết nứt gần bản lề (rất nguy hiểm)",
                    "• Mùi lạ (cháy, hóa chất, ẩm mốc)",
                    "• Ốc vít bị toét nhiều (tháo lắp liên tục)",
                    "• Tem bảo hành bị rách, mờ, hoặc thiếu"
                ]
            }
        }
    },
    "en": {
        "title": "🔍 DETAILED PHYSICAL INSPECTION GUIDE",
        "why": "Physical condition reflects previous owner's usage and care. Dropped, water-damaged, or poorly repaired machines can cause unpredictable issues.",
        "sections": {
            "exterior": {
                "title": "💻 EXTERIOR",
                "items": [
                    "• Case: Check for cracks, fractures, dents at corners",
                    "• Hinges: Open/close 10-15 times, listen for strange sounds",
                    "• Hinges must be tight, hold angle, no wobbling",
                    "• Keyboard: Press each key, none should be loose/stuck",
                    "• Touchpad: Flat surface, not bulging, smooth clicks",
                    "• Ports: USB, HDMI, audio - test plug, not loose",
                    "• Vents: Not blocked by dust"
                ]
            },
            "hardware": {
                "title": "🔩 HARDWARE",
                "items": [
                    "• Screws: Not stripped (sign of disassembly)",
                    "• Warranty seal: Intact, not peeled",
                    "• Serial number: Matches BIOS and sticker",
                    "• LED lights: Normal when charging",
                    "• Vent grills: Clean, no thick dust"
                ]
            },
            "ports": {
                "title": "🔌 PORTS",
                "items": [
                    "• Charging port: Plug and wiggle - must NOT be loose",
                    "• Loose port = replace motherboard (expensive!)",
                    "• USB: Plug USB, check detection",
                    "• HDMI: If available, test with external monitor",
                    "• Audio jack: Plug headphones, test both sides"
                ]
            },
            "thinkpad_specific": {
                "title": "⚠️ THINKPAD SPECIFIC",
                "items": [
                    "• Check genuine Lenovo seal on bottom",
                    "• Look for peeled/re-applied stickers",
                    "• Corporate ThinkPads usually have asset tags",
                    "• Check carefully as ThinkPads prone to BIOS lock",
                    "• Ask about origin: personal or corporate liquidation"
                ]
            },
            "warning_signs": {
                "title": "🚨 WARNING SIGNS",
                "items": [
                    "• Very loose hinges or squeaking",
                    "• Loose charging port, doesn't hold tight",
                    "• Cracks near hinges (very dangerous)",
                    "• Strange smell (burnt, chemical, musty)",
                    "• Many stripped screws (frequent disassembly)",
                    "• Torn, faded, or missing warranty seals"
                ]
            }
        }
    }
}

BIOS_CHECK_GUIDE = {
    "vi": {
        "title": "🔒 HƯỚNG DẪN KIỂM TRA BIOS - CẢNH BÁO KHÓA BIOS",
        "why": "BIOS là 'não' của máy tính. Máy bị khóa BIOS (đặc biệt ThinkPad) sẽ KHÔNG THỂ SỬ DỤNG hoặc cần chi phí cao để mở khóa. Đây là bẫy phổ biến khi mua laptop cũ doanh nghiệp.",
        "sections": {
            "access": {
                "title": "1️⃣ VÀO BIOS",
                "items": [
                    "• Dell/Alienware: Nhấn F2 hoặc F12 khi khởi động",
                    "• HP/Compaq: Nhấn F10 hoặc ESC",
                    "• Lenovo/ThinkPad: Nhấn F1, F2 hoặc Enter",
                    "• ASUS: Nhấn F2 hoặc Delete",
                    "• Acer: Nhấn F2 hoặc Delete",
                    "• MSI: Nhấn Delete hoặc F2",
                    "• Nhấn liên tục ngay khi bật máy"
                ]
            },
            "performance": {
                "title": "2️⃣ KIỂM TRA HIỆU NĂNG",
                "items": [
                    "• CPU: Intel Turbo Boost/AMD Boost = Enabled",
                    "• RAM: XMP/DOCP profile = Enabled (nếu có)",
                    "• Virtualization: VT-x/AMD-V = Enabled",
                    "• Power Management: Balanced hoặc Performance"
                ]
            },
            "security_critical": {
                "title": "3️⃣ ⚠️ KIỂM TRA KHÓA BIOS (CỰC KỲ QUAN TRỌNG!)",
                "items": [
                    "• Vào menu Security trong BIOS",
                    "• Supervisor Password: NẾU CÓ = MÁY BỊ KHÓA!",
                    "• User Password: Có thể xóa được",
                    "• HDD Password: NẾU CÓ = Ổ cứng bị khóa!",
                    "• Computrace/Absolute: NẾU Enabled = NGUY HIỂM!",
                    "• Computrace có thể khóa máy từ xa qua internet"
                ]
            },
            "thinkpad_warning": {
                "title": "4️⃣ 🚨 ĐẶC BIỆT VỚI THINKPAD",
                "critical": True,
                "items": [
                    "• ThinkPad bị khóa BIOS = KHÔNG THỂ SỬ DỤNG",
                    "• Không thể cài Windows, không boot được",
                    "• Mở khóa cần chip programmer (500k-1 triệu)",
                    "• Hoặc phải thay mainboard (vài triệu)",
                    "• Kiểm tra: Security → Password → Supervisor",
                    "• Nếu yêu cầu password = TRÁNH MUA!",
                    "• Nếu người bán nói 'quên mật khẩu' = LỪA ĐẢO",
                    "• ThinkPad thanh lý công ty thường bị khóa",
                    "• Yêu cầu người bán vào BIOS trước mặt bạn"
                ]
            },
            "unlock_cost": {
                "title": "💰 CHI PHÍ MỞ KHÓA BIOS",
                "items": [
                    "• Chip programmer: 500,000 - 1,000,000 VNĐ",
                    "• Thời gian: 1-3 ngày",
                    "• Rủi ro: Có thể hỏng mainboard (10-20%)",
                    "• Thay mainboard: 2,000,000 - 5,000,000 VNĐ",
                    "• KẾT LUẬN: Không đáng mua máy bị khóa!"
                ]
            },
            "other_checks": {
                "title": "5️⃣ KIỂM TRA KHÁC",
                "items": [
                    "• Boot Mode: UEFI (không phải Legacy)",
                    "• Secure Boot: Enabled (bảo mật)",
                    "• Boot Order: Kiểm tra thứ tự đúng",
                    "• SATA Mode: AHCI (không phải IDE)",
                    "• USB Boot: Enabled (để cài Windows)"
                ]
            },
            "how_to_check": {
                "title": "📋 CÁCH KIỂM TRA AN TOÀN",
                "items": [
                    "• Yêu cầu người bán khởi động máy trước mặt",
                    "• Nhấn phím vào BIOS ngay khi bật máy",
                    "• Nếu yêu cầu password ngay = BỊ KHÓA",
                    "• Vào được BIOS → kiểm tra Security menu",
                    "• Thử thay đổi 1 setting nhỏ (Boot Order)",
                    "• Nếu yêu cầu password khi Save = BỊ KHÓA",
                    "• Không mua nếu không vào được BIOS"
                ]
            }
        }
    },
    "en": {
        "title": "🔒 BIOS CHECK GUIDE - BIOS LOCK WARNING",
        "why": "BIOS is the 'brain' of the computer. A BIOS-locked machine (especially ThinkPad) will be UNUSABLE or require high costs to unlock. This is a common trap when buying used corporate laptops.",
        "sections": {
            "access": {
                "title": "1️⃣ ACCESS BIOS",
                "items": [
                    "• Dell/Alienware: Press F2 or F12 at startup",
                    "• HP/Compaq: Press F10 or ESC",
                    "• Lenovo/ThinkPad: Press F1, F2 or Enter",
                    "• ASUS: Press F2 or Delete",
                    "• Acer: Press F2 or Delete",
                    "• MSI: Press Delete or F2",
                    "• Press repeatedly right when turning on"
                ]
            },
            "performance": {
                "title": "2️⃣ CHECK PERFORMANCE",
                "items": [
                    "• CPU: Intel Turbo Boost/AMD Boost = Enabled",
                    "• RAM: XMP/DOCP profile = Enabled (if available)",
                    "• Virtualization: VT-x/AMD-V = Enabled",
                    "• Power Management: Balanced or Performance"
                ]
            },
            "security_critical": {
                "title": "3️⃣ ⚠️ CHECK BIOS LOCK (EXTREMELY IMPORTANT!)",
                "items": [
                    "• Go to Security menu in BIOS",
                    "• Supervisor Password: IF SET = MACHINE LOCKED!",
                    "• User Password: Can be removed",
                    "• HDD Password: IF SET = Hard drive locked!",
                    "• Computrace/Absolute: IF Enabled = DANGER!",
                    "• Computrace can lock machine remotely via internet"
                ]
            },
            "thinkpad_warning": {
                "title": "4️⃣ 🚨 THINKPAD SPECIFIC WARNING",
                "critical": True,
                "items": [
                    "• ThinkPad with BIOS lock = UNUSABLE",
                    "• Cannot install Windows, cannot boot",
                    "• Unlock requires chip programmer ($50-100)",
                    "• Or must replace motherboard ($200-500)",
                    "• Check: Security → Password → Supervisor",
                    "• If password required = AVOID PURCHASE!",
                    "• If seller says 'forgot password' = SCAM",
                    "• Corporate liquidation ThinkPads often locked",
                    "• Demand seller access BIOS in front of you"
                ]
            },
            "unlock_cost": {
                "title": "💰 BIOS UNLOCK COSTS",
                "items": [
                    "• Chip programmer: $50 - $100",
                    "• Time: 1-3 days",
                    "• Risk: May damage motherboard (10-20%)",
                    "• Replace motherboard: $200 - $500",
                    "• CONCLUSION: Not worth buying locked machine!"
                ]
            },
            "other_checks": {
                "title": "5️⃣ OTHER CHECKS",
                "items": [
                    "• Boot Mode: UEFI (not Legacy)",
                    "• Secure Boot: Enabled (security)",
                    "• Boot Order: Check correct order",
                    "• SATA Mode: AHCI (not IDE)",
                    "• USB Boot: Enabled (for Windows install)"
                ]
            },
            "how_to_check": {
                "title": "📋 HOW TO CHECK SAFELY",
                "items": [
                    "• Ask seller to boot machine in front of you",
                    "• Press BIOS key right when turning on",
                    "• If password required immediately = LOCKED",
                    "• Access BIOS → check Security menu",
                    "• Try changing 1 small setting (Boot Order)",
                    "• If password required when Save = LOCKED",
                    "• Don't buy if cannot access BIOS"
                ]
            }
        }
    }
}

def get_physical_guide(lang="vi"):
    """Get physical inspection guide in specified language"""
    return PHYSICAL_INSPECTION_GUIDE.get(lang, PHYSICAL_INSPECTION_GUIDE["vi"])

def get_bios_guide(lang="vi"):
    """Get BIOS check guide in specified language"""
    return BIOS_CHECK_GUIDE.get(lang, BIOS_CHECK_GUIDE["vi"])

def format_guide_for_display(guide_data):
    """Format guide data for display in UI"""
    output = []
    output.append(f"\n{'='*60}")
    output.append(guide_data["title"])
    output.append(f"{'='*60}\n")
    
    if "why" in guide_data:
        output.append(f"❓ TẠI SAO QUAN TRỌNG:")
        output.append(f"{guide_data['why']}\n")
    
    for section_key, section_data in guide_data["sections"].items():
        output.append(f"\n{section_data['title']}")
        output.append("-" * 50)
        
        if section_data.get("critical"):
            output.append("⚠️⚠️⚠️ CỰC KỲ QUAN TRỌNG ⚠️⚠️⚠️")
        
        for item in section_data["items"]:
            output.append(item)
        output.append("")
    
    return "\n".join(output)

if __name__ == "__main__":
    # Test display
    print(format_guide_for_display(get_physical_guide("vi")))
    print("\n" + "="*80 + "\n")
    print(format_guide_for_display(get_bios_guide("vi")))
