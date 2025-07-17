import Quartz.CoreGraphics as CG
from AppKit import NSWorkspace
import os
import pyautogui
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data import array as channels
from common.send_mail import send_email


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

                # Nhập text vào vùng input
                pyautogui.sleep(1)
                print(f"Nhập kênh tìm kiếm: {channel}")
                pyautogui.write(channel)

                # click vào vị trí đó search
                pyautogui.sleep(1)
                print("Thực hiện sự kiện search") 
                pyautogui.click(x + 355, y + 76)

                # click vào vị trí user
                print("Nhấn vào người dùng")
                pyautogui.sleep(5)
                pyautogui.click(x + 39, y + 205)

                # click vào video
                pyautogui.sleep(5)
                print("Nhấn vào xem video")
                pyautogui.click(x + 61, y + 426)

                # Xem 3 video cho mỗi kênh
                for i in range(3):
                    # xem video 5s
                    print(f"Xem video {i+1} trong vòng 5s")
                    pyautogui.sleep(5)

                    if i < 2:  # Không cần chuyển video ở lần cuối
                        print("Chuyển video mới")
                        # click và giữ chuột tại vị trí A
                        pyautogui.mouseDown(x + 184, y + 550)
                        # kéo chuột đến vị trí B 
                        pyautogui.moveTo(x + 189, y + 147)
                        # thả chuột
                        pyautogui.mouseUp()
    
    
    
    # Send email notification when done
    # print("Gửi email notification...")
    # send_email(
    #     subject="Auto Bot TikTok",
    #     body="Auto watch TikTok done",
    #     receiver_email="khoivinh282828@gmail.com"
    # )

    print("----------Kết thúc BOT AUTO WATCH----------")
else:
    print(f"Không tìm thấy ứng dụng {app_name} đang chạy.")
