import re
import pystray
from pystray import MenuItem as item
import pygetwindow as gw
import win32gui
import win32con
from PIL import Image
from utility import get_resource_path

is_client_hidden = False
window_handle = None

image = Image.open(get_resource_path("images/favicon.ico"))

def toggle_client_visibility(root, icon):
    global is_client_hidden, window_handle
    pattern = re.compile(r'\b\w{12}\b')

    if window_handle is None:
        for window in gw.getAllWindows():
            if pattern.fullmatch(window.title):
                window_handle = window._hWnd
                break

    if window_handle:
        if is_client_hidden:
            root.deiconify()
            win32gui.ShowWindow(window_handle, win32con.SW_SHOW)
            is_client_hidden = False
        else:
            root.withdraw()
            win32gui.ShowWindow(window_handle, win32con.SW_HIDE)
            is_client_hidden = True
        update_menu(icon)
    else:
        print("Window not found")

def update_menu(icon):
    global is_client_hidden
    icon.menu = pystray.Menu(
        item('Show Sailor Client' if is_client_hidden else 'Hide Sailor Client', lambda: toggle_client_visibility(root, icon)),
        item('Quit', lambda: icon.stop())
    )
    icon.update_menu()

def setup_tray_icon(root):
    icon = pystray.Icon("Sailor Hide")
    icon.icon = image
    icon.title = "Sailor Hide"
    update_menu(icon)
    icon.run()

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    setup_tray_icon(root)
