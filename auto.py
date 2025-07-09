import pyautogui

from data.data import array as channels


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


# Danh sách các kênh cần xem
# Format channel URLs to usernames by removing the domain prefix
channels = [channel.replace('https://www.tiktok.com/', '') for channel in channels]

for channel in channels:
    if channel != channels[0]:  # Nếu không phải channel đầu tiên
        print("Click thêm lần nữa vào ô search")
        pyautogui.sleep(1)
        pyautogui.click(70, 114)


    # Nhập text vào vùng input
    print(f"Nhập kênh tìm kiếm: {channel}")
    pyautogui.sleep(1)
    pyautogui.typewrite(channel)

    # click vào vị trí đó search
    print("Thực hiện search") 
    pyautogui.sleep(1)
    pyautogui.click(437, 116)

    # click vào vị trí user
    print("Nhấn vào người dùng")
    pyautogui.sleep(5)
    pyautogui.click(40, 243)

    # click vào video
    print("Nhấn vào xem video")
    pyautogui.sleep(3)
    pyautogui.click(73, 509)

    # Xem 3 video cho mỗi kênh
    for i in range(3):
        # xem video 5s
        print(f"Xem video {i+1} trong vòng 5s")
        pyautogui.sleep(5)

        if i < 2:  # Không cần chuyển video ở lần cuối
            print("Chuyển video mới")
            # click và giữ chuột tại vị trí A
            pyautogui.mouseDown(x=226, y=621)
            # kéo chuột đến vị trí B 
            pyautogui.moveTo(x=234, y=250)
            # thả chuột
            pyautogui.mouseUp()



print("Program is completed")
