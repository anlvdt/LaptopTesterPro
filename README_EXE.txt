# LaptopTester - Portable EXE

## Cách tạo file .exe:

1. Chạy: make_exe.bat
2. Đợi quá trình build hoàn thành (2-5 phút)
3. File .exe sẽ được tạo trong thư mục dist/

## Cách chia sẻ:

- File EXE: dist/LaptopTester.exe (khoảng 50-100MB)
- Hoặc thư mục: LaptopTester_Portable/ (chứa EXE + hướng dẫn)

## Yêu cầu người dùng cuối:

- Windows 10/11
- Quyền Administrator (khuyến nghị)
- Không cần cài Python

## Lưu ý:

- Lần đầu chạy có thể chậm (10-30 giây)
- Antivirus có thể cảnh báo (false positive)
- File EXE tự chứa tất cả dependencies

## Troubleshooting:

- Nếu build lỗi: cài đặt lại Python và pip
- Nếu EXE không chạy: kiểm tra quyền Administrator
- Nếu thiếu tính năng: copy thêm thư mục assets/, bin/