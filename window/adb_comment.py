import os
import subprocess
import time
import sys
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data_comment import array as comments
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data_device import array as DEVICES


# ==== HÀM TIỆN ÍCH ====
def run(cmd, timeout=None):
    """Chạy lệnh và trả về (stdout, stderr, returncode)"""
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.stdout.strip(), p.stderr.strip(), p.returncode

def adb_connect(serial, retry=3, delay=2):
    for i in range(retry):
        out, err, rc = run(["adb", "connect", serial])
        if "connected" in out or "already connected" in out:
            print(f"[{serial}] Đã kết nối ADB")
            return True
        print(f"[{serial}] Kết nối thất bại, thử lại ({i+1}/{retry}) -> {out or err}")
        time.sleep(delay)
    return False

def adb(serial, *args, timeout=None):
    """Gửi lệnh adb -s <serial> ..."""
    full = ["adb", "-s", serial, *args]
    out, err, rc = run(full, timeout=timeout)
    if err:
        print(f"[{serial}] ERR: {err}")
    if out:
        print(f"[{serial}] {out}")
    return rc == 0, out

# (TÙY CHỌN) Nếu bạn muốn chỉnh vị trí/kích thước cửa sổ BlueStacks theo từng máy:
def move_window_if_needed(window_title, width, height):
    try:
        import win32gui, win32api
        hwnds = []
        def enum_cb(hwnd, acc):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if window_title.lower() in title.lower():
                    acc.append(hwnd)
        win32gui.EnumWindows(enum_cb, hwnds)
        if not hwnds:
            print(f"[UI] Không tìm thấy cửa sổ: {window_title}")
            return
        hwnd = hwnds[0]
        screen_w = win32api.GetSystemMetrics(0)
        screen_h = win32api.GetSystemMetrics(1)
        x = (screen_w - width)//2
        y = (screen_h - height)//2
        win32gui.MoveWindow(hwnd, x, y, width, height, True)
        print(f"[UI] Đã move/resize cửa sổ '{window_title}' -> {width}x{height}")
        time.sleep(1)
    except Exception as e:
        print(f"[UI] Lỗi chỉnh cửa sổ '{window_title}': {e}")

# ==== LOGIC TÁC VỤ CHO MỘT THIẾT BỊ ====
def job_for_device(serial, window_title=None, resolution=None):
    try:
        # 1) Kết nối ADB
        if not adb_connect(serial):
            return f"[{serial}] KO: không kết nối được ADB"

        # 2) (Tùy chọn) căn cửa sổ BlueStacks cho thiết bị này
        if window_title and resolution:
            w, h = resolution
            move_window_if_needed(window_title, w, h)
        

        # 3) Thực thi chuỗi thao tác TikTok
        # Click ô search home
        adb(serial, "shell", "input", "tap", "675", "77")


        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from data.data import array as channels
        channels = [channel.replace('https://www.tiktok.com/', '') for channel in channels]

        for idx, channel in enumerate(channels):
            if idx != 0:  # Nếu không phải channel đầu tiên
                time.sleep(2)
                adb(serial, "shell", "input", "tap", "115", "73")

            # Nhập text (khi có ký tự đặc biệt, đôi khi cần escape; có thể thử 'input text \"\\@ngheunek\"')
            adb(serial, "shell", "input", "text", channel)

            # Click ô search trong trang tìm kiếm
            adb(serial, "shell", "input", "tap", "659", "75")

            # Click vào tab user
            time.sleep(4)
            adb(serial, "shell", "input", "tap", "141", "141")

            # Chờ và chọn user đầu tiên
            time.sleep(5)
            adb(serial, "shell", "input", "tap", "68", "242")

            # Chờ và mở video đầu tiên
            time.sleep(5)
            adb(serial, "shell", "input", "tap", "111", "665")

            # Lướt 3 video
            for _ in range(2):
                time.sleep(5)

                # Nhập comment
                adb(serial, "shell", "input", "tap", "79", "1243")
                adb(serial, "shell", "input", "text", random.choice(comments))
                adb(serial, "shell", "input", "tap", "669", "853")
                time.sleep(2)
                
                # Lướt video
                adb(serial, "shell", "input", "swipe", "339", "959", "363", "137", "500")

        return f"[{serial}] OK"
    except Exception as e:
        return f"[{serial}] Lỗi: {e}"

# ==== CHẠY SONG SONG NHIỀU THIẾT BỊ ====
def main():
    futures = []
    with ThreadPoolExecutor(max_workers=len(DEVICES)) as ex:
        for d in DEVICES:
            futures.append(
                ex.submit(job_for_device, d["serial"], d.get("window_title"), d.get("resolution"))
            )
        for f in as_completed(futures):
            print(f.result())

if __name__ == "__main__":
    main()
