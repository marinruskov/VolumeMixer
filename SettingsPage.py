import customtkinter as ctk
import FloatSpinbox
import XML
from Tab import set_volume_increment


class SettingsPage:
    def __init__(self, parent):
        self.spinbox_1 = None
        self.frame = ctk.CTkFrame(parent, fg_color="#111111")

        self.input_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.input_frame.pack(padx=10, pady=20, anchor="w")
        self.startup_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.startup_frame.pack(padx=10, pady=20, anchor="w")

        self.label = ctk.CTkLabel(self.input_frame, text="Increment Value:", font=("Arial", 16))
        self.label.pack(side="left", padx=(0, 10))

        self.spinbox_1 = FloatSpinbox.FloatSpinbox(self.input_frame, width=150, step_size=5,
                                                   command=lambda: self.save_increment_value(self.spinbox_1.get()))
        self.spinbox_1.pack(side="left")
        self.spinbox_1.set(XML.load_increment_value())

        self.label = ctk.CTkLabel(self.startup_frame, text="Start application on system startup:", font=("Arial", 16))
        self.label.pack(side="left", padx=(0, 10))
        self.startup_var = ctk.BooleanVar(value=XML.load_startup_enabled())
        self.startup_checkbox = ctk.CTkCheckBox(
            self.startup_frame,
            text=" ",
            variable=self.startup_var,
            command=self.toggle_run_on_startup
        )
        self.startup_checkbox.pack(pady=(0, 0), anchor="w")

    def toggle_run_on_startup(self):
        from main import toggle_startup
        enabled = self.startup_var.get()
        XML.save_startup_enabled(enabled)
        toggle_startup()


    def show(self):
        self.frame.pack(fill="both", expand=True, pady=10)

    def hide(self):
        self.frame.pack_forget()

    def save_increment_value(self, value):
        XML.save_increment_value(value)
        set_volume_increment(value)
        print(f"Increment value set to: {value}")
