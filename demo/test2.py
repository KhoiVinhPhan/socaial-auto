import os

def resize_app_window(app_name, width, height):
    # AppleScript to resize a window of a specific app
    applescript = f"""
    tell application "{app_name}"
        set the bounds of the first window to {{100, 100, {100 + width}, {100 + height}}}
    end tell
    """
    # Execute the AppleScript
    os.system(f"osascript -e '{applescript}'")

# Example usage: Resize the Python window to 800x600
resize_app_window('Bluestacks', 800, 600)
