import tkinter as tk

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Auto bot by khoivinhphan")

# Thiết lập màu nền xanh lá cây cho cửa sổ
root.configure(bg="green")

# Tạo label với text "text demo" và đặt ở giữa cửa sổ
label = tk.Label(root, text="Thay đổi kích thước của\nứng dụng bluestacks và\nđể ứng dụng vào trong\nvùng màu xanh lá\ntrước khi chạy bot", bg="green", fg="white", font=("Arial", 14))
label.place(relx=0.5, rely=0.5, anchor="center")

# Tạo button "Auto watch"
def run_auto_watch():
    import os
    os.system("python auto/auto_watch.py")

watch_button = tk.Button(root, text="Auto watch", command=run_auto_watch, font=("Arial", 12))
watch_button.place(relx=0.2, rely=0.7, anchor="center")

# Tạo button "Auto like"
def run_auto_like():
    import os
    os.system("python auto/auto_like.py")

like_button = tk.Button(root, text="Auto like", command=run_auto_like, font=("Arial", 12))
like_button.place(relx=0.7, rely=0.7, anchor="center")

# Tạo button "Auto comment"
def run_auto_comment():
    import os
    os.system("python auto/auto_comment.py")

comment_button = tk.Button(root, text="Auto comment", command=run_auto_comment, font=("Arial", 12))
comment_button.place(relx=0.2, rely=0.85, anchor="center")

# Tạo button "Auto follow" 
def run_auto_follow():
    import os
    os.system("python auto/auto_follow.py")

follow_button = tk.Button(root, text="Auto follow", command=run_auto_follow, font=("Arial", 12))
follow_button.place(relx=0.7, rely=0.85, anchor="center")




# Thiết lập kích thước cửa sổ
root.geometry("427x735")
# Không cho phép thay đổi kích thước cửa sổ
root.resizable(False, False)

# Chạy vòng lặp giao diện người dùng
root.mainloop()
