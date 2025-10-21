# Contributing to LaptopTester Pro

Cảm ơn bạn đã quan tâm đóng góp cho LaptopTester Pro! Dưới đây là hướng dẫn chi tiết.

## 🤝 Các Cách Đóng Góp

### 1. Báo Cáo Lỗi
- Sử dụng [GitHub Issues](../../issues)
- Mô tả rõ: OS, Version, Cách tái hiện
- Thêm screenshots nếu có
- Kiểm tra lỗi tương tự không bị report trước

### 2. Đề Xuất Tính Năng
- Mở Issue với title rõ ràng
- Giải thích bài toán cần giải quyết
- Mô tả giải pháp đề xuất
- Liệt kê các lợi ích

### 3. Cải Thiện Code
- Fork repository
- Tạo feature branch: `git checkout -b feature/amazing`
- Commit changes: `git commit -m 'Add amazing feature'`
- Push: `git push origin feature/amazing`
- Mở Pull Request

### 4. Cải Thiện Tài Liệu
- Sửa typos, lỗi ngữ pháp
- Cải thiện hướng dẫn, ví dụ
- Thêm bản dịch mới
- Cập nhật changelog

---

## 📋 Pull Request Process

### Trước khi Submit PR:

1. **Code Quality**
   ```bash
   # Kiểm tra syntax
   python -m py_compile your_file.py
   ```

2. **Commit Message Format**
   ```
   [TYPE] Description
   
   - Details about change
   - Why this change
   - Any breaking changes
   
   Types: feat, fix, docs, style, refactor, test, chore
   ```

3. **Keep it focused**
   - 1 feature/fix per PR
   - Tránh mixing concerns
   - Rebase trước submit

### PR Description Template:

```markdown
## Description
[Mô tả thay đổi]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactor

## Testing
- [ ] Tested on Windows 10
- [ ] Tested on Windows 11
- [ ] All 16 tests work

## Screenshots (nếu có)
[Thêm screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] No new warnings generated
- [ ] Updated documentation
- [ ] Backward compatible
```

---

## 🎯 Development Guidelines

### Code Style
```python
# PEP 8 compliant
# Indent: 4 spaces
# Max line length: 100 characters

class MyClass:
    """Clear docstrings."""
    
    def my_method(self):
        """Method description."""
        pass
```

### Adding a New Test Step

1. **Create Step Class**
   ```python
   class MyTestStep(BaseStepFrame):
       def __init__(self, master, **kwargs):
           kwargs["step_key"] = "my_test"  # IMPORTANT!
           title = get_text("my_test")
           super().__init__(master, title, why_text, how_text, **kwargs)
   ```

2. **Implement Methods**
   ```python
   def on_show(self):
       """Called when step is shown"""
       pass
   
   def mark_completed(self, result_data, auto_advance=False):
       """Mark step as completed"""
       pass
   ```

3. **Add to Steps List**
   - Update `AppMain.show_step()` list

4. **Add Translations**
   - Update `LANG` dictionary với key
   - Vietnamese & English

### Important: step_key Architecture

```python
# ✅ CORRECT - Use fixed step_key
kwargs["step_key"] = "my_test"  # Constant, never changes

# ❌ WRONG - Use translated title
# Title changes with language!
```

**Why?** 
- Results dict keys không thay đổi khi đổi ngôn ngữ
- Report lookup hoạt động nhất quán
- Database/export không bị lỗi

---

## 🧪 Testing

### Run Tests Locally
```bash
# Chạy ứng dụng
python build_main.py

# Test từng bước
# - Kiểm tra UI không bị crash
# - Verify translations
# - Check report output
```

### Test Cases
- [ ] All 16 steps work
- [ ] Vietnamese & English toggle
- [ ] Report exports (PDF/Excel/Text)
- [ ] Jump buttons (▲ ▼) hoạt động
- [ ] No crashes on Windows 10/11

---

## 📚 Resources

- **Main File:** `main_enhanced_auto.py` (6000+ lines)
- **Config:** `config.json` - Cấu hình
- **Assets:** `assets/` - Logo, icons, audio
- **Build:** `build_simple_fast.py` - Build script

---

## 🐛 Known Issues

Xem [GitHub Issues](../../issues) để danh sách đầy đủ

---

## ❓ Questions?

- Open an [Issue](../../issues)
- Check [Discussions](../../discussions)
- Email: [contact info]

---

## 📜 License

By contributing, you agree that your contributions will be licensed under MIT License.

---

**Happy Contributing! 🎉**
