import pystray
from PIL import Image
from threading import Thread
import os
import sys

tray_icon = None
tray_running = False  # Flag to check if the tray icon is running

def hide_window(app, event=None):
    try:
        global tray_icon, tray_running
        app.withdraw()
        if not tray_running:  # Only create the tray icon if it's not already running
            try:
                image = Image.open(resource_path("icon.png"))
            except Exception as e:
                print(f"Error loading icon.png: {e}")
            menu = (pystray.MenuItem('Show', lambda icon, item: show_app(app, icon, item), default=True),
                    pystray.MenuItem('Quit', lambda icon, item: quit_app(app, icon, item)))
            tray_icon = pystray.Icon("name", image, "Custom Volume Mixer", menu)
            tray_running = True
            Thread(target=tray_icon.run).start()
    except Exception as e:
        print(f"Error in hide_window: {e}")

def show_app(app, icon, item):
    global tray_icon, tray_running
    icon.stop()
    tray_icon = None
    tray_running = False
    app.after(0, app.deiconify)

def quit_app(app, icon, item):
    icon.stop()
    app.quit()

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller packs files into a temp dir
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)

