import datetime
import pygetwindow as gw  # on Windows
from repositories.window_repository import WindowRepository

class WindowMonitor:
    def __init__(self, db_file, gui_var):
        self.repo = WindowRepository(db_file)
        self.gui_var = gui_var
        self.current_window = None
        self.window_usage = {}

    def collect_data(self):
        active_window = self.get_active_window()
        active_window = self.sanitize_window_name(active_window)

        if active_window != self.current_window:
            if self.current_window is not None:
                self.update_window_usage(self.current_window)
            
            self.current_window = active_window
            if active_window not in self.window_usage:
                self.window_usage[active_window] = 0

        self.window_usage[self.current_window] += 1
        
        self.check_midnight_reset()

        return {"active_window": self.current_window, "usage_time": self.window_usage[self.current_window]}
    
    def update_widget(self):
        data = self.collect_data()
        self.gui_var.set(f"Active Window: {data['active_window']}")

    def sanitize_window_name(self, window_name):
        if window_name:
            parts = window_name.rsplit(' - ', 1)
            if len(parts) > 1:
                sanitized_name = parts[1]
            else:
                sanitized_name = window_name.strip()
            return sanitized_name.strip()
        return "Unknown"


    def update_window_usage(self, window_name):
        usage_time = self.window_usage.get(window_name, 0)
        # print(f"Час використання вікна '{window_name}': {usage_time} сек.")
        
    def get_active_window(self):
        try:
            window = gw.getActiveWindow()
            if window is not None:
                return window.title
            else:
                return "Unknown"
        except Exception as e:
            print(f"Error getting active window: {e}")
            return "Unknown"

    def save_usage_data(self):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if not self.repo.current_date_exists(current_date):
            self.repo.insert_current_date()

        for window_name, usage_time in self.window_usage.items():
            if window_name != "Unknown":
                self.repo.insert_window_usage(window_name, usage_time)

    def check_midnight_reset(self):
        current_time = datetime.datetime.now().time()
        if current_time.hour == 0 and current_time.minute == 0:
            self.save_usage_data()
            self.window_usage = {}