import sys
import subprocess
import atexit
import signal
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Auto bot by khoivinhphan"

# -----------------------------
# Process Management
# -----------------------------
running_processes = []

# Danh sách các button để disable/enable
action_buttons = []

def disable_all_buttons():
    """Disable tất cả các button khi có script đang chạy"""
    for btn in action_buttons:
        btn.configure(state="disabled")
        # Thêm tooltip để giải thích
        btn.configure(text=f"{btn.cget('text')} (Đang chạy...)")
    # Disable cả combobox
    view_time_combo.configure(state="disabled")
    num_videos_combo.configure(state="disabled")

def enable_all_buttons():
    """Enable tất cả các button khi không có script nào chạy"""
    for btn in action_buttons:
        btn.configure(state="normal")
        # Khôi phục text gốc
        original_texts = {
            "Auto Watch": "Auto Watch",
            "Auto Like": "Auto Like", 
            "Auto Comment": "Auto Comment",
            "Auto Follow": "Auto Follow",
            "For You": "For You"
        }
        btn.configure(text=original_texts.get(btn.cget('text').replace(" (Đang chạy...)", ""), btn.cget('text').replace(" (Đang chạy...)", "")))
    # Enable cả combobox
    view_time_combo.configure(state="readonly")
    num_videos_combo.configure(state="readonly")

def cleanup_processes():
    """Dừng tất cả process con đang chạy"""
    for process in running_processes:
        try:
            if process.poll() is None:  # Process vẫn đang chạy
                print(f"Đang dừng process {process.pid}...")
                process.terminate()  # Gửi SIGTERM
                try:
                    process.wait(timeout=5)  # Chờ tối đa 5 giây
                except subprocess.TimeoutExpired:
                    process.kill()  # Force kill nếu cần
                print(f"Đã dừng process {process.pid}")
        except Exception as e:
            print(f"Lỗi khi dừng process {process.pid}: {e}")
    
    # Enable lại tất cả button sau khi dừng
    enable_all_buttons()

def on_closing():
    """Handler khi tắt giao diện"""
    cleanup_processes()
    root.destroy()

# Đăng ký cleanup khi thoát
atexit.register(cleanup_processes)

# Xử lý signal để cleanup khi nhận signal thoát
if hasattr(signal, 'SIGINT'):
    signal.signal(signal.SIGINT, lambda sig, frame: cleanup_processes())
if hasattr(signal, 'SIGTERM'):
    signal.signal(signal.SIGTERM, lambda sig, frame: cleanup_processes())

# -----------------------------
# Helpers
# -----------------------------
def center_window(win, w=600, h=420):
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = (sw - w) // 2, (sh - h) // 3
    win.geometry(f"{w}x{h}+{x}+{y}")

def run_script(script_name: str, view_time: str, num_videos: str):
    """
    Chạy script con không chặn UI.
    Dùng python hiện tại (sys.executable) để đảm bảo đúng môi trường.
    """
    script_path = Path("window") / script_name
    if not script_path.exists():
        messagebox.showerror("Không tìm thấy file", f"Thiếu: {script_path}")
        return

    try:
        # Tùy chọn cờ tạo tiến trình (Windows: ẩn console)
        creationflags = 0
        if sys.platform == "win32":
            creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

        # Truyền tham số nếu script con cần
        p = subprocess.Popen(
            [sys.executable, str(script_path), view_time, num_videos],
            # creationflags=creationflags # ẩn console
        )
        
        # Thêm vào danh sách process đang chạy
        running_processes.append(p)
        
        # Disable tất cả button khi bắt đầu chạy script
        disable_all_buttons()

        status_var.set(f"Đang chạy {script_name} (PID {p.pid}) • thời lượng {view_time}s • {num_videos} video • Có {len(running_processes)} script đang chạy")

        # Theo dõi hoàn tất mà không chặn UI
        def _poll():
            if p.poll() is None:
                root.after(500, _poll)
            else:
                # Xóa process khỏi danh sách khi hoàn thành
                if p in running_processes:
                    running_processes.remove(p)
                status_var.set(f"{script_name} đã xong • exit={p.returncode} • Còn {len(running_processes)} script đang chạy")
                
                # Enable lại tất cả button nếu không còn script nào chạy
                if len(running_processes) == 0:
                    enable_all_buttons()
        root.after(500, _poll)

    except Exception as e:
        messagebox.showerror("Lỗi chạy script", str(e))

def on_action(action_key: str):
    view_time = view_time_var.get()
    num_videos = num_videos_var.get()

    mapping = {
        "watch": "adb_watch.py",
        "like": "adb_like.py",
        "comment": "adb_comment.py",
        "follow": "adb_follow.py",
        "foryou": "adb_foryou.py",
    }
    run_script(mapping[action_key], view_time, num_videos)

# -----------------------------
# UI
# -----------------------------
root = tk.Tk()
root.title(APP_TITLE)
root.minsize(600, 420)
root.resizable(False, False)

# Theme & Style (ttk)
style = ttk.Style()
# chọn theme "clam" cho ổn định màu và hover
try:
    style.theme_use("clam")
except tk.TclError:
    pass

base_font = ("Segoe UI", 11)  # thay đổi font nếu thích
style.configure(".", font=base_font)
style.configure("TLabel", padding=(0, 2))
style.configure("TButton", padding=(14, 8), relief="flat")
style.map("TButton",
          relief=[("pressed", "sunken")])

# màu nền chính
root.configure(bg="#f6f7fb")

# Khung tiêu đề
header = ttk.Frame(root, padding=(18, 16))
header.grid(row=0, column=0, sticky="ew")
header.columnconfigure(0, weight=1)
title_lbl = ttk.Label(header, text="Bảng điều khiển", font=("Segoe UI Semibold", 16))
title_lbl.grid(row=0, column=0, sticky="w")

# Card nhập cấu hình
card = ttk.Frame(root, padding=18, style="Card.TFrame")
card.grid(row=1, column=0, padx=16, pady=(6, 10), sticky="ew")
card.columnconfigure(1, weight=1)

# Tạo style card (viền nhẹ + nền trắng)
style.configure("Card.TFrame", background="#ffffff", borderwidth=1, relief="solid")
style.configure("Muted.TLabel", foreground="#667085")

# --- Hàng: Thời lượng xem (s)
view_time_var = tk.StringVar(value="5")
ttk.Label(card, text="Thời lượng xem (s)", style="Muted.TLabel").grid(row=0, column=0, sticky="w", pady=6)
view_time_combo = ttk.Combobox(
    card, textvariable=view_time_var, state="readonly",
    values=["5", "10", "15", "20", "25", "30"]
)
view_time_combo.grid(row=0, column=1, sticky="ew", pady=6)

# --- Hàng: Số video xem
num_videos_var = tk.StringVar(value="3")
ttk.Label(card, text="Số lượng video", style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=6)
num_videos_combo = ttk.Combobox(
    card, textvariable=num_videos_var, state="readonly",
    values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
)
num_videos_combo.grid(row=1, column=1, sticky="ew", pady=6)

# Card các nút hành động
actions = ttk.Frame(root, padding=18, style="Card.TFrame")
actions.grid(row=2, column=0, padx=16, pady=(0, 14), sticky="ew")
for i in range(4):
    actions.columnconfigure(i, weight=1)

btn_watch = ttk.Button(actions, text="Auto Watch", command=lambda: on_action("watch"))
btn_like = ttk.Button(actions, text="Auto Like", command=lambda: on_action("like"))
btn_comment = ttk.Button(actions, text="Auto Comment", command=lambda: on_action("comment"))
btn_follow = ttk.Button(actions, text="Auto Follow", command=lambda: on_action("follow"))
btn_foryou = ttk.Button(actions, text="For You", command=lambda: on_action("foryou"))

# Thêm các button vào danh sách để quản lý
action_buttons.extend([btn_watch, btn_like, btn_comment, btn_follow, btn_foryou])

btn_watch.grid(row=0, column=0, padx=6, pady=4, sticky="ew")
btn_like.grid(row=0, column=1, padx=6, pady=4, sticky="ew")
btn_comment.grid(row=0, column=2, padx=6, pady=4, sticky="ew")
btn_follow.grid(row=0, column=3, padx=6, pady=4, sticky="ew")
btn_foryou.grid(row=0, column=4, padx=6, pady=4, sticky="ew")

# Thêm nút Stop All
btn_stop = ttk.Button(actions, text="Stop script", command=cleanup_processes, style="Stop.TButton")
btn_stop.grid(row=1, column=0, columnspan=5, padx=6, pady=(8, 4), sticky="ew")

# Style cho nút Stop
style.configure("Stop.TButton", background="#dc3545", foreground="white")

# Thanh trạng thái
status_var = tk.StringVar(value="Sẵn sàng.")
status_bar = ttk.Label(root, textvariable=status_var, anchor="w", padding=(16, 10))
status_bar.grid(row=3, column=0, sticky="ew", padx=0)

# Cập nhật status bar để hiển thị số process đang chạy
def update_status():
    if running_processes:
        pids = [str(p.pid) for p in running_processes]
        status_var.set(f"Có {len(running_processes)} script đang chạy (PIDs: {', '.join(pids)})")
        # Đảm bảo button bị disable khi có script chạy
        if any(btn.cget("state") == "normal" for btn in action_buttons):
            disable_all_buttons()
    else:
        status_var.set("Sẵn sàng.")
        # Đảm bảo button được enable khi không có script nào chạy
        if any(btn.cget("state") == "disabled" for btn in action_buttons):
            enable_all_buttons()
    root.after(2000, update_status)  # Cập nhật mỗi 2 giây

# Bắt đầu cập nhật status
root.after(2000, update_status)

# Phím tắt tiện dụng
root.bind("<Return>", lambda e: on_action("watch"))  # Enter = Auto Watch

# Xử lý khi tắt giao diện
root.protocol("WM_DELETE_WINDOW", on_closing)

# center_window(root, 760, 420)
root.mainloop()
