import Quartz.CoreGraphics as CG
from AppKit import NSWorkspace
import os
import pyautogui
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data import array as channels
from common.send_mail import send_email
import random

app_name = 'BlueStacks'  # Thay thế với tên ứng dụng bạn muốn tìm

# Tìm tất cả các cửa sổ của ứng dụng đang mở
def get_windows_of_app(app_name):
    workspace = NSWorkspace.sharedWorkspace()
    app_list = workspace.runningApplications()
    
    windows = []
    for app in app_list:
        if app.localizedName() == app_name:
            windows.append(app)
    return windows

# Lấy tất cả các cửa sổ của ứng dụng BlueStacks
apps = get_windows_of_app(app_name)

if apps:
    # Nếu tìm thấy, lấy thông tin cửa sổ (ví dụ vị trí của cửa sổ)
    window_info = CG.CGEventSourceCreate(CG.kCGEventSourceStateHIDSystemState)
    # Lấy vị trí của cửa sổ
    window_list = CG.CGWindowListCopyWindowInfo(CG.kCGWindowListOptionOnScreenOnly | CG.kCGWindowListExcludeDesktopElements, CG.kCGNullWindowID)
    found_windows = []
    for window in window_list:
        if window.get(CG.kCGWindowOwnerName, '') == app_name:
            # Lấy vị trí và kích thước của cửa sổ
            x = window.get(CG.kCGWindowBounds, {}).get('X', 0)
            y = window.get(CG.kCGWindowBounds, {}).get('Y', 0)
            width = window.get(CG.kCGWindowBounds, {}).get('Width', 0)
            height = window.get(CG.kCGWindowBounds, {}).get('Height', 0)
            kCGWindowOwnerPID = window.get(CG.kCGWindowOwnerPID, 0)
            kCGWindowName = window.get(CG.kCGWindowName, '')
            print(f"----------Tìm thấy cửa sổ BlueStacks: {kCGWindowName} - PID: {kCGWindowOwnerPID} tại vị trí: x={x}, y={y}. Kích thước hiện tại: width={width}, height={height}----------")

            # # lấy vị trị tương đối của chuột trong app
            # # Đợi 5 giây
            # pyautogui.sleep(5)
            # # Lấy vị trí hiện tại của chuột
            # current_x, current_y = pyautogui.position()
            # # Tính toán vị trí tương đối so với cửa sổ
            # relative_x = current_x - x
            # relative_y = current_y - y
            # print(f"Vị trí tương đối: x={relative_x}, y={relative_y}")
            # exit()

            # Kết nối ứng dụng
            print(f"Mở ứng dụng {app_name} - PID: {kCGWindowOwnerPID} - Tên cửa sổ: {kCGWindowName}")
            os.system(f"open -a {app_name}")
            # Đưa cửa sổ lên trên cùng
            applescript = f"""
            tell application "{app_name}"
                activate
                set frontmost to true
            end tell
            """
            os.system(f"osascript -e '{applescript}'")
            pyautogui.sleep(1)  # Đợi ứng dụng khởi động lâu hơn
            # exit()
            # Click vào cửa sổ để kích hoạt focus
            pyautogui.click(x + width//2, y + height//2)  # Click vào giữa cửa sổ
            pyautogui.sleep(0.5)  # Đợi một chút để focus được kích hoạt

            # click vào vị trí search
            pyautogui.sleep(1)
            print("Nhấn vào nút search")
            pyautogui.click(x + 370, y + 79)

            # Danh sách các kênh cần xem
            # Format channel URLs to usernames by removing the domain prefix
            channels = [channel.replace('https://www.tiktok.com/', '') for channel in channels]

            for channel in channels:
                if channel != channels[0]:  # Nếu không phải channel đầu tiên
                    pyautogui.sleep(1)
                    print("Click vào icon search nhỏ")
                    pyautogui.click(x + 68, y + 76)

                    pyautogui.sleep(1)
                    print("Click vào icon xoá search")
                    pyautogui.click(x + 308, y + 76)
                    pyautogui.sleep(1)

                # Nhập text vào vùng input
                pyautogui.sleep(2)
                print(f"Nhập kênh tìm kiếm: {channel}")
                pyautogui.typewrite(channel)

                # click vào vị trí đó search
                pyautogui.sleep(2)
                print("Thực hiện search") 
                pyautogui.click(x + 355, y + 76)

                # click follow
                print("Nhấn vào follow người dùng")
                pyautogui.sleep(5)
                try:
                    # Tìm vị trí của hình ảnh trên màn hình
                    # Thay 'ten_hinh_anh.png' bằng đường dẫn đến file hình ảnh của bạn
                    image_location = pyautogui.locateOnScreen('./images/follow.png', confidence=0.8)
                    
                    if image_location is not None:
                        # Tính toán tọa độ trung tâm của hình ảnh
                        image_center = pyautogui.center(image_location)  # Tọa độ trung tâm (x, y)
                        pyautogui.click(image_center)
                    else:
                        print("Không tìm thấy hình ảnh follow trên màn hình")

                except Exception as e:
                    print(f"Có lỗi xảy ra: {e} Có thể đã follow rồi")
    
    
    # Send email notification when done
    # print("Gửi email notification...")
    # send_email(
    #     subject="Auto Bot TikTok",
    #     body="Auto follow TikTok done",
    #     receiver_email="khoivinh282828@gmail.com"
    # )

    print("----------Kết thúc BOT AUTO FOLLOW----------")
else:
    print(f"Không tìm thấy ứng dụng {app_name} đang chạy.")
