import os
import pyautogui
import sys
import time
import win32gui
import win32con
import win32process
import win32api
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data import array as channels
from common.send_mail import send_email


# INSERT_YOUR_REWRITE_HERE
import sys
# Nhận 3 giá trị truyền từ app.py qua đối số dòng lệnh
if len(sys.argv) > 3:
    view_time = sys.argv[1]
    num_videos = sys.argv[2]
    vm_name = sys.argv[3]
    print(f"Đã nhận giá trị từ app.py: Thời lượng xem video (s): {view_time}, Số video xem: {num_videos}, Tên máy ảo: {vm_name}")
else:
    view_time = 5
    num_videos = 3
    vm_name = ""
    print("Không nhận đủ giá trị từ app.py (cần 3 giá trị: thời lượng xem video, số video xem, tên máy ảo)")

app_name = vm_name  # Tên ứng dụng bạn muốn tìm

# Hàm enum_windows_callback được sử dụng làm callback cho hàm win32gui.EnumWindows.
# Nó sẽ được gọi cho mỗi cửa sổ đang mở trên hệ thống.
# Tham số hwnd là handle của cửa sổ hiện tại, windows là danh sách để lưu các handle cửa sổ phù hợp.
# Nếu cửa sổ đang visible (hiển thị) và tiêu đề của nó chứa tên ứng dụng (app_name),
# thì handle của cửa sổ đó sẽ được thêm vào danh sách windows.
def enum_windows_callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if app_name.lower() in title.lower():
            windows.append(hwnd)

def get_bluestacks_window():
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def bring_window_to_front(hwnd):
    # Restore if minimized
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    # Bring to front
    win32gui.SetForegroundWindow(hwnd)
    # Force to top
    win32gui.BringWindowToTop(hwnd)

# Hàm get_window_rect nhận vào một handle cửa sổ (hwnd) và trả về vị trí (x, y) cùng với kích thước (width, height) của cửa sổ đó.
# Cụ thể, hàm sử dụng win32gui.GetWindowRect để lấy tọa độ góc trên bên trái (x, y) và góc dưới bên phải (x2, y2) của cửa sổ.
# Sau đó, tính toán chiều rộng (width = x2 - x) và chiều cao (height = y2 - y) dựa trên các tọa độ này.
# Kết quả trả về là bộ 4 giá trị: x, y, width, height.
def get_window_rect(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x, y, x2, y2 = rect
    width = x2 - x
    height = y2 - y
    return x, y, width, height

# Hàm start_bluestacks dùng để khởi động ứng dụng có tên được lưu trong biến app_name.
# Cụ thể, hàm này sử dụng subprocess.Popen để thực thi lệnh 'start' trên Windows nhằm mở ứng dụng.
# Nếu quá trình mở ứng dụng gặp lỗi (ví dụ như không tìm thấy ứng dụng), ngoại lệ sẽ được bắt và in ra thông báo lỗi.
# def start_bluestacks():
#     try:
#         subprocess.Popen(['start', '', app_name], shell=True)
#     except Exception as e:
#         print(f"Không thể mở {app_name}: {e}")

# Tìm cửa sổ BlueStacks
windows = get_bluestacks_window()

if not windows:
    print(f"Không tìm thấy ứng dụng {app_name} đang chạy.")
    # start_bluestacks()
    # time.sleep(5)
    # windows = get_bluestacks_window()
    exit()

if windows:
    hwnd = windows[0]
    win_title = win32gui.GetWindowText(hwnd)
    x, y, width, height = get_window_rect(hwnd)
    print(f"----------Tìm thấy cửa sổ: {win_title} tại vị trí: x={x}, y={y}. Kích thước hiện tại: width={width}, height={height}----------")


    # Thay đổi kích thước cửa sổ
    new_width = 427
    new_height = 735
    # Đặt lại vị trí cửa sổ về vị trí hiện tại (x, y) với kích thước mới
    print(f"Thay đổi kích thước và vị trí cửa sổ BlueStacks về width: {new_width}, height: {new_height}")
    # Lấy kích thước màn hình
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    # Tính toán vị trí để cửa sổ nằm ở giữa màn hình
    center_x = (screen_width - new_width) // 2
    center_y = (screen_height - new_height) // 2
    win32gui.MoveWindow(hwnd, center_x, center_y, new_width, new_height, True)
    # Cập nhật lại width, height để các thao tác click phía sau đúng vị trí
    width = new_width
    height = new_height
   

    # Đưa cửa sổ lên trên cùng
    bring_window_to_front(hwnd)
    time.sleep(1)  # Đợi ứng dụng khởi động lâu hơn

    # Click vào giữa cửa sổ để kích hoạt focus
    pyautogui.click(x + width // 2, y + height // 2)
    time.sleep(1)

    # click vào vị trí search
    time.sleep(1)
    print("Nhấn vào nút search")
    pyautogui.click(x + 370, y + 79)

    # Danh sách các kênh cần xem
    # Format channel URLs to usernames by removing the domain prefix
    channels = [channel.replace('https://www.tiktok.com/', '') for channel in channels]

    for idx, channel in enumerate(channels):
        if idx != 0:  # Nếu không phải channel đầu tiên
            time.sleep(1)
            print("Click vào icon search nhỏ")
            pyautogui.click(x + 68, y + 76)

        # Nhập text vào vùng input
        time.sleep(2)
        print(f"Nhập kênh tìm kiếm: {channel}")
        pyautogui.write(channel)

        # click vào vị trí đó search
        time.sleep(2)
        print("Thực hiện sự kiện search")
        pyautogui.click(x + 355, y + 76)

        # click vào vị trí user
        print("Nhấn vào người dùng")
        time.sleep(5)
        pyautogui.click(x + 36, y + 181)

        # click vào video
        time.sleep(5)
        print("Nhấn vào xem video")
        pyautogui.click(x + 61, y + 426)

        # Xem 3 video cho mỗi kênh
        for i in range(int(num_videos)):
            print(f"Xem video {i+1} trong vòng {view_time}s")
            time.sleep(int(view_time))

            if i < int(num_videos) - 1:  # Không cần chuyển video ở lần cuối
                print("Chuyển video mới")
                # click và giữ chuột tại vị trí A
                pyautogui.mouseDown(x + 184, y + 550)
                # kéo chuột đến vị trí B
                pyautogui.moveTo(x + 189, y + 147)
                # thả chuột
                pyautogui.mouseUp()

    # Send email notification when done (bỏ comment nếu muốn gửi mail)
    # print("Gửi email notification...")
    # send_email(
    #     subject="Auto Bot TikTok",
    #     body="Auto watch TikTok done",
    #     receiver_email="khoivinh282828@gmail.com"
    # )

    print("----------Kết thúc BOT AUTO WATCH----------")
else:
    print(f"Không tìm thấy ứng dụng {app_name} đang chạy.")
