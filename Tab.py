import Mixer
import Keybinds
import XML


#from pynput import keyboard, mouse

def set_volume_increment(value):
    if value is None:
        Tab.volume_increment = XML.load_increment_value()
    else:
        Tab.volume_increment = value
    if Tab.volume_increment is None:
        Tab.volume_increment = 5

class Tab:
    volume_increment = None  # Will be set from SettingsPage

    def __init__(self, session, ctk, scrollable_frame):
        # Processed volume as int
        self.initial_volume = 0
        self.volume = 0
        # Raw volume query interface
        self.raw_volume = None
        self.inc_hotkey = None
        self.dec_hotkey = None

        self.session = session
        self.ctk = ctk
        self.scrollable_frame = scrollable_frame
        self.frame = None
        self.get_initial_volume()
        set_volume_increment(None)

    def get_initial_volume(self):
        try:
            self.raw_volume = self.session._ctl.QueryInterface(Mixer.ISimpleAudioVolume)
            self.volume = int(self.raw_volume.GetMasterVolume() * 100)
        except Exception as e:
            print(f"Error getting volume: {e}")

    def increase_volume(self, slider):
        if not self.volume + Tab.volume_increment > 100:
            self.volume += Tab.volume_increment
            self.update_volume(self.volume)
            if slider.winfo_exists():
                slider.set(self.volume)
        else:
            self.volume = 100
            self.update_volume(self.volume)

    def decrease_volume(self, slider):
        if not self.volume - Tab.volume_increment < 0:
            self.volume -= Tab.volume_increment
            self.update_volume(self.volume)
            if slider.winfo_exists():
                slider.set(self.volume)
        else:
            self.volume = 0
            self.update_volume(self.volume)

    def create_tab(self):
        def bind_inc_hotkeys(*args):
            if inc_char_var.get() != "Select Character" and inc_modifier_var.get() != "Select Modifier":
                if self.inc_hotkey:
                    self.inc_hotkey.stop_hotkey()
                self.inc_hotkey = Keybinds.HotkeyListener(inc_modifier_var.get(), inc_char_var.get(),
                                                          lambda: self.increase_volume(slider))
                XML.save_keybinds(
                    self.session.Process.name() if self.session.Process and self.session.Process.name() is not None else "System Sounds",
                    inc_modifier_var.get() if inc_modifier_var.get() is not None else "Select Modifier",
                    inc_char_var.get() if inc_char_var.get() is not None else "Select Character",
                    dec_modifier_var.get() if dec_modifier_var.get() is not None else "Select Modifier",
                    dec_char_var.get() if dec_char_var.get() is not None else "Select Character"
                )

        def bind_dec_hotkeys(*args):
            if dec_char_var.get() != "Select Character" and dec_modifier_var.get() != "Select Modifier":
                if self.dec_hotkey:
                    self.dec_hotkey.stop_hotkey()
                self.dec_hotkey = Keybinds.HotkeyListener(dec_modifier_var.get(), dec_char_var.get(),
                                                          lambda: self.decrease_volume(slider))
                XML.save_keybinds(
                    self.session.Process.name() if self.session.Process and self.session.Process.name() is not None else "System Sounds",
                    inc_modifier_var.get() if inc_modifier_var.get() is not None else "Select Modifier",
                    inc_char_var.get() if inc_char_var.get() is not None else "Select Character",
                    dec_modifier_var.get() if dec_modifier_var.get() is not None else "Select Modifier",
                    dec_char_var.get() if dec_char_var.get() is not None else "Select Character"
                )

        volume = self.volume

        self.frame = self.ctk.CTkFrame(self.scrollable_frame, height=130, fg_color="#363636")
        self.frame.pack_propagate(False)
        self.frame.pack(fill="both", pady=10)

        label = self.ctk.CTkLabel(self.frame,
                                  text=self.session.Process.name() if self.session.Process else "System Sounds",
                                  font=("Arial", 17))
        label.pack(side="left", padx=10)

        # Create a StringVar to dynamically update the value label
        self.value_var = self.ctk.StringVar(value=str(self.volume))

        slider = self.ctk.CTkSlider(self.frame, from_=0, to=100, width=200, height=20, command=self.update_volume,
                                    number_of_steps=50)
        slider.pack(side="right", padx=5)
        slider.set(self.volume)
        value_label = self.ctk.CTkLabel(self.frame, textvariable=self.value_var,
                                        font=("Arial", 17), width=30)
        value_label.pack(side="right", padx=5)

        frame_hotkeys = self.ctk.CTkFrame(self.frame, height=35, fg_color="#363636")
        frame_hotkeys.pack(side="right", pady=5, padx=2)

        # Increase hotkey
        # Frame
        inc_frame_hotkeys = self.ctk.CTkFrame(frame_hotkeys, fg_color="#363636")
        inc_frame_hotkeys.pack(side="top", pady=10)

        # Label
        inc_label_hotkeys = self.ctk.CTkLabel(inc_frame_hotkeys, text="Increase Hotkeys: ",
                                              font=("Arial", 12, "bold"))
        inc_label_hotkeys.pack(side="left")

        # Option Menus
        inc_char_var = self.ctk.StringVar(value="Select Character")
        inc_char_menu = self.ctk.CTkOptionMenu(inc_frame_hotkeys, variable=inc_char_var, command=bind_inc_hotkeys,
                                               values=["Scroll Up", "Scroll Down"] + [chr(i) for i in range(48, 96)])
        inc_char_menu.pack(side="right")

        inc_modifier_var = self.ctk.StringVar(value="Select Modifier")
        inc_modifier_menu = self.ctk.CTkOptionMenu(inc_frame_hotkeys, variable=inc_modifier_var,
                                                   command=bind_inc_hotkeys,
                                                   values=["Shift", "Ctrl", "Alt"])
        inc_modifier_menu.pack(side="right")

        # Decrease hotkey
        # Frame
        dec_frame_hotkeys = self.ctk.CTkFrame(frame_hotkeys, fg_color="#363636")
        dec_frame_hotkeys.pack(side="bottom", pady=10)

        # Label
        dec_label_hotkeys = self.ctk.CTkLabel(dec_frame_hotkeys, text="Decrease Hotkeys: ",
                                              font=("Arial", 12, "bold"))
        dec_label_hotkeys.pack(side="left")

        # Option Menus
        dec_char_var = self.ctk.StringVar(value="Select Character")
        dec_char_menu = self.ctk.CTkOptionMenu(dec_frame_hotkeys, variable=dec_char_var, command=bind_dec_hotkeys,
                                               values=["Scroll Up", "Scroll Down"] + [chr(i) for i in range(48, 96)])
        dec_char_menu.pack(side="right")

        dec_modifier_var = self.ctk.StringVar(value="Select Modifier")
        dec_modifier_menu = self.ctk.CTkOptionMenu(dec_frame_hotkeys, variable=dec_modifier_var,
                                                   command=bind_dec_hotkeys,
                                                   values=["Shift", "Ctrl", "Alt"])
        dec_modifier_menu.pack(side="right")

        # Load existing keybinds if available
        inc_mod, inc_char, dec_mod, dec_char = XML.load_keybinds(
            self.session.Process.name() if self.session.Process else "System Sounds")
        if inc_mod and inc_char:
            inc_modifier_var.set(inc_mod)
            inc_char_var.set(inc_char)
            bind_inc_hotkeys()
        if dec_mod and dec_char:
            dec_modifier_var.set(dec_mod)
            dec_char_var.set(dec_char)
            bind_dec_hotkeys()

    def destroy_tab(self):
        if self.frame:
            self.frame.destroy()
            self.frame = None

    def show_tab_info(self):
        return f"Tab Info: {self.session}"

    def update_volume(self, value):
        try:
            #volume = self.session._ctl.QueryInterface(Mixer.ISimpleAudioVolume)
            self.raw_volume.SetMasterVolume(value / 100, None)
            self.volume = int(value)
            self.value_var.set(str(int(value)))
        except Exception as e:
            print(f"Error setting volume for {self.session.Process.name()}: {e}")
