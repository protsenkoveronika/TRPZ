import datetime
import pygetwindow as gw  # on Windows
from repositories.monitoring_days_repository import MonitoringDaysRepository
from repositories.window_repository import WindowRepository

class WindowMonitor:
    def __init__(self, db_file, gui_var):
        self.repo = WindowRepository(db_file)
        self.daysrepo = MonitoringDaysRepository(db_file)
        self.gui_var = gui_var
        self.current_window = None
        self.window_usage = {}
        self.is_active = True
        self.last_activity_time = None

    def check_activity(self, is_active):
        if not is_active and self.is_active:
            self.stop_tracking()

        self.is_active = is_active

    def stop_tracking(self):
        if self.current_window:
            self.update_window_usage(self.current_window)

    def collect_data(self):
        if not self.is_active:
            return {"active_window": "Unknown", "usage_time": 0}
        
        active_window = self.get_active_window()
        active_window = self.sanitize_window_name(active_window)

        if active_window == "Unknown":
            self.check_midnight_reset()
            print(self.window_usage)
            return {"active_window": "Unknown", "usage_time": 0}

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

    def save_data(self):
        if not self.window_usage:
            print("No window data collected yet.")
            return

        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        date_id = self.daysrepo.get_or_add_date_id(today_date)
        if date_id is None:
            print("Failed to save data: date_id could not be determined.")
            return
        
        for window_name, time in self.window_usage.items():
            window_id = self.repo.get_or_add_window_id(window_name)
            if window_id is None:
                print(f"Failed to save usage for window: {window_name} (window_id could not be determined).")
                continue
            
            try:
                self.repo.insert_window_usage(date_id, window_id, time)
                print(f"Saved usage data for window: {window_name}, time: {time} seconds.")
            except Exception as e:
                print(f"Error saving usage data for window: {window_name}, time: {time}. Error: {e}")

        self.window_usage = {}
        # pass

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

    def check_midnight_reset(self):
        current_time = datetime.datetime.now().time()
        if current_time.hour == 0 and current_time.minute == 0:
            self.save_data()