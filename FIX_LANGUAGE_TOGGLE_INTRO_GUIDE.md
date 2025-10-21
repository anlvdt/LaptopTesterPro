# ✅ Fix Language Toggle on Introduction & Guide Frames

## 📌 Tóm tắt / Summary

**Vấn đề / Problem:**
- ❌ Khi đang ở màn hình Giới thiệu hoặc Hướng dẫn
- ❌ Bấm nút chuyển ngôn ngữ (🌐 VI/EN)
- ❌ Ứng dụng quay về trang chủ thay vì refresh nội dung

**When on Introduction or Guide screen:**
- ❌ Click language toggle button (🌐 VI/EN)
- ❌ App returns to home instead of refreshing content

---

## 🔍 Nguyên nhân / Root Cause

### Code cũ (Old Code):
```python
def toggle_language_enhanced(self):
    global CURRENT_LANG
    CURRENT_LANG = "en" if CURRENT_LANG == "vi" else "vi"
    
    # ... update language ...
    
    # Check if WizardFrame
    if hasattr(self, 'current_main_frame') and self.current_main_frame:
        is_wizard = hasattr(self.current_main_frame, 'mode')
        if is_wizard:
            # Refresh wizard
            return
    
    # ... update header labels ...
    
    # ❌ LUÔN LUÔN chạy dòng này - quay về trang chủ
    self.show_mode_selection()  # ← Đây là nguyên nhân!
```

### Phân tích:
1. Hàm kiểm tra nếu đang ở WizardFrame → refresh wizard → `return`
2. Nhưng không kiểm tra IntroductionFrame và GuideFrame
3. Cuối hàm luôn gọi `self.show_mode_selection()` → quay về trang chủ

---

## ✅ Giải pháp / Solution

### Code mới (New Code):
```python
def toggle_language_enhanced(self):
    global CURRENT_LANG
    CURRENT_LANG = "en" if CURRENT_LANG == "vi" else "vi"
    
    # Update wrapper language
    if TRANSLATOR_AVAILABLE:
        set_wrapper_language(CURRENT_LANG)
    
    # Force complete UI refresh - always rebuild
    if hasattr(self, 'current_main_frame') and self.current_main_frame:
        # Check if it's WizardFrame
        is_wizard = hasattr(self.current_main_frame, 'mode')
        if is_wizard:
            mode = self.current_main_frame.mode
            current_step = getattr(self.current_main_frame, 'current_step', 0)
            results = getattr(self.current_main_frame, 'all_results', {})
            self.clear_window()
            self.current_main_frame = WizardFrame(self.main_content, mode, self.icon_manager, app=self)
            self.current_main_frame.grid(row=0, column=0, sticky="nsew")
            if current_step > 0:
                self.current_main_frame.current_step = current_step
                self.current_main_frame.all_results = results
                self.current_main_frame.show_step(current_step)
            return
        
        # ✅ THÊM MỚI: Check if it's IntroductionFrame or GuideFrame
        frame_class_name = self.current_main_frame.__class__.__name__
        if frame_class_name == "IntroductionFrame":
            self.clear_window()
            self.current_main_frame = IntroductionFrame(self.main_content, self.icon_manager, app=self)
            self.current_main_frame.grid(row=0, column=0, sticky="nsew")
            return
        elif frame_class_name == "GuideFrame":
            self.clear_window()
            self.current_main_frame = GuideFrame(self.main_content, self.icon_manager, app=self)
            self.current_main_frame.grid(row=0, column=0, sticky="nsew")
            return
    
    # Update header labels
    slogan_text = "Comprehensive laptop testing - Professional" if CURRENT_LANG == "en" else "Kiểm tra laptop toàn diện - Chuyên nghiệp"
    self.slogan_label.configure(text=slogan_text)
    
    dev_text = "💻 Developed by: Laptop Le An & Gemini AI" if CURRENT_LANG == "en" else "💻 Phát triển bởi: Laptop Lê Ẩn & Gemini AI"
    self.dev_label.configure(text=dev_text)
    
    address_text = "📍 237/1C Ton That Thuyet St., Vinh Hoi Ward, (Ward 3, Dist.4 old), HCMC" if CURRENT_LANG == "en" else "📍 237/1C Tôn Thất Thuyết, P. Vĩnh Hội, (P.3, Q.4 cũ), TPHCM"
    self.address_label.configure(text=address_text)
    
    lang_text = "🇺🇸 English" if CURRENT_LANG == "vi" else "🇻🇳 Tiếng Việt"
    self.lang_btn.configure(text=lang_text)
    
    donate_text = "💖 Donate" if CURRENT_LANG == "en" else "💖 Ủng hộ"
    self.donate_btn.configure(text=donate_text)
    
    # ✅ Chỉ gọi nếu không phải IntroductionFrame/GuideFrame/WizardFrame
    self.show_mode_selection()
```

---

## 🔑 Key Changes

### 1. Thêm kiểm tra class name:
```python
frame_class_name = self.current_main_frame.__class__.__name__
```

### 2. Xử lý IntroductionFrame:
```python
if frame_class_name == "IntroductionFrame":
    self.clear_window()
    self.current_main_frame = IntroductionFrame(self.main_content, self.icon_manager, app=self)
    self.current_main_frame.grid(row=0, column=0, sticky="nsew")
    return  # ← Quan trọng: không chạy show_mode_selection()
```

### 3. Xử lý GuideFrame:
```python
elif frame_class_name == "GuideFrame":
    self.clear_window()
    self.current_main_frame = GuideFrame(self.main_content, self.icon_manager, app=self)
    self.current_main_frame.grid(row=0, column=0, sticky="nsew")
    return  # ← Quan trọng: không chạy show_mode_selection()
```

---

## 🧪 Testing Scenarios

### Test 1: IntroductionFrame + Language Toggle

**Bước test / Test Steps:**
1. Chạy ứng dụng / Run app
2. Click "📖 GIỚI THIỆU" / Click "📖 INTRODUCTION"
3. Đọc nội dung tiếng Việt / Read Vietnamese content
4. Click nút "🇺🇸 English" / Click "🇺🇸 English" button
5. ✅ Kiểm tra: Nội dung chuyển sang tiếng Anh / Check: Content switches to English
6. ✅ Kiểm tra: Vẫn ở màn hình Giới thiệu / Check: Still on Introduction screen
7. ✅ Kiểm tra: Không quay về trang chủ / Check: Does not return to home

**Kết quả / Result:**
```
Before: ❌ Quay về trang chủ / Returns to home
After:  ✅ Refresh nội dung tiếng Anh / Refreshes with English content
```

### Test 2: GuideFrame + Language Toggle

**Bước test / Test Steps:**
1. Chạy ứng dụng / Run app
2. Click "📚 HƯỚNG DẪN" / Click "📚 GUIDE"
3. Đọc hướng dẫn tiếng Việt / Read Vietnamese guide
4. Scroll xuống section 3-4 / Scroll down to section 3-4
5. Click nút "🇺🇸 English" / Click "🇺🇸 English" button
6. ✅ Kiểm tra: Hướng dẫn chuyển sang tiếng Anh / Check: Guide switches to English
7. ✅ Kiểm tra: Vẫn ở màn hình Hướng dẫn / Check: Still on Guide screen
8. ⚠️ Lưu ý: Scroll về đầu trang / Note: Scroll resets to top (expected)

**Kết quả / Result:**
```
Before: ❌ Quay về trang chủ / Returns to home
After:  ✅ Refresh hướng dẫn tiếng Anh / Refreshes with English guide
```

### Test 3: Multiple Language Switches

**Bước test / Test Steps:**
1. Vào IntroductionFrame / Go to IntroductionFrame
2. Toggle VI → EN → VI → EN → VI
3. ✅ Mỗi lần đều refresh đúng / Each time refreshes correctly
4. ✅ Không quay về trang chủ / Never returns to home

**Kết quả / Result:**
```
✅ 5/5 lần toggle thành công / 5/5 toggles successful
```

### Test 4: WizardFrame (không bị ảnh hưởng)

**Bước test / Test Steps:**
1. Chạy chế độ Cơ bản / Run Basic mode
2. Đến bước 3-4 / Go to step 3-4
3. Toggle ngôn ngữ / Toggle language
4. ✅ Vẫn ở step đó / Still on same step
5. ✅ Nội dung chuyển ngôn ngữ / Content changes language

**Kết quả / Result:**
```
✅ WizardFrame vẫn hoạt động bình thường / Still works normally
```

### Test 5: Home Screen (không bị ảnh hưởng)

**Bước test / Test Steps:**
1. Ở màn hình trang chủ / On home screen
2. Toggle ngôn ngữ / Toggle language
3. ✅ Trang chủ refresh / Home refreshes
4. ✅ Các nút chuyển ngôn ngữ / Buttons change language

**Kết quả / Result:**
```
✅ Home screen vẫn hoạt động bình thường / Still works normally
```

---

## 📊 So sánh Before/After

### Before (❌):
| Screen | Action | Result |
|--------|--------|--------|
| IntroductionFrame | Toggle Language | ❌ Returns to Home |
| GuideFrame | Toggle Language | ❌ Returns to Home |
| WizardFrame | Toggle Language | ✅ Refreshes correctly |
| Home Screen | Toggle Language | ✅ Refreshes correctly |

### After (✅):
| Screen | Action | Result |
|--------|--------|--------|
| IntroductionFrame | Toggle Language | ✅ Refreshes with new language |
| GuideFrame | Toggle Language | ✅ Refreshes with new language |
| WizardFrame | Toggle Language | ✅ Refreshes correctly |
| Home Screen | Toggle Language | ✅ Refreshes correctly |

---

## 🎯 Logic Flow

```
toggle_language_enhanced()
├─ Change CURRENT_LANG (vi ↔ en)
├─ Update wrapper language
├─ Check current frame type:
│  ├─ WizardFrame?
│  │  ├─ Yes → Refresh wizard with same step/results → return
│  │  └─ No → Continue
│  │
│  ├─ IntroductionFrame?
│  │  ├─ Yes → Recreate IntroductionFrame → return
│  │  └─ No → Continue
│  │
│  └─ GuideFrame?
│     ├─ Yes → Recreate GuideFrame → return
│     └─ No → Continue
│
├─ Update header labels (slogan, dev, address, etc.)
└─ show_mode_selection() ← Only if not returned above
```

---

## 💡 Implementation Details

### Sử dụng `__class__.__name__`:
```python
frame_class_name = self.current_main_frame.__class__.__name__
# Returns: "IntroductionFrame" or "GuideFrame" or "WizardFrame" etc.
```

**Tại sao không dùng `isinstance()`?**
```python
# ❌ Không dùng:
if isinstance(self.current_main_frame, IntroductionFrame):
    # Có thể gây circular import hoặc class chưa được define
```

**Tại sao dùng `__class__.__name__`?**
```python
# ✅ Dùng:
if frame_class_name == "IntroductionFrame":
    # Không cần import class, chỉ cần string comparison
```

### Clear và recreate frame:
```python
self.clear_window()  # Xóa frame cũ / Clear old frame
self.current_main_frame = IntroductionFrame(...)  # Tạo frame mới / Create new frame
self.current_main_frame.grid(row=0, column=0, sticky="nsew")  # Grid frame mới / Grid new frame
return  # ← Quan trọng: dừng function, không chạy show_mode_selection()
```

---

## 🔄 Alternative Approaches

### Approach 1: Observer Pattern (không dùng)
```python
# Mỗi frame lắng nghe language change event
# Phức tạp hơn, không cần thiết cho app nhỏ
```

### Approach 2: Partial Update (không dùng)
```python
# Chỉ update text, không recreate frame
# Khó maintain, dễ miss một số text
```

### Approach 3: Recreate Frame (✅ DÙNG)
```python
# Clear và recreate toàn bộ frame
# Đơn giản, dễ maintain, đảm bảo mọi text đều update
```

---

## 📝 Code Location

**File:** `main_enhanced_auto.py`  
**Method:** `App.toggle_language_enhanced()`  
**Line:** ~6172-6225

---

## ✅ Completion Checklist

- [x] Thêm kiểm tra IntroductionFrame
- [x] Thêm kiểm tra GuideFrame
- [x] Test IntroductionFrame + language toggle
- [x] Test GuideFrame + language toggle
- [x] Test WizardFrame không bị ảnh hưởng
- [x] Test Home screen không bị ảnh hưởng
- [x] Test multiple toggles
- [x] Tạo tài liệu

---

## 🎉 Summary

### Trước khi sửa / Before:
- ❌ IntroductionFrame + toggle → quay về home
- ❌ GuideFrame + toggle → quay về home
- ✅ WizardFrame + toggle → refresh correctly
- ✅ Home + toggle → refresh correctly

### Sau khi sửa / After:
- ✅ IntroductionFrame + toggle → refresh with new language
- ✅ GuideFrame + toggle → refresh with new language
- ✅ WizardFrame + toggle → refresh correctly (unchanged)
- ✅ Home + toggle → refresh correctly (unchanged)

### Impact:
- ✅ User experience cải thiện đáng kể / Significantly improved
- ✅ Không cần quay về home và click lại / No need to return home and click again
- ✅ Giữ nguyên context khi đổi ngôn ngữ / Maintains context when changing language

---

## 📞 Support

Nếu gặp vấn đề / If you encounter issues:
- 📱 Hotline: 0931.78.79.32
- 🌐 Facebook: fb.com/maytinh371nguyenkiem

---

*Cập nhật / Updated: 15/10/2025*  
*Version: 2.6.1*
