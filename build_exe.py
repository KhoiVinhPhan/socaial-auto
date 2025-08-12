import os
import subprocess
import sys

def install_requirements():
    """Cài đặt các dependencies cần thiết"""
    print("Đang cài đặt dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Đã cài đặt dependencies thành công!")
    except subprocess.CalledProcessError:
        print("❌ Lỗi khi cài đặt dependencies")
        return False
    return True

def build_exe():
    """Build file .exe từ app.py"""
    print("Đang build file .exe...")
    try:
        # Sử dụng PyInstaller để tạo file .exe
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",  # Tạo 1 file .exe duy nhất
            "--windowed",  # Không hiển thị console window
            "--name=AutoBot",  # Tên file .exe
            "--icon=images/like.png",  # Icon cho file .exe (nếu có)
            "app1.py"
        ]
        
        subprocess.check_call(cmd)
        print("✅ Đã build file .exe thành công!")
        print("📁 File .exe được tạo trong thư mục: dist/AutoBot.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi build file .exe: {e}")
        return False
    except FileNotFoundError:
        print("❌ Không tìm thấy PyInstaller. Hãy cài đặt trước.")
        return False

def main():
    print("🚀 Bắt đầu quá trình tạo file .exe...")
    print("=" * 50)
    
    # Cài đặt dependencies
    if not install_requirements():
        return
    
    print("-" * 50)
    
    # Build file .exe
    if build_exe():
        print("-" * 50)
        print("🎉 Hoàn thành! Bạn có thể tìm file AutoBot.exe trong thư mục dist/")
        print("💡 Để chạy ứng dụng, chỉ cần double-click vào file AutoBot.exe")
    else:
        print("❌ Không thể tạo file .exe. Vui lòng kiểm tra lỗi và thử lại.")

if __name__ == "__main__":
    main() 