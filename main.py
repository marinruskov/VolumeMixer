import customtkinter as ctk
import tkinter as tk

import Keybinds
from TopBar import TopBar
from SettingsPage import SettingsPage
from Mixer import getDevices
from Tab import Tab
import Tray
import XML
import os
import sys
from win32com.client import Dispatch


def generate_tabs():
    global tabs
    # Clear existing tabs
    for tab in tabs:
        tab.destroy_tab()
    tabs.clear()

    sessions = getDevices()
    for session in sessions:
        tab = Tab(session, ctk, scrollable_frame)
        tab.create_tab()
        tabs.append(tab)


def show_home():
    settings_page.hide()
    scrollable_frame.pack(fill="both", expand=True, pady=10)
    generate_tabs()


def show_settings():
    scrollable_frame.pack_forget()
    settings_page.show()


def toggle_startup():
    app_name = "CustomVolumeMixer"
    startup = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
    shortcut_path = os.path.join(startup, f"{app_name}.lnk")

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)  # disable startup
    else:
        target = sys.executable
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = target
        shortcut.save()


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller packs files into a temp dir
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)



if __name__ == "__main__":
    # Initialize the main window
    app = ctk.CTk()
    app.geometry("810x470")
    app.title("Custom Volume Mixer")
    try:
        app.iconbitmap(resource_path("icon.ico"))
    except Exception as e:
        print(f"Error setting icon: {e}")
    app.resizable(False, False)
    app.wm_attributes("-alpha", 0.95)
    app.geometry("+700+300")
    ctk.set_default_color_theme("green")

    # Create the top bar
    top_bar = TopBar(app)

    # Create the settings page
    settings_page = SettingsPage(app)

    # Create the scrollable frame for tabs
    scrollable_frame = ctk.CTkScrollableFrame(app, height=50, fg_color="#111111")
    scrollable_frame.pack(fill="both", expand=True, pady=10)

    tabs = []  # List to store generated tabs

    # Define top bar button actions
    top_bar.set_home_action(lambda: show_home())
    top_bar.set_settings_action(lambda: show_settings())
    generate_tabs()

    # Bind the window close event to hide the window instead of closing it
    app.bind("<FocusOut>", lambda event: Tray.hide_window(app, event))
    app.protocol("WM_DELETE_WINDOW", lambda: Tray.hide_window(app))
    app.bind("<FocusIn>", lambda event: generate_tabs())
    Keybinds.HotkeyListener("ctrl", "k", lambda: generate_tabs())

    app.mainloop()


