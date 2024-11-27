import time
import datetime
import pygetwindow as gw  # on Windows
from repositories.window_repository import WindowRepository
from repositories.monitor_repository import MonitorRepository

class WindowMonitor:
    def __init__(self, db_file):
        self.repo = WindowRepository(db_file)
        self.monitorrepo = MonitorRepository(db_file)
        self.current_window = None
        self.window_start_time = None
        self.window_usage = {}

    def get_active_window(self):
        active_window = gw.getActiveWindow()
        if active_window:
            return active_window.title
        return None

    def track_active_window(self):
        active_window = self.get_active_window()
        
        if active_window != self.current_window:
            if self.current_window is not None:
                elapsed_time = time.time() - self.window_start_time
                elapsed_time_minutes = round(elapsed_time / 60, 2)
                self.update_window_usage(self.current_window, elapsed_time_minutes)
            self.current_window = active_window
            self.window_start_time = time.time()
        
        time.sleep(1)

    def update_window_usage(self, window_name, elapsed_time_minutes):
        if window_name not in self.window_usage:
            self.window_usage[window_name] = elapsed_time_minutes
        else:
            self.window_usage[window_name] += elapsed_time_minutes

    def save_usage_data(self):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if not self.monitorrepo.current_date_exists(current_date):
            self.monitorrepo.insert_current_date()
        for window_name, usage_time in self.window_usage.items():
            self.repo.insert_window_usage(window_name, usage_time)

    def check_midnight_reset(self):
        current_time = datetime.datetime.now().time()
        if current_time.hour == 0 and current_time.minute == 0:
            self.save_usage_data()
            self.window_usage = {}

    def start_monitoring(self):
        try:
            while True:
                self.track_active_window()
                self.check_midnight_reset()
        except KeyboardInterrupt:
            print("Window monitoring stopped.")
