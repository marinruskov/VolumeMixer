import customtkinter as ctk

class TopBar:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, height=40, fg_color="#222222")
        self.frame.pack(fill="x")

        self.home_button = ctk.CTkButton(self.frame, text="Home")
        self.home_button.pack(side="left", padx=10, pady=5)

        self.settings_button = ctk.CTkButton(self.frame, text="Settings")
        self.settings_button.pack(side="left", padx=10, pady=5)

    def set_home_action(self, action):
        self.home_button.configure(command=action)

    def set_settings_action(self, action):
        self.settings_button.configure(command=action)