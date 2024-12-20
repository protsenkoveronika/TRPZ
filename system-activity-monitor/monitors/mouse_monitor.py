import time
from pynput import mouse
import threading

class MouseMonitor:
    def __init__(self, gui_var):
        self.current_position = (0, 0)
        self.last_click_event = None
        self.activity_flag = True
        self.last_mouse_activity_time = time.time()
        self.inactivity_threshold = 10
        self.gui_var = gui_var
        
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )
        self.listener.start()

        self.inactivity_thread = threading.Thread(target=self.check_inactivity, daemon=True)
        self.inactivity_thread.start()

    def collect_data(self):
        return {
            "current_position": self.current_position,
            "last_click_event": self.last_click_event,
            "activity_flag": self.activity_flag
        }
    
    def update_widget(self):
        data = self.collect_data()
        position = f"Mouse position: {data['current_position']}"
        if data['last_click_event']:
            last_click = f"Button pressed: {data['last_click_event']}"
        else:
            last_click = "Button pressed: None"

        activity_status = "Active" if data['activity_flag'] else "Inactive"

        self.gui_var.set(f"{position}  |  {last_click}  |  {activity_status}")


    def on_move(self, x, y):
        self.current_position = (x, y)
        self.last_mouse_activity_time = time.time()
        self.activity_flag = True

    def on_click(self, x, y, button, pressed):
        self.last_click_event = str(button) if pressed else "None"
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
