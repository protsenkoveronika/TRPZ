import time
from pynput import keyboard
import threading

class KeyboardMonitor:
    def __init__(self, gui_var):
        self.current_key = None
        self.activity_flag = True
        self.last_keypress_time = time.time()
        self.inactivity_threshold = 10
        self.gui_var = gui_var

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

        self.inactivity_thread = threading.Thread(target=self.check_inactivity, daemon=True)
        self.inactivity_thread.start()

    def on_press(self, key):
        try:
            self.current_key = key.char
        except AttributeError:
            self.current_key = str(key)
        
        self.last_keypress_time = time.time()
        self.activity_flag = True

    def on_release(self, key):
        self.current_key = None

    def collect_data(self):
        return {
            "current_key": self.current_key,
            "activity_flag": self.activity_flag,
        }

    def update_widget(self):
        data = self.collect_data()
        if data["current_key"]:
            key_info = f"Keyboard key pressed: {data['current_key']}"
        else:
            key_info = "Keyboard key pressed: None"

        activity_status = "Active" if data["activity_flag"] else "Inactive"
        self.gui_var.set(f"{key_info}  |  Activity: {activity_status}")


    def check_inactivity(self):
        while True:
            current_time = time.time()
            if current_time - self.last_keypress_time > self.inactivity_threshold:
                if self.activity_flag:
                    print("No activity for 10 minutes.")
                self.activity_flag = False
            time.sleep(1)
