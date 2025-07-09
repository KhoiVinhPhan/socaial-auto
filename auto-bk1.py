import pyautogui

# # Đợi 5 giây để người dùng di chuyển chuột đến vị trí cần lấy tọa độ
# print("Bạn có 5 giây để di chuyển chuột đến vị trí cần lấy tọa độ...")
# pyautogui.sleep(5)
# # Lấy vị trí hiện tại của con trỏ chuột
# x, y = pyautogui.position()
# # In ra tọa độ
# print(f'Tọa độ vị trí bạn đã click: x={x}, y={y}')
# exit()

print("Program is running...")
pyautogui.sleep(3)

# click app
print("Kết nối thiết bị")
pyautogui.click(450, 116)

# click vào vị trí đó search
print("Nhấn vào nút search")
pyautogui.sleep(1)
pyautogui.click(450, 116)

# Nhập text vào vùng input
print("Nhập kênh tìm kiếm")
pyautogui.sleep(1)
pyautogui.typewrite('@perri_kiely_02')

# click vào vị trí đó search
print("Thực hiện search")
pyautogui.sleep(1)
pyautogui.click(437, 116)

# click vào vị trí user
print("Nhấn vào người dùng")
pyautogui.sleep(1)
pyautogui.click(40, 243)


# click vào video
print("Nhấn vào xem video")
pyautogui.sleep(3)
pyautogui.click(73, 509)


# xem video 5s
print("Xem video trong vòng 5s")
pyautogui.sleep(5)


print("Chuyển video mới")
# click và giữ chuột tại vị trí A
pyautogui.mouseDown(x=226, y=621)
# kéo chuột đến vị trí B 
pyautogui.moveTo(x=234, y=250)
# thả chuột
pyautogui.mouseUp()

# xem video 5s
print("Xem video trong vòng 5s")
pyautogui.sleep(5)

print("Chuyển video mới")
# click và giữ chuột tại vị trí A
pyautogui.mouseDown(x=226, y=621)
# kéo chuột đến vị trí B 
pyautogui.moveTo(x=234, y=250)
# thả chuột
pyautogui.mouseUp()

# xem video 5s
print("Xem video trong vòng 5s")
pyautogui.sleep(5)

print("Chuyển video mới")
# click và giữ chuột tại vị trí A
pyautogui.mouseDown(x=226, y=621)
# kéo chuột đến vị trí B 
pyautogui.moveTo(x=234, y=250)
# thả chuột
pyautogui.mouseUp()







print("Program is completed")








# # Đợi 5 giây
# pyautogui.sleep(5)

# # Lấy vị trí hiện tại của con trỏ chuột
# current_mouse_x, current_mouse_y = pyautogui.position()
# print(f'Vị trí con trỏ chuột: x={current_mouse_x}, y={current_mouse_y}')

# # Click vào vị trí hiện tại của con trỏ chuột
# pyautogui.click(current_mouse_x, current_mouse_y)

# # dừng chương trình
# exit()



# Press Command + Space to open Spotlight Search on MacBook
# pyautogui.hotkey('command', 'space')
# pyautogui.hotkey('command', 'space')

# # đợi 1 giây
# pyautogui.sleep(1)

# # nhập vào text là vào 
# pyautogui.typewrite('google Chrome')

# # đợi 3 giây
# pyautogui.sleep(2)

# # nhấn enter
# pyautogui.press('enter')



# # Đợi 2 giây để Chrome khởi động
# pyautogui.sleep(3)

# # Mở tab mới bằng Command + T
# pyautogui.hotkey('command', 't')

# # Đợi 1 giây để đảm bảo tab mới đã mở
# pyautogui.sleep(1)


# # Nhập URL TikTok
# pyautogui.typewrite('https://www.tiktok.com/@ong6camau')

# # Nhấn enter để truy cập trang
# pyautogui.press('enter')

# # Đợi 2 giây để trang TikTok load hoàn toàn
# pyautogui.sleep(2)

# pyautogui.click(560, 265)

# pyautogui.sleep(2)

# pyautogui.hotkey('command', 'l')

# pyautogui.typewrite('https://www.tiktok.com/@p_shiri')

# pyautogui.press('enter')

# pyautogui.sleep(2)

# pyautogui.click(560, 265)




# try:
#     # Tìm vị trí của hình ảnh trên màn hình
#     # Thay 'ten_hinh_anh.png' bằng đường dẫn đến file hình ảnh của bạn
#     image_location = pyautogui.locateOnScreen('./images/image1.png', confidence=0.8)
#     print('image_location', image_location)
    
#     if image_location is not None:
#          # Tính toán tọa độ trung tâm của hình ảnh
#         image_center = pyautogui.center(image_location)  # Tọa độ trung tâm (x, y)
#         print('image_center', image_center)

#         # Click vào vị trí của hình ảnh
#         print('click vào vị trí của hình ảnh')
#         pyautogui.click(image_center)
#     else:
#         print("Không tìm thấy hình ảnh trên màn hình")

# except Exception as e:
#     print(f"Có lỗi xảy ra: {e}")






