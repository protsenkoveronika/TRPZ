import time
from pynput import keyboard
import threading

class KeyboardMonitor:
    def __init__(self):
        self.current_key = None
        self.activity_flag = True
        self.last_keypress_time = time.time()
        self.inactivity_threshold = 10 * 60

    def on_press(self, key):
        try:
            self.current_key = key.char
            print(f"Key pressed: {self.current_key}")
        except AttributeError:
            self.current_key = str(key)
            print(f"Special key pressed: {self.current_key}")
        
        self.last_keypress_time = time.time()
        self.activity_flag = True

    def on_release(self, key):
        self.current_key = None
        print("None")

    def check_inactivity(self):
        while True:
            current_time = time.time()
            if current_time - self.last_keypress_time > self.inactivity_threshold:
                if self.activity_flag:
                    print("No activity for 10 minutes.")
                self.activity_flag = False
            time.sleep(1)

    def start_monitoring(self):
        inactivity_thread = threading.Thread(target=self.check_inactivity)
        inactivity_thread.daemon = True
        inactivity_thread.start()

        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
