import datetime
import time
from repositories.computer_usage_repository import ComputerUsageRepository
from repositories.monitoring_days_repository import MonitoringDaysRepository

class ComputerUsage:
    def __init__(self, db_file, gui_var):
        self.repo = ComputerUsageRepository(db_file)
        self.daysrepo = MonitoringDaysRepository(db_file)
        self.db_file = db_file
        self.gui_var = gui_var
        self.active_time = 0
        self.is_active = False
        self.activity_start_time = None
    
    def start_tracking(self):
        self.activity_start_time = time.time()

    def stop_tracking(self):
        if self.activity_start_time is not None:
            self.active_time += time.time() - self.activity_start_time
            self.activity_start_time = None
    
    def check_activity(self, is_active):
        self.is_active = is_active
        
        if is_active:
            if not self.activity_start_time:
                self.start_tracking()
            else:
                current_time = time.time()
                self.active_time += current_time - self.activity_start_time
                self.activity_start_time = current_time
        else:
            self.stop_tracking()

        self.check_midnight_reset()
        # print(f"Total active time check: {self.active_time:.2f} seconds.  |  {'Active' if self.is_active else 'Inactive'}")
        self.update_widget()


    def update_widget(self):
        self.gui_var.set(f"Computer Usage Time: {self.active_time:.2f} seconds.   |  {'Active' if self.is_active else 'Inactive'}")

    def save_data(self):
        if self.active_time == 0:
            print("No active time data collected yet.")
            return

        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        date_id = self.daysrepo.get_or_add_date_id(today_date)
        if date_id is None:
            print("Failed to save data: date_id could not be determined.")
            return
        
        self.repo.insert_computer_usage(date_id, round(self.active_time, 2))
        self.active_time = 0
        # pass

    def check_midnight_reset(self):
        current_time = datetime.datetime.now().time()
        if current_time.hour == 0 and current_time.minute == 0:
            self.save_data()
