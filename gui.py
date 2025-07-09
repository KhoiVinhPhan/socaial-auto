import tkinter as tk
import pyautogui

import subprocess

# Hàm thực hiện chạy file auto.py
# Cập nhật hàm run_auto để hiển thị log
def run_auto():
    # Xóa log cũ
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "Bắt đầu chạy chương trình...\n")
    
    # Chạy file auto.py và capture output
    process = subprocess.Popen(['python', 'auto.py'], 
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True)
    
    # Đọc và hiển thị output
    def read_output():
        # Đọc output từ process
        if process.poll() is None:  # Nếu process vẫn đang chạy
            # Đọc output có sẵn mà không block
            output = process.stdout.readline()
            if output:
                log_text.insert(tk.END, output)
                log_text.see(tk.END)  # Tự động cuộn xuống
            
            # Lập lịch kiểm tra tiếp sau 100ms
            root.after(100, read_output)
        else:
            # Process đã kết thúc
            # Đọc output còn lại
            remaining_output = process.stdout.read()
            if remaining_output:
                log_text.insert(tk.END, remaining_output)
                log_text.see(tk.END)
            log_text.insert(tk.END, "\nChương trình đã hoàn thành!")

    # Bắt đầu đọc output
    read_output()


# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("TikTok Auto Watch")

# Thiết lập kích thước cửa sổ
root.geometry("500x500")

# Nút bấm thực hiện chạy auto.py
button_watch = tk.Button(root, text="Watch", command=run_auto)
button_watch.pack(pady=20)

# Tạo Text widget để hiển thị log
log_text = tk.Text(root, height=20, width=70)
log_text.pack(pady=10)


# Chạy vòng lặp giao diện người dùng
root.mainloop()
