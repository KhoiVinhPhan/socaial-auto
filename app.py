import tkinter as tk

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Auto bot by khoivinhphan")

# Thiết lập màu nền xanh lá cây cho cửa sổ
root.configure(bg="white")

# Thêm select option (OptionMenu) để chọn giá trị gửi qua auto_watch.py
# Label và OptionMenu cùng 1 hàng (ngang)

# Hàng nhập text: Label và Entry (ô nhập text), nằm trên option_label_view_time
label_vm_name = tk.Label(root, text="Nhập tên máy ảo:", font=("Arial", 12), bg="white")
entry_vm_name = tk.Entry(root, font=("Arial", 12), width=30)
# Đặt label và entry cùng 1 hàng, label bên trái, entry bên phải, ở hàng trên option_label_view_time
label_vm_name.place(relx=0.16, rely=0.07, anchor="center")
entry_vm_name.place(relx=0.62, rely=0.07, anchor="center")


# Hàng 1: Thời lượng xem video (s)
option_label_view_time = tk.Label(root, text="Thời lượng xem video (s):", font=("Arial", 12), bg="white")
selected_option_view_time = tk.StringVar(root)
selected_option_view_time.set("5")  # Giá trị mặc định
options_view_time = ["5", "10", "15", "20", "25", "30"]
option_menu_view_time = tk.OptionMenu(root, selected_option_view_time, *options_view_time)
option_menu_view_time.config(font=("Arial", 12))
# Đặt label và option menu cùng 1 hàng, label bên trái, option menu bên phải
option_label_view_time.place(relx=0.18, rely=0.15, anchor="center")
option_menu_view_time.place(relx=0.43, rely=0.15, anchor="center")

# Hàng 2: Số video xem
option_label_num_videos = tk.Label(root, text="Số video xem:", font=("Arial", 12), bg="white")
selected_option_num_videos = tk.StringVar(root)
selected_option_num_videos.set("3")  # Giá trị mặc định
options_num_videos = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "20"]
option_menu_num_videos = tk.OptionMenu(root, selected_option_num_videos, *options_num_videos)
option_menu_num_videos.config(font=("Arial", 12))
# Đặt label và option menu cùng 1 hàng, label bên trái, option menu bên phải, ở hàng dưới
option_label_num_videos.place(relx=0.12, rely=0.25, anchor="center")
option_menu_num_videos.place(relx=0.43, rely=0.25, anchor="center")

# Tạo button "Auto watch"
def run_auto_watch():
    import os
    # Lấy giá trị đã chọn từ OptionMenu
    value_view_time = selected_option_view_time.get()
    value_number_video = selected_option_num_videos.get()
    value_vm_name = entry_vm_name.get()
    # Truyền cả ba giá trị này qua đối số dòng lệnh
    os.system(f"python window/auto_watch.py \"{value_view_time}\" \"{value_number_video}\" \"{value_vm_name}\"")

watch_button = tk.Button(root, text="Auto watch", command=run_auto_watch, font=("Arial", 12))
watch_button.place(relx=0.2, rely=0.7, anchor="center")

# Tạo button "Auto like"
def run_auto_like():
    import os
    value_view_time = selected_option_view_time.get()
    value_number_video = selected_option_num_videos.get()
    value_vm_name = entry_vm_name.get()
    os.system(f"python window/auto_like.py \"{value_view_time}\" \"{value_number_video}\" \"{value_vm_name}\"")

like_button = tk.Button(root, text="Auto like", command=run_auto_like, font=("Arial", 12))
like_button.place(relx=0.7, rely=0.7, anchor="center")

# Tạo button "Auto comment"
def run_auto_comment():
    import os
    value_view_time = selected_option_view_time.get()
    value_number_video = selected_option_num_videos.get()
    value_vm_name = entry_vm_name.get()
    os.system(f"python window/auto_comment.py \"{value_view_time}\" \"{value_number_video}\" \"{value_vm_name}\"")

comment_button = tk.Button(root, text="Auto comment", command=run_auto_comment, font=("Arial", 12))
comment_button.place(relx=0.2, rely=0.85, anchor="center")

# Tạo button "Auto follow" 
def run_auto_follow():
    import os
    value_view_time = selected_option_view_time.get()
    value_number_video = selected_option_num_videos.get()
    value_vm_name = entry_vm_name.get()
    os.system(f"python window/auto_follow.py \"{value_view_time}\" \"{value_number_video}\" \"{value_vm_name}\"")

follow_button = tk.Button(root, text="Auto follow", command=run_auto_follow, font=("Arial", 12))
follow_button.place(relx=0.7, rely=0.85, anchor="center")




# Thiết lập kích thước cửa sổ
root.geometry("600x500")
# Không cho phép thay đổi kích thước cửa sổ
root.resizable(False, False)

# Chạy vòng lặp giao diện người dùng
root.mainloop()
