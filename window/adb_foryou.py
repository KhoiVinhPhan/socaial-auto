import os
import subprocess
import time
import sys
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data_device import array as DEVICES


def screenshot(serial):
    out = subprocess.run(["adb", "-s", serial, "exec-out", "screencap", "-p"],
                         stdout=subprocess.PIPE).stdout
    img = cv2.imdecode(np.frombuffer(out, np.uint8), cv2.IMREAD_COLOR)
    return img

def find_icon(screen, template_path, threshold=0.85):
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        h, w = template.shape[:2]
        cx, cy = max_loc[0] + w//2, max_loc[1] + h//2
        return cx, cy, max_val
    return None

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
def job_for_device(serial, window_title=None, resolution=None, view_time=None, number_video=None):
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
       
        # Lướt {number_video} video
        for _ in range(number_video):
            time.sleep(view_time)
            #Click like
            screen = screenshot(serial)
            pos = find_icon(screen, "./images/like-3.png")
            print(pos)
            if pos:
                x_icon, y_icon, score = pos
                adb(serial, "shell", "input", "tap", str(x_icon), str(y_icon))
            time.sleep(2)

            # Chuyển video
            adb(serial, "shell", "input", "swipe", "339", "959", "363", "137", "500")

            
        return f"[{serial}] OK"
    except Exception as e:
        return f"[{serial}] Lỗi: {e}"

# ==== CHẠY SONG SONG NHIỀU THIẾT BỊ ====
def main():
    import sys

    # Nhận tham số từ dòng lệnh: view_time, number_video
    if len(sys.argv) < 3:
        print("Thiếu tham số: view_time và number_video")
        sys.exit(1)
    try:
        view_time = int(sys.argv[1])
        number_video = int(sys.argv[2])
    except Exception as e:
        print(f"Lỗi chuyển đổi tham số: {e}")
        sys.exit(1)

    futures = []
    with ThreadPoolExecutor(max_workers=len(DEVICES)) as ex:
        for d in DEVICES:
            futures.append(
                ex.submit(
                    job_for_device, 
                    d["serial"], 
                    d.get("window_title"), 
                    d.get("resolution"),
                    # Truyền thêm view_time và number_video nếu job_for_device cần
                    # Nếu chưa có, bạn cần sửa job_for_device nhận thêm 2 tham số này
                    view_time,
                    number_video
                )
            )
        for f in as_completed(futures):
            print(f.result())

if __name__ == "__main__":
    main()
