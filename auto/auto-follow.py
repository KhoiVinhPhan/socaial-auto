import Quartz.CoreGraphics as CG
from AppKit import NSWorkspace
import os
import pyautogui
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.data import array as channels


app_name = 'BlueStacks'  # Thay thế với tên ứng dụng bạn muốn tìm

# Tìm cửa sổ của ứng dụng đang mở
def get_window_of_app(app_name):
    workspace = NSWorkspace.sharedWorkspace()
    app_list = workspace.runningApplications()
    
    for app in app_list:
        if app.localizedName() == app_name:
            return app
    return None

# Thay đổi kích thước cửa sổ của ứng dụng
def resize_app_window(app_name, width, height):
    # AppleScript to resize a window of a specific app
    applescript = f"""
    tell application "{app_name}"
        set the bounds of the first window to {{0, 0, {width}, {height}}}
    end tell
    """
    # Execute the AppleScript
    os.system(f"osascript -e '{applescript}'")

# Thay đổi kích thước cửa sổ của ứng dụng
# resize_app_window(app_name, 463, 798)


# Lấy cửa sổ của ứng dụng Safari
app = get_window_of_app(app_name)

if app:
    # Nếu tìm thấy, lấy thông tin cửa sổ (ví dụ vị trí của cửa sổ)
    window_info = CG.CGEventSourceCreate(CG.kCGEventSourceStateHIDSystemState)
    # Lấy vị trí của cửa sổ
    window_list = CG.CGWindowListCopyWindowInfo(CG.kCGWindowListOptionOnScreenOnly | CG.kCGWindowListExcludeDesktopElements, CG.kCGNullWindowID)
    
    for window in window_list:
        if window.get(CG.kCGWindowOwnerName, '') == app_name:
            # Lấy vị trí và kích thước của cửa sổ
            x = window.get(CG.kCGWindowBounds, {}).get('X', 0)
            y = window.get(CG.kCGWindowBounds, {}).get('Y', 0)
            width = window.get(CG.kCGWindowBounds, {}).get('Width', 0) 
            height = window.get(CG.kCGWindowBounds, {}).get('Height', 0)
            print(f"Vị trí cửa sổ của app: x={x}, y={y}")
            print(f"Kích thước hiện tại của app: width={width}, height={height}")


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
            print(f"Mở ứng dụng {app_name}")
            os.system(f"open -a {app_name}")
            pyautogui.sleep(1)  # Đợi ứng dụng khởi động

            # click vào vị trí search
            print("Nhấn vào nút search")
            pyautogui.sleep(1)
            pyautogui.click(x + 370, y + 79)


            # Danh sách các kênh cần xem
            # Format channel URLs to usernames by removing the domain prefix
            channels = [channel.replace('https://www.tiktok.com/', '') for channel in channels]


            for channel in channels:
                if channel != channels[0]:  # Nếu không phải channel đầu tiên
                    print("Click thêm lần nữa vào ô search")
                    pyautogui.sleep(1)
                    pyautogui.click(x + 68, y + 76)

                    # click vào icon xoá search
                    pyautogui.sleep(1)
                    pyautogui.click(x + 308, y + 77)


                # Nhập text vào vùng input
                print(f"Nhập kênh tìm kiếm: {channel}")
                pyautogui.sleep(1)
                pyautogui.typewrite(channel)

                # click vào vị trí đó search
                print("Thực hiện search") 
                pyautogui.sleep(1)
                pyautogui.click(x + 355, y + 76)

                # click vào vị trí user
                print("Nhấn vào follow người dùng")
                pyautogui.sleep(5)
                try:
                    # Tìm vị trí của hình ảnh trên màn hình
                    # Thay 'ten_hinh_anh.png' bằng đường dẫn đến file hình ảnh của bạn
                    image_location = pyautogui.locateOnScreen('./images/follow.png', confidence=0.8)
                    print('image_location', image_location)
                    
                    if image_location is not None:
                        # Tính toán tọa độ trung tâm của hình ảnh
                        image_center = pyautogui.center(image_location)  # Tọa độ trung tâm (x, y)
                        print('image_center', image_center)
                        pyautogui.click(image_center)
                    else:
                        print("Không tìm thấy hình ảnh follow trên màn hình")

                except Exception as e:
                    print(f"Có lỗi xảy ra: {e}")

            break
    print("Đã follow xong tất cả các kênh")
    print("----------KẾT THÚC CHƯƠNG TRÌNH----------")
    exit()
else:
    print(f"Ứng dụng {app_name} không chạy.")
