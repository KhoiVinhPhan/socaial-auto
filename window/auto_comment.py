import os
import pyautogui
import sys
import time
import win32gui
import win32con
import win32process
import win32api
import subprocess
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data import array as channels
from common.send_mail import send_email

# Nhận 3 giá trị truyền từ app.py qua đối số dòng lệnh
if len(sys.argv) > 3:
    view_time = int(sys.argv[1])
    num_videos = int(sys.argv[2])
    vm_name = sys.argv[3]
    print(f"Đã nhận giá trị từ app.py: Thời lượng xem video (s): {view_time}, Số video xem: {num_videos}, Tên máy ảo: {vm_name}")
else:
    view_time = 5
    num_videos = 3
    vm_name = ""
    print("Không nhận đủ giá trị từ app.py (cần 3 giá trị: thời lượng xem video, số video xem, tên máy ảo)")
    exit()

app_name = vm_name  # Tên ứng dụng bạn muốn tìm

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
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    win32gui.BringWindowToTop(hwnd)

def get_window_rect(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x, y, x2, y2 = rect
    width = x2 - x
    height = y2 - y
    return x, y, width, height

# Tìm cửa sổ BlueStacks
windows = get_bluestacks_window()

if not windows:
    print(f"Không tìm thấy cửa sổ ứng dụng '{app_name}'. Hãy chắc chắn rằng BlueStacks đang chạy với tên máy ảo đúng.")
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


    # # lấy vị trị tương đối của chuột trong app
    # # Đợi 5 giây
    # pyautogui.sleep(5)
    # # Lấy vị trí hiện tại của chuột
    # current_x, current_y = pyautogui.position()
    # # Tính toán vị trí tương đối so với cửa sổ
    # relative_x = current_x - x
    # relative_y = current_y - y
    # print(f"Vị trí tương đối: x={relative_x}, y={relative_y}")
    # exit()

    # Đưa cửa sổ lên trên cùng
    bring_window_to_front(hwnd)
    time.sleep(1)  # Đợi ứng dụng khởi động lâu hơn

    # Click vào giữa cửa sổ để kích hoạt focus
    pyautogui.click(x + width // 2, y + height // 2)
    time.sleep(1)

    # Click vào ô search
    time.sleep(1)
    print("Nhấn vào nút search")
    pyautogui.click(x + 370, y + 79)

    # Danh sách các kênh cần xem
    channels = [channel.replace('https://www.tiktok.com/', '') for channel in channels]

    for channel_idx, channel in enumerate(channels):
        if channel_idx != 0:
            time.sleep(1)
            print("Click vào icon search nhỏ")
            pyautogui.click(x + 68, y + 76)

        # Nhập text vào vùng input
        time.sleep(2)
        print(f"Nhập kênh tìm kiếm: {channel}")
        pyautogui.typewrite(channel)

        # click vào vị trí đó search
        time.sleep(2)
        print("Thực hiện search")
        pyautogui.click(x + 355, y + 76)

        # click vào vị trí user
        time.sleep(5)
        print("Nhấn vào người dùng")
        pyautogui.click(x + 36, y + 181)

        # click vào video
        time.sleep(5)
        print("Nhấn vào xem video")
        pyautogui.click(x + 61, y + 426)

        # Xem num_videos video cho mỗi kênh
        for i in range(num_videos):
            print(f"Xem video {i+1} trong vòng {view_time}s")
            time.sleep(view_time)

            # click vào vị trí comment
            print("Nhấn vào vị trí comment")
            pyautogui.click(x + 79, y + 714)

            # Nhập text comment
            print("Nhập text comment")
            time.sleep(1)
            from data.data_comment import array as comments
            pyautogui.typewrite(random.choice(comments))

            # click vào vị trí send
            print("Nhấn vào vị trí send")
            time.sleep(2)
            pyautogui.click(x + 364, y + 496)
            time.sleep(1)

            if i < num_videos - 1:
                print("Chuyển video mới")
                pyautogui.mouseDown(x + 184, y + 550)
                pyautogui.moveTo(x + 189, y + 147)
                pyautogui.mouseUp()

# Gửi email khi hoàn thành (nếu muốn)
# send_email(
#     subject="Auto Bot TikTok",
#     body="Auto comment TikTok done",
#     receiver_email="khoivinh282828@gmail.com"
# )

print("----------Kết thúc BOT AUTO COMMENT----------")
