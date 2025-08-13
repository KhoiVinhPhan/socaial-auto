import sys
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Auto bot by khoivinhphan"

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
        # Popen để không chặn UI, nếu bạn muốn đợi kết thúc: dùng subprocess.run(...)
        import os
        os.system(f"python window/{script_name}")

        status_var.set(f"Đã chạy {script_name} • thời lượng {view_time}s • {num_videos} video")
    except Exception as e:
        messagebox.showerror("Lỗi chạy script", str(e))

def on_action(action_key: str):
    view_time = view_time_var.get()
    num_videos = num_videos_var.get()

    mapping = {
        "watch": "adb_watch.py",
        "like": "adb_like.py",
        "comment": "wadb_comment.py",
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
    values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "20"]
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

btn_watch.grid(row=0, column=0, padx=6, pady=4, sticky="ew")
btn_like.grid(row=0, column=1, padx=6, pady=4, sticky="ew")
btn_comment.grid(row=0, column=2, padx=6, pady=4, sticky="ew")
btn_follow.grid(row=0, column=3, padx=6, pady=4, sticky="ew")
btn_foryou.grid(row=0, column=4, padx=6, pady=4, sticky="ew")

# Thanh trạng thái
status_var = tk.StringVar(value="Sẵn sàng.")
status_bar = ttk.Label(root, textvariable=status_var, anchor="w", padding=(16, 10))
status_bar.grid(row=3, column=0, sticky="ew", padx=0)

# Phím tắt tiện dụng
root.bind("<Return>", lambda e: on_action("watch"))  # Enter = Auto Watch

center_window(root, 760, 420)
root.mainloop()
