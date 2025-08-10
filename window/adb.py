import subprocess
import time
import win32gui
import win32con
import win32api
import time

# Địa chỉ ADB của máy ảo BlueStacks
adb_address = "127.0.0.1:5615"

def start_bluestacks():
    """
    Hàm này sẽ mở BlueStacks nếu chưa chạy.
    Thông thường BlueStacks sẽ tự động mở khi bạn thao tác, 
    nhưng nếu cần bạn có thể mở bằng subprocess với đường dẫn tới BlueStacks.exe.
    """
    # Đường dẫn tới file thực thi BlueStacks, thay đổi nếu cài đặt ở vị trí khác
    bluestacks_path = r"C:\Program Files\BlueStacks_nxt\HD-Player.exe"
    try:
        subprocess.Popen([bluestacks_path])
        print("Đang mở BlueStacks...")
        time.sleep(10)  # Đợi BlueStacks khởi động
    except Exception as e:
        print(f"Lỗi khi mở BlueStacks: {e}")

def connect_adb(adb_addr):
    """
    Kết nối tới máy ảo BlueStacks qua ADB.
    """
    try:
        result = subprocess.run(["adb", "connect", adb_addr], capture_output=True, text=True)
        print(result.stdout)
        if "connected" in result.stdout or "already connected" in result.stdout:
            print(f"Đã kết nối tới {adb_addr} qua ADB.")
            return True
        else:
            print(f"Không thể kết nối tới {adb_addr}.")
            return False
    except Exception as e:
        print(f"Lỗi khi kết nối ADB: {e}")
        return False

def send_adb_command(adb_addr, command):
    """
    Gửi lệnh ADB tới máy ảo.
    """
    full_cmd = ["adb", "-s", adb_addr] + command
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        print(f"Lệnh: {' '.join(full_cmd)}")
        print("Kết quả:", result.stdout)
        if result.stderr:
            print("Lỗi:", result.stderr)
    except Exception as e:
        print(f"Lỗi khi gửi lệnh ADB: {e}")

if __name__ == "__main__":
    # Bước 1: (Tùy chọn) Mở BlueStacks nếu chưa chạy
    # start_bluestacks()

    # Bước 2: Kết nối tới máy ảo qua ADB
    if connect_adb(adb_address):
        app_name = '@rynsey_asmr_ UK#24'  # Hoặc tên cửa sổ chính xác của bạn

        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if app_name.lower() in title.lower():
                    windows.append(hwnd)

        def get_bluestacks_window():
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            return windows

        # Tìm cửa sổ BlueStacks
        windows = get_bluestacks_window()
        if windows:
            hwnd = windows[0]
            # Đặt kích thước cửa sổ
            new_width = 427
            new_height = 735
            # Lấy kích thước màn hình để căn giữa (tùy chọn)
            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)
            center_x = (screen_width - new_width) // 2
            center_y = (screen_height - new_height) // 2
            win32gui.MoveWindow(hwnd, center_x, center_y, new_width, new_height, True)
            print("Đã thay đổi kích thước cửa sổ BlueStacks.")
            time.sleep(1)
        else:
            print("Không tìm thấy cửa sổ BlueStacks để thay đổi kích thước.")
            exit()
       
        
        # Click vào ô search của trang home tiktok
        send_adb_command(adb_address, ["shell", "input", "tap", str(675), str(77)])

        # Nhập text "@ngheunek" vào ô search bằng ADB
        send_adb_command(adb_address, ["shell", "input", "text", "@ngheunek"])

        # Click vào ô search trong trang tìm kiếm
        send_adb_command(adb_address, ["shell", "input", "tap", str(659), str(75)])
       
        # Click vào người tìm kiếm đầu tiên
        time.sleep(5)  # chờ 5s để load trang
        send_adb_command(adb_address, ["shell", "input", "tap", str(66), str(281)])

        # Click vào video đầu tiên của người tìm kiếm
        time.sleep(5)  # chờ 5s để load trang
        send_adb_command(adb_address, ["shell", "input", "tap", str(111), str(665)])

        # Lướt video tiếp theo
        for _ in range(3):
            time.sleep(5)  # xem video trong 5s
            send_adb_command(adb_address, [
                "shell", "input", "swipe",
                str(339), str(959), str(363), str(137), str(500)
            ])


            
