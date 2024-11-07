import time
from pynput import mouse
import threading

class MouseMonitor:
    def __init__(self):
        self.current_position = (0, 0)
        self.activity_flag = True
        self.last_mouse_activity_time = time.time()
        self.inactivity_threshold = 10

    def on_move(self, x, y):
        self.current_position = (x, y)
        print(f"Mouse moved to: {self.current_position}")
        self.last_mouse_activity_time = time.time()
        self.activity_flag = True

    def on_click(self, x, y, button, pressed):
        action = 'pressed' if pressed else 'released'
        print(f"Mouse {action} at ({x}, {y}) with {button}.")
        self.last_mouse_activity_time = time.time()
        self.activity_flag = True

    def check_inactivity(self):
        while True:
            current_time = time.time()
            if current_time - self.last_mouse_activity_time > self.inactivity_threshold:
                if self.activity_flag:
                    print("No mouse activity for 10 minutes.")
                self.activity_flag = False
            time.sleep(1)

    def start_monitoring(self):
        inactivity_thread = threading.Thread(target=self.check_inactivity)
        inactivity_thread.daemon = True
        inactivity_thread.start()

        with mouse.Listener(on_move=self.on_move, on_click=self.on_click) as listener:
            listener.join()
