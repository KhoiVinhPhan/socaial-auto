import os
import subprocess
import time
import sys
import cv2
import numpy as np
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data_device import array as DEVICES
from data.data_comment import array as comments
from common.send_mail import send_email

# === Lưu ý về vấn đề khi chạy nhiều máy ảo song song ===
# 1. ADB không thread-safe: Khi nhiều thread/process cùng gửi lệnh adb, có thể bị nghẽn hoặc conflict, nhất là khi nhiều thiết bị cùng port 127.0.0.1:<port>.
# 2. subprocess.run (dùng cho adb) là blocking, nhưng không đồng bộ hóa truy cập adb, có thể gây lỗi khi nhiều thread cùng lúc.
# 3. Nếu máy yếu, CPU/RAM không đủ, thao tác nhận diện ảnh (cv2) và adb sẽ bị chậm, gây timeout hoặc thao tác không đúng.
# 4. Việc random.choice([True, False]) cho like/comment/save có thể khiến hành vi không đồng nhất, dễ gây hiểu nhầm là "không thực hiện đúng sự kiện".
# 5. Không kiểm tra kết quả trả về của adb (chỉ in ra), nếu adb bị treo hoặc disconnect, thao tác tiếp theo vẫn chạy tiếp.
# 6. Không có lock khi thao tác adb, có thể gây race condition nếu adb server bị nghẽn.

# === Giải pháp: Thêm lock cho adb, kiểm tra kết quả trả về, tăng timeout, log kỹ hơn ===

adb_lock = Lock()

# ==== HÀM KIỂM TRA TRẠNG THÁI BLUESTACKS ====
def check_bluestacks_status(port):
    """Kiểm tra xem BlueStacks có đang chạy trên port này không"""
    try:
        # Kiểm tra kết nối TCP đến port
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout 1 giây
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            # Port đang mở, kiểm tra thêm bằng adb devices
            with adb_lock:
                out, err, rc = run(["adb", "devices"], timeout=3)
            if f"127.0.0.1:{port}" in out and "device" in out:
                return True, "Đang chạy và có thể kết nối ADB"
            elif f"127.0.0.1:{port}" in out:
                return True, "Đang chạy nhưng chưa kết nối ADB"
            else:
                return True, "Đang chạy nhưng không phản hồi ADB"
        else:
            return False, "Port không mở"
    except Exception as e:
        return False, f"Lỗi kiểm tra: {e}"

def get_active_bluestacks():
    """Lấy danh sách BlueStacks đang hoạt động"""
    active_instances = []
    
    print("=== KIỂM TRA TRẠNG THÁI BLUESTACKS ===")
    for device in DEVICES:
        serial = device["serial"]
        if ":" in serial:
            port = int(serial.split(":")[1])
            is_active, status = check_bluestacks_status(port)
            
            if is_active:
                device_copy = device.copy()
                device_copy["status"] = status
                active_instances.append(device_copy)
                print(f"[{serial}] {status}")
            else:
                print(f"[{serial}] {status} - Bỏ qua")
    
    return active_instances

def screenshot(serial):
    # Thêm timeout và kiểm tra lỗi
    try:
        with adb_lock:
            out = subprocess.run(["adb", "-s", serial, "exec-out", "screencap", "-p"],
                                 stdout=subprocess.PIPE, timeout=10).stdout
        img = cv2.imdecode(np.frombuffer(out, np.uint8), cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"[{serial}] Lỗi screenshot: {e}")
        return None

def find_icon(screen, template_path, threshold=0.85):
    if screen is None:
        return None
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"[IMG] Không tìm thấy template: {template_path}")
        return None
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
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.stdout.strip(), p.stderr.strip(), p.returncode
    except Exception as e:
        return "", str(e), -1

def adb_connect(serial, retry=3, delay=2):
    for i in range(retry):
        with adb_lock:
            out, err, rc = run(["adb", "connect", serial], timeout=10)
        if "connected" in out or "already connected" in out:
            print(f"[{serial}] Đã kết nối ADB")
            return True
        print(f"[{serial}] Kết nối thất bại, thử lại ({i+1}/{retry}) -> {out or err}")
        time.sleep(delay)
    return False

def adb(serial, *args, timeout=None):
    """Gửi lệnh adb -s <serial> ..."""
    full = ["adb", "-s", serial, *args]
    with adb_lock:
        out, err, rc = run(full, timeout=timeout or 10)
    if err:
        print(f"[{serial}] ERR: {err}")
    if out:
        print(f"[{serial}] {out}")
    return rc == 0, out

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
        for idx in range(number_video):
            print(f"[{serial}] --- Video {idx+1}/{number_video} ---")
            time.sleep(view_time)
            screen = screenshot(serial)
            if screen is None:
                print(f"[{serial}] Không lấy được screenshot, bỏ qua video này.")
                continue

            choice_like = random.choice([True, False])
            print(f"[{serial}] choice_like: {choice_like}")
            if choice_like:
                pos_like = find_icon(screen, "./images/like-3.png")
                print(f"[{serial}] pos_like: {pos_like}")
                if pos_like:
                    x_icon, y_icon, score = pos_like
                    ok, _ = adb(serial, "shell", "input", "tap", str(x_icon), str(y_icon))
                    if not ok:
                        print(f"[{serial}] Lỗi tap like")
                time.sleep(2)

                pos_save = find_icon(screen, "./images/save.png")
                print(f"[{serial}] pos_save: {pos_save}")
                if pos_save:
                    x_icon, y_icon, score = pos_save
                    ok, _ = adb(serial, "shell", "input", "tap", str(x_icon), str(y_icon))
                    if not ok:
                        print(f"[{serial}] Lỗi tap save")
                time.sleep(2)

            choice_comment = random.choice([True, False])
            print(f"[{serial}] choice_comment: {choice_comment}")
            if choice_comment:
                pos_comment = find_icon(screen, "./images/comment-2.png")
                print(f"[{serial}] pos_comment: {pos_comment}")
                if pos_comment:
                    x_icon, y_icon, score = pos_comment
                    ok, _ = adb(serial, "shell", "input", "tap", str(x_icon), str(y_icon))
                    if not ok:
                        print(f"[{serial}] Lỗi tap comment icon")
                    time.sleep(2)
                    ok, _ = adb(serial, "shell", "input", "tap", "151", "1233")
                    if not ok:
                        print(f"[{serial}] Lỗi tap vào ô nhập comment")
                    time.sleep(2)
                    comment_text = random.choice(comments)
                    ok, _ = adb(serial, "shell", "input", "text", comment_text)
                    if not ok:
                        print(f"[{serial}] Lỗi nhập comment")
                    time.sleep(2)
                    ok, _ = adb(serial, "shell", "input", "tap", "666", "852")
                    if not ok:
                        print(f"[{serial}] Lỗi tap gửi comment")
                    time.sleep(2)
                    ok, _ = adb(serial, "shell", "input", "tap", "335", "271")
                    if not ok:
                        print(f"[{serial}] Lỗi tap đóng comment")

                    # Click lan 2
                    time.sleep(1)
                    adb(serial, "shell", "input", "tap", "335", "271")
                time.sleep(2)

            ok, _ = adb(serial, "shell", "input", "swipe", "339", "959", "363", "137", "500")
            if not ok:
                print(f"[{serial}] Lỗi swipe sang video tiếp theo")

        return f"[{serial}] OK"
    except Exception as e:
        return f"[{serial}] Lỗi: {e}"

# ==== CHẠY SONG SONG NHIỀU THIẾT BỊ ====
def main():
    import sys

    # Nhận tham số từ dòng lệnh: view_time, number_video
    if len(sys.argv) < 3:
        print("Thiếu tham số: view_time và number_video")
        print("Sử dụng: python adb_foryou_all.py <view_time> <number_video>")
        print("Ví dụ: python adb_foryou_all.py 10 5")
        sys.exit(1)
    try:
        view_time = int(sys.argv[1])
        number_video = int(sys.argv[2])
    except Exception as e:
        print(f"Lỗi chuyển đổi tham số: {e}")
        sys.exit(1)

    # Kiểm tra trạng thái BlueStacks trước khi chạy
    active_devices = get_active_bluestacks()
    
    if not active_devices:
        print("❌ Không có BlueStacks nào đang chạy!")
        print("💡 Hãy khởi động BlueStacks trước khi chạy script")
        return
    
    print(f"\n✅ Tìm thấy {len(active_devices)} BlueStacks đang hoạt động")
    print(f"📊 TỔNG KẾT:")
    print(f"   - Tổng cấu hình: {len(DEVICES)}")
    print(f"   - Đang hoạt động: {len(active_devices)}")
    print(f"   - Không hoạt động: {len(DEVICES) - len(active_devices)}")
    
    print(f"\n🎯 BẮT ĐẦU XỬ LÝ:")
    print(f"   - Thời gian xem mỗi video: {view_time} giây")
    print(f"   - Số video sẽ xem: {number_video}")
    print("=" * 50)

    futures = []

    with ThreadPoolExecutor(max_workers=len(active_devices)) as ex:
        try:
            for d in active_devices:
                futures.append(
                    ex.submit(
                        job_for_device, 
                        d["serial"], 
                        d.get("window_title"), 
                        d.get("resolution"),
                        view_time,
                        number_video
                    )
                )
            for f in as_completed(futures):
                print(f.result())
            
            print("\n🎉 HOÀN THÀNH TẤT CẢ THIẾT BỊ!")
            print("Gửi email notification...")
            send_email(
                subject="[Auto Bot] TikTok",
                body="Auto watch TikTok done",
                receiver_email=["khoivinhphan@gmail.com", "khoivinh282828@gmail.com"]
            )    
        except Exception as e:
            print(f"Lỗi khi submit job cho thiết bị: {e}")

def quick_status_check():
    """Kiểm tra nhanh trạng thái tất cả BlueStacks"""
    print("=== KIỂM TRA NHANH TRẠNG THÁI BLUESTACKS ===")
    active_devices = get_active_bluestacks()
    
    if not active_devices:
        print("❌ Không có BlueStacks nào đang chạy!")
        return
    
    print(f"\n📊 TỔNG KẾT:")
    print(f"   - Tổng cấu hình: {len(DEVICES)}")
    print(f"   - Đang hoạt động: {len(active_devices)}")
    print(f"   - Không hoạt động: {len(DEVICES) - len(active_devices)}")
    
    return active_devices

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        quick_status_check()
    else:
        main()
