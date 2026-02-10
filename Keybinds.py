from pynput import keyboard, mouse
import threading


class HotkeyListener:
    def __init__(self, modifier, character, action):
        self.scrollHotkey = False
        self.modifier_pressed = False
        self.stop_event = threading.Event()
        self.listener_thread = None
        self.modifier = modifier.lower()
        self.character = character.lower()
        self.action = action
        if self.character in ['scroll up', 'scroll down']:
            if self.character == "scroll up":
                self.character = "scroll_up"
            elif self.character == "scroll down":
                self.character = "scroll_down"
            self.scrollHotkey = True
        else:
            self.hotkey = f'<{self.modifier}>+{self.character}'
            self.scrollHotkey = False
        self.start_hotkey(action)

    # For plain keyboard hotkeys
    def keyboard_globalHotKeys_listener(self, hotkey):
        def listener():
            with keyboard.GlobalHotKeys(hotkey) as h:
                while not self.stop_event.is_set():
                    h.join(0.1)  # Check periodically if the stop event is set

        self.listener_thread = threading.Thread(target=listener, daemon=True)
        self.listener_thread.start()

    # For scroll wheel hotkeys
    def keyboard_key_listener(self):
        def on_press(key):
            if hasattr(key, 'name') and key.name in [self.modifier, f"{self.modifier}_l", f"{self.modifier}_r"]:
                self.modifier_pressed = True
                #print(self.modifier_pressed)

        def on_release(key):
            if hasattr(key, 'name') and key.name in [self.modifier, f"{self.modifier}_l", f"{self.modifier}_r"]:
                self.modifier_pressed = False
                #print(self.modifier_pressed)

        def listener():
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                while not self.stop_event.is_set():
                    listener.join(0.1)

        self.listener_thread = threading.Thread(target=listener, daemon=True)
        self.listener_thread.start()

    def mouse_listener(self, character):
        def on_scroll(x, y, dx, dy):
            if character == 'scroll_up' and dy > 0 and self.modifier_pressed:
                self.action()
            elif character == 'scroll_down' and dy < 0 and self.modifier_pressed:
                self.action()

        def listener():
            with mouse.Listener(on_scroll=on_scroll) as listener:
                while not self.stop_event.is_set():
                    listener.join(0.1)  # Check periodically if the stop event is set

        self.listener_thread = threading.Thread(target=listener, daemon=True)
        self.listener_thread.start()

    # Start the appropriate listener based on the hotkey type
    def start_hotkey(self, action):
        self.stop_event.clear()
        if not (self.listener_thread and self.listener_thread.is_alive()):
            if self.scrollHotkey:
                self.keyboard_key_listener()
                self.mouse_listener(self.character)
            else:
                self.keyboard_globalHotKeys_listener({self.hotkey: lambda: action()})

    # Stop the hotkey
    def stop_hotkey(self):
        self.stop_event.set()
        print("Stopping hotkey listener for", self.modifier, self.character)
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join()

    def return_hotkey(self):
        return (self.modifier, self.character)

    def is_running(self):
        return self.listener_thread and self.listener_thread.is_alive()

# Example usage
if __name__ == "__main__":
    listener = HotkeyListener("shift", "scroll up", lambda: print("Hotkey pressed!"))
    listener2 = HotkeyListener("ctrl", "h", lambda: print("Hotkey 2 pressed!"))
    listener3 = HotkeyListener("alt", "scroll down", lambda: print("Hotkey 3 pressed!"))

    input("Press Enter to stop the listener...\n")
    listener.stop_hotkey()


    input("Listener stopped. Press Enter to exit...\n")
