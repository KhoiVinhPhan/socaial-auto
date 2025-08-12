# Hướng Dẫn Tạo File .EXE từ app.py

## Cách 1: Sử dụng file batch (Đơn giản nhất)

1. **Double-click vào file `build_exe.bat`**
2. Script sẽ tự động:
   - Cài đặt dependencies cần thiết
   - Build file .exe
   - Thông báo kết quả

## Cách 2: Chạy trực tiếp Python script

1. **Mở Command Prompt hoặc PowerShell**
2. **Di chuyển đến thư mục dự án:**
   ```cmd
   cd /d "D:\project\socaial-auto"
   ```
3. **Chạy script build:**
   ```cmd
   python build_exe.py
   ```

## Cách 3: Build thủ công

1. **Cài đặt PyInstaller:**
   ```cmd
   pip install pyinstaller
   ```

2. **Build file .exe:**
   ```cmd
   pyinstaller --onefile --windowed --name=AutoBot app.py
   ```

## Kết quả

- File .exe sẽ được tạo trong thư mục `dist/`
- Tên file: `AutoBot.exe`
- Kích thước: Khoảng 10-20 MB
- Có thể chạy trên máy Windows khác mà không cần cài Python

## Lưu ý

- Đảm bảo Python đã được cài đặt trên máy
- Nếu gặp lỗi, hãy kiểm tra:
  - Python version (khuyến nghị Python 3.7+)
  - Quyền truy cập thư mục
  - Antivirus có thể chặn quá trình build

## Sử dụng

Sau khi có file .exe:
1. Copy file `AutoBot.exe` đến máy khác
2. Double-click để chạy
3. Giao diện sẽ hiện ra giống như khi chạy `app.py`

## Troubleshooting

### Lỗi "python not found"
- Cài đặt Python và thêm vào PATH
- Hoặc sử dụng đường dẫn đầy đủ: `C:\Python39\python.exe build_exe.py`

### Lỗi "pyinstaller not found"
- Chạy: `pip install pyinstaller`
- Hoặc sử dụng script `build_exe.py` để tự động cài đặt

### File .exe không chạy
- Kiểm tra Windows Defender/Antivirus
- Chạy với quyền Administrator
- Kiểm tra Windows version compatibility 