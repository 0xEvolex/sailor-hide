import re
import pystray
from pystray import MenuItem as item
import pygetwindow as gw
import win32gui
import win32con
from PIL import Image
from utility import get_resource_path
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

is_client_hidden = False
window_handle = None
window_title = None

image = Image.open(get_resource_path("images/favicon.ico"))

def toggle_client_visibility(root, icon):
    global is_client_hidden, window_handle, window_title
    pattern = re.compile(r'\b\w{12}\b', re.UNICODE)

    def enum_window_callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        logging.debug(f"Checking window: {title}")
        if pattern.fullmatch(title):
            global window_handle, window_title
            window_handle = hwnd
            window_title = title
            logging.info(f"Window detected: {title}")
            return False  # Stop enumeration
        return True  # Continue enumeration

    # Always search for the window to handle randomized titles
    logging.debug("Searching for window with 12-character title...")
    window_handle = None
    window_title = None
    win32gui.EnumWindows(enum_window_callback, None)

    if window_handle:
        if is_client_hidden:
            logging.info(f"Showing Sailor Client window: {window_title}")
            root.deiconify()
            win32gui.ShowWindow(window_handle, win32con.SW_SHOW)
            is_client_hidden = False
        else:
            logging.info(f"Hiding Sailor Client window: {window_title}")
            root.withdraw()
            win32gui.ShowWindow(window_handle, win32con.SW_HIDE)
            is_client_hidden = True
        update_menu(icon)
    else:
        logging.error("Window not found")

def update_menu(icon):
    global is_client_hidden
    logging.debug("Updating tray icon menu")
    icon.menu = pystray.Menu(
        item('Show Sailor Client' if is_client_hidden else 'Hide Sailor Client', lambda: toggle_client_visibility(root, icon)),
        item('Quit', lambda: icon.stop())
    )
    icon.update_menu()

def setup_tray_icon(root):
    logging.debug("Setting up tray icon")
    icon = pystray.Icon("Sailor Hide")
    icon.icon = image
    icon.title = "Sailor Hide"
    update_menu(icon)
    icon.run()

if __name__ == "__main__":
    import tkinter as tk
    logging.debug("Starting application")
    root = tk.Tk()
    root.withdraw()
    setup_tray_icon(root)