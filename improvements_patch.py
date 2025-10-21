"""
Patch file để cải tiến LaptopTester:
1. Cải thiện màu chữ của nút bấm (trước và sau khi bấm)
2. Bổ sung nhận định về khả năng xử lý tác vụ dựa trên RAM, CPU, GPU
"""

# ============================================================================
# PHẦN 1: CẢI THIỆN MÀU CHỮ CỦA NÚT BẤM
# ============================================================================

# Thêm vào class Theme (sau dòng 430):
"""
    # Button text colors - Enhanced visibility
    BUTTON_TEXT_NORMAL = "#ffffff"  # White text for normal state
    BUTTON_TEXT_HOVER = "#ffffff"   # White text for hover state  
    BUTTON_TEXT_PRESSED = "#e6e6e6" # Slightly dimmed for pressed state
    BUTTON_TEXT_DISABLED = "#8b949e" # Gray for disabled state
"""

# ============================================================================
# PHẦN 2: NHẬN ĐỊNH KHẢ NĂNG XỬ LÝ TÁC VỤ
# ============================================================================

def analyze_hardware_capability(cpu_info, ram_gb, gpu_info):
    """
    Phân tích khả năng xử lý tác vụ dựa trên cấu hình phần cứng
    
    Args:
        cpu_info: Thông tin CPU (string)
        ram_gb: Dung lượng RAM (float)
        gpu_info: Thông tin GPU (string)
    
    Returns:
        dict: {
            'office': {'level': 'Excellent/Good/Average/Poor', 'details': '...'},
            'design': {...},
            'gaming': {...},
            'programming': {...},
            'video_editing': {...}
        }
    """
    
    # Phân tích CPU
    cpu_score = 0
    cpu_cores = 0
    cpu_threads = 0
    
    if cpu_info:
        cpu_lower = cpu_info.lower()
        
        # Detect cores and threads
        if '(' in cpu_info and 'c/' in cpu_info.lower():
            try:
                parts = cpu_info.split('(')[1].split(')')[0]
                if 'c/' in parts.lower():
                    core_thread = parts.lower().split('c/')
                    cpu_cores = int(core_thread[0].strip())
                    cpu_threads = int(core_thread[1].split('t')[0].strip())
            except:
                pass
        
        # CPU generation and tier scoring
        if 'i9' in cpu_lower or 'ryzen 9' in cpu_lower or 'threadripper' in cpu_lower:
            cpu_score = 95
        elif 'i7' in cpu_lower or 'ryzen 7' in cpu_lower:
            cpu_score = 85
        elif 'i5' in cpu_lower or 'ryzen 5' in cpu_lower:
            cpu_score = 70
        elif 'i3' in cpu_lower or 'ryzen 3' in cpu_lower:
            cpu_score = 50
        elif 'celeron' in cpu_lower or 'pentium' in cpu_lower or 'atom' in cpu_lower:
            cpu_score = 30
        else:
            cpu_score = 60  # Default for unknown
        
        # Adjust by generation (newer = better)
        for gen in range(13, 7, -1):  # Intel 13th to 8th gen
            if f'{gen}th' in cpu_lower or f'gen {gen}' in cpu_lower or f'-{gen}' in cpu_lower:
                cpu_score += (gen - 8) * 2
                break
        
        # AMD Ryzen generation
        if 'ryzen' in cpu_lower:
            for gen in range(7000, 2000, -1000):
                if str(gen) in cpu_info:
                    cpu_score += (gen - 2000) // 1000 * 3
                    break
    
    # Phân tích GPU
    gpu_score = 0
    has_dedicated_gpu = False
    
    if gpu_info:
        gpu_lower = gpu_info.lower()
        
        # Check for dedicated GPU
        if any(x in gpu_lower for x in ['nvidia', 'geforce', 'rtx', 'gtx', 'radeon rx', 'radeon pro']):
            has_dedicated_gpu = True
            
            # NVIDIA scoring
            if 'rtx 40' in gpu_lower:
                gpu_score = 95
            elif 'rtx 30' in gpu_lower:
                gpu_score = 90
            elif 'rtx 20' in gpu_lower or 'gtx 16' in gpu_lower:
                gpu_score = 80
            elif 'gtx 10' in gpu_lower:
                gpu_score = 70
            elif 'gtx 9' in gpu_lower or 'gtx 7' in gpu_lower:
                gpu_score = 50
            elif 'mx' in gpu_lower:  # MX series (entry level)
                gpu_score = 40
            
            # AMD scoring
            elif 'rx 7' in gpu_lower:
                gpu_score = 90
            elif 'rx 6' in gpu_lower:
                gpu_score = 85
            elif 'rx 5' in gpu_lower:
                gpu_score = 75
            elif 'rx 4' in gpu_lower or 'rx 3' in gpu_lower:
                gpu_score = 60
            else:
                gpu_score = 65  # Default dedicated GPU
        else:
            # Integrated GPU
            if 'iris xe' in gpu_lower or 'iris plus' in gpu_lower:
                gpu_score = 45
            elif 'uhd' in gpu_lower or 'hd graphics' in gpu_lower:
                gpu_score = 30
            elif 'vega' in gpu_lower:
                gpu_score = 40
            else:
                gpu_score = 25
    
    # Phân tích RAM
    ram_score = 0
    if ram_gb >= 32:
        ram_score = 95
    elif ram_gb >= 16:
        ram_score = 85
    elif ram_gb >= 8:
        ram_score = 65
    elif ram_gb >= 4:
        ram_score = 40
    else:
        ram_score = 20
    
    # Tính điểm tổng hợp cho từng tác vụ
    capabilities = {}
    
    # 1. Văn phòng (Office Work)
    office_score = (cpu_score * 0.3 + ram_score * 0.6 + gpu_score * 0.1)
    if office_score >= 80:
        capabilities['office'] = {
            'level': 'Xuất sắc',
            'icon': '🌟',
            'color': '#238636',
            'tasks': 'Word, Excel, PowerPoint, Email, Web browsing, Video calls (Zoom/Teams)',
            'details': f'Xử lý mượt mà {cpu_cores}+ tabs Chrome, multitasking tốt'
        }
    elif office_score >= 60:
        capabilities['office'] = {
            'level': 'Tốt',
            'icon': '✅',
            'color': '#238636',
            'tasks': 'Word, Excel, PowerPoint, Email, Web browsing',
            'details': 'Đủ cho công việc văn phòng hàng ngày'
        }
    elif office_score >= 40:
        capabilities['office'] = {
            'level': 'Trung bình',
            'icon': '⚠️',
            'color': '#d29922',
            'tasks': 'Word, Excel cơ bản, Email',
            'details': 'Có thể chậm khi mở nhiều ứng dụng cùng lúc'
        }
    else:
        capabilities['office'] = {
            'level': 'Yếu',
            'icon': '❌',
            'color': '#f85149',
            'tasks': 'Chỉ phù hợp cho tác vụ nhẹ',
            'details': 'Sẽ lag khi multitasking'
        }
    
    # 2. Thiết kế đồ họa (Graphic Design)
    design_score = (cpu_score * 0.3 + ram_score * 0.4 + gpu_score * 0.3)
    if design_score >= 80 and ram_gb >= 16 and has_dedicated_gpu:
        capabilities['design'] = {
            'level': 'Xuất sắc',
            'icon': '🌟',
            'color': '#238636',
            'tasks': 'Photoshop, Illustrator, InDesign, Figma, Canva Pro',
            'details': f'Xử lý file lớn mượt, {ram_gb}GB RAM đủ cho nhiều layer'
        }
    elif design_score >= 60 and ram_gb >= 8:
        capabilities['design'] = {
            'level': 'Tốt',
            'icon': '✅',
            'color': '#238636',
            'tasks': 'Photoshop, Illustrator, Canva',
            'details': 'Đủ cho thiết kế 2D, có thể chậm với file phức tạp'
        }
    elif design_score >= 40:
        capabilities['design'] = {
            'level': 'Trung bình',
            'icon': '⚠️',
            'color': '#d29922',
            'tasks': 'Canva, GIMP, thiết kế đơn giản',
            'details': 'Chỉ phù hợp cho thiết kế nhẹ, sẽ lag với Photoshop'
        }
    else:
        capabilities['design'] = {
            'level': 'Không phù hợp',
            'icon': '❌',
            'color': '#f85149',
            'tasks': 'Không khuyến nghị',
            'details': 'Cấu hình quá yếu cho thiết kế đồ họa'
        }
    
    # 3. Gaming
    gaming_score = (cpu_score * 0.25 + ram_score * 0.25 + gpu_score * 0.5)
    if gaming_score >= 85 and has_dedicated_gpu and ram_gb >= 16:
        capabilities['gaming'] = {
            'level': 'Xuất sắc',
            'icon': '🌟',
            'color': '#238636',
            'tasks': 'AAA games (High/Ultra), Cyberpunk 2077, Elden Ring, GTA V',
            'details': f'Chơi game nặng 60+ FPS, GPU {gpu_info.split(";")[0] if ";" in gpu_info else gpu_info[:30]}'
        }
    elif gaming_score >= 65 and has_dedicated_gpu:
        capabilities['gaming'] = {
            'level': 'Tốt',
            'icon': '✅',
            'color': '#238636',
            'tasks': 'Game trung bình (Medium/High), Valorant, CS:GO, Dota 2',
            'details': 'Chơi được game phổ thông, AAA games cần giảm setting'
        }
    elif gaming_score >= 45:
        capabilities['gaming'] = {
            'level': 'Trung bình',
            'icon': '⚠️',
            'color': '#d29922',
            'tasks': 'Game nhẹ (Low), League of Legends, Minecraft',
            'details': 'Chỉ chơi được game nhẹ hoặc game cũ'
        }
    else:
        capabilities['gaming'] = {
            'level': 'Không phù hợp',
            'icon': '❌',
            'color': '#f85149',
            'tasks': 'Không khuyến nghị',
            'details': 'Cấu hình quá yếu cho gaming'
        }
    
    # 4. Lập trình (Programming)
    prog_score = (cpu_score * 0.4 + ram_score * 0.5 + gpu_score * 0.1)
    if prog_score >= 80 and ram_gb >= 16:
        capabilities['programming'] = {
            'level': 'Xuất sắc',
            'icon': '🌟',
            'color': '#238636',
            'tasks': 'Full-stack, Android Studio, Docker, VM, AI/ML',
            'details': f'{cpu_cores}+ cores tốt cho compile, {ram_gb}GB RAM đủ chạy nhiều container'
        }
    elif prog_score >= 60 and ram_gb >= 8:
        capabilities['programming'] = {
            'level': 'Tốt',
            'icon': '✅',
            'color': '#238636',
            'tasks': 'Web dev, Python, Java, VS Code, Git',
            'details': 'Đủ cho lập trình thông thường, có thể chậm với Android Studio'
        }
    elif prog_score >= 40:
        capabilities['programming'] = {
            'level': 'Trung bình',
            'icon': '⚠️',
            'color': '#d29922',
            'tasks': 'Web dev nhẹ, Python, VS Code',
            'details': 'Chỉ phù hợp cho project nhỏ, compile chậm'
        }
    else:
        capabilities['programming'] = {
            'level': 'Yếu',
            'icon': '❌',
            'color': '#f85149',
            'tasks': 'Chỉ code đơn giản',
            'details': 'Sẽ rất chậm với IDE nặng'
        }
    
    # 5. Chỉnh sửa video (Video Editing)
    video_score = (cpu_score * 0.35 + ram_score * 0.35 + gpu_score * 0.3)
    if video_score >= 85 and ram_gb >= 16 and has_dedicated_gpu:
        capabilities['video_editing'] = {
            'level': 'Xuất sắc',
            'icon': '🌟',
            'color': '#238636',
            'tasks': 'Premiere Pro, DaVinci Resolve, After Effects, 4K editing',
            'details': f'Export nhanh, xử lý 4K mượt với {cpu_cores} cores + GPU'
        }
    elif video_score >= 65 and ram_gb >= 8:
        capabilities['video_editing'] = {
            'level': 'Tốt',
            'icon': '✅',
            'color': '#238636',
            'tasks': 'Premiere Pro, DaVinci Resolve, 1080p editing',
            'details': 'Đủ cho edit 1080p, 4K sẽ chậm'
        }
    elif video_score >= 45:
        capabilities['video_editing'] = {
            'level': 'Trung bình',
            'icon': '⚠️',
            'color': '#d29922',
            'tasks': 'CapCut, Filmora, 720p editing',
            'details': 'Chỉ phù hợp cho edit video đơn giản, export chậm'
        }
    else:
        capabilities['video_editing'] = {
            'level': 'Không phù hợp',
            'icon': '❌',
            'color': '#f85149',
            'tasks': 'Không khuyến nghị',
            'details': 'Cấu hình quá yếu cho chỉnh sửa video'
        }
    
    return capabilities


# ============================================================================
# PHẦN 3: HTML TEMPLATE CHO NHẬN ĐỊNH
# ============================================================================

def generate_capability_html(capabilities):
    """Tạo HTML hiển thị nhận định khả năng xử lý"""
    
    html = """
    <div style='background: #161b22; padding: 20px; border-radius: 8px; margin: 10px 0;'>
        <h2 style='color: #58a6ff; margin-bottom: 15px; font-size: 22px;'>
            🎯 NHẬN ĐỊNH KHẢ NĂNG XỬ LÝ TÁC VỤ
        </h2>
        <p style='color: #8b949e; margin-bottom: 20px; font-size: 16px;'>
            Dựa trên cấu hình CPU, RAM, GPU - Đánh giá khả năng xử lý các tác vụ phổ biến:
        </p>
    """
    
    categories = [
        ('office', '💼 Văn phòng'),
        ('programming', '💻 Lập trình'),
        ('design', '🎨 Thiết kế đồ họa'),
        ('video_editing', '🎬 Chỉnh sửa video'),
        ('gaming', '🎮 Gaming')
    ]
    
    for key, title in categories:
        if key in capabilities:
            cap = capabilities[key]
            html += f"""
        <div style='background: #21262d; padding: 15px; border-radius: 6px; margin: 10px 0; border-left: 4px solid {cap["color"]};'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                <h3 style='color: #f0f6fc; margin: 0; font-size: 18px;'>{title}</h3>
                <span style='color: {cap["color"]}; font-weight: bold; font-size: 16px;'>
                    {cap["icon"]} {cap["level"]}
                </span>
            </div>
            <p style='color: #c9d1d9; margin: 8px 0; font-size: 15px;'>
                <strong>Tác vụ:</strong> {cap["tasks"]}
            </p>
            <p style='color: #8b949e; margin: 8px 0 0 0; font-size: 14px; font-style: italic;'>
                {cap["details"]}
            </p>
        </div>
            """
    
    html += """
        <div style='background: #1f6feb; padding: 12px; border-radius: 6px; margin-top: 15px;'>
            <p style='color: white; margin: 0; font-size: 14px;'>
                💡 <strong>Lưu ý:</strong> Đánh giá dựa trên thông số phần cứng. 
                Hiệu năng thực tế còn phụ thuộc vào tản nhiệt, driver, và tình trạng máy.
            </p>
        </div>
    </div>
    """
    
    return html


# ============================================================================
# HƯỚNG DẪN TÍCH HỢP
# ============================================================================

"""
CÁCH TÍCH HỢP VÀO main_enhanced_auto.py:

1. Thêm màu chữ nút bấm vào class Theme (dòng ~430)

2. Cập nhật tất cả các nút bấm để sử dụng text_color:
   
   # Thay vì:
   ctk.CTkButton(parent, text="Text", fg_color=Theme.SUCCESS)
   
   # Sử dụng:
   ctk.CTkButton(parent, text="Text", fg_color=Theme.SUCCESS, 
                 text_color=Theme.BUTTON_TEXT_NORMAL,
                 hover_color="#1a7f37")

3. Trong HardwareFingerprintStep.display_info() (dòng ~1240):
   
   Thêm sau khi hiển thị thông tin phần cứng:
   
   # Phân tích khả năng xử lý
   try:
       cpu_info = hw_info.get("CPU", "")
       ram_str = hw_info.get("RAM", "0GB")
       ram_gb = float(ram_str.split("GB")[0]) if "GB" in ram_str else 0
       gpu_info = hw_info.get("GPU", "")
       
       capabilities = analyze_hardware_capability(cpu_info, ram_gb, gpu_info)
       
       # Hiển thị nhận định
       capability_frame = ctk.CTkFrame(self.container, fg_color=Theme.INFO, corner_radius=8)
       capability_frame.grid(row=len(self.info_items)+2, column=0, sticky="ew", pady=10, padx=20)
       
       # Tạo scrollable text widget để hiển thị HTML-like content
       cap_label = ctk.CTkLabel(capability_frame, 
                                text="🎯 NHẬN ĐỊNH KHẢ NĂNG XỬ LÝ TÁC VỤ",
                                font=Theme.HEADING_FONT,
                                text_color="white")
       cap_label.pack(pady=10)
       
       # Hiển thị từng category
       for key, title in [('office', '💼 Văn phòng'), ('programming', '💻 Lập trình'),
                          ('design', '🎨 Thiết kế'), ('video_editing', '🎬 Video'),
                          ('gaming', '🎮 Gaming')]:
           if key in capabilities:
               cap = capabilities[key]
               
               cat_frame = ctk.CTkFrame(capability_frame, fg_color=Theme.FRAME, corner_radius=6)
               cat_frame.pack(fill="x", padx=15, pady=5)
               
               # Title and level
               header = ctk.CTkFrame(cat_frame, fg_color="transparent")
               header.pack(fill="x", padx=10, pady=8)
               
               ctk.CTkLabel(header, text=title, font=Theme.SUBHEADING_FONT).pack(side="left")
               ctk.CTkLabel(header, text=f"{cap['icon']} {cap['level']}", 
                           font=Theme.BODY_FONT, text_color=cap['color']).pack(side="right")
               
               # Tasks
               ctk.CTkLabel(cat_frame, text=f"Tác vụ: {cap['tasks']}", 
                           font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY,
                           wraplength=700, justify="left").pack(anchor="w", padx=10, pady=2)
               
               # Details
               ctk.CTkLabel(cat_frame, text=cap['details'], 
                           font=Theme.SMALL_FONT, text_color=Theme.TEXT_SECONDARY,
                           wraplength=700, justify="left").pack(anchor="w", padx=10, pady=(0,8))
       
       # Note
       note_frame = ctk.CTkFrame(capability_frame, fg_color=Theme.ACCENT, corner_radius=6)
       note_frame.pack(fill="x", padx=15, pady=10)
       ctk.CTkLabel(note_frame, 
                   text="💡 Lưu ý: Đánh giá dựa trên thông số phần cứng. Hiệu năng thực tế phụ thuộc tản nhiệt, driver.",
                   font=Theme.SMALL_FONT, text_color="white",
                   wraplength=700, justify="left").pack(padx=10, pady=8)
       
   except Exception as e:
       print(f"Error analyzing capabilities: {e}")

4. Import hàm analyze_hardware_capability vào đầu file main_enhanced_auto.py
"""

print("✅ Patch file created successfully!")
print("📝 Đọc phần HƯỚNG DẪN TÍCH HỢP ở cuối file để áp dụng các cải tiến.")
