import tkinter as tk

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Device")

# Thiết lập màu nền xanh lá cây cho cửa sổ
root.configure(bg="green")

# Tạo label với text "text demo" và đặt ở giữa cửa sổ
label = tk.Label(root, text="Thay đổi kích thước của\nứng dụng bluestacks và\nđể ứng dụng vào trong\nvùng màu xanh lá", bg="green", fg="white", font=("Arial", 14))
label.place(relx=0.5, rely=0.5, anchor="center")

# Thiết lập kích thước cửa sổ
root.geometry("427x735")

# Chạy vòng lặp giao diện người dùng
root.mainloop()
