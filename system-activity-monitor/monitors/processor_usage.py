import threading
import psutil
import datetime
from repositories.processor_repository import ProcessorRepository
from repositories.monitoring_days_repository import MonitoringDaysRepository

class ProcessorUsage:
    def __init__(self, db_file, gui_var):
        self.repo = ProcessorRepository(db_file)
        self.daysrepo = MonitoringDaysRepository(db_file)
        self.gui_var = gui_var
        self.cpu_data = []

    def collect_data(self):
        usage = psutil.cpu_percent(interval=1)
        self.cpu_data.append(usage)
        # print(f"Collected CPU usage: {usage}, Current data: {self.cpu_data}")
        self.check_hourly_reset()
        return {"cpu_usage": usage}
    
    def update_widget(self):
        data = self.collect_data()
        self.gui_var.set(f"CPU Usage: {data['cpu_usage']}%")

    def save_data(self):
        if not self.cpu_data:
            print("No CPU data collected yet.")
            return

        average_usage = self.calculate_average_cpu_usage()
        timestamp = self.get_previous_hour_timestamp()
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        date_id = self.daysrepo.get_or_add_date_id(today_date)
        if date_id is None:
            print("Failed to save data: date_id could not be determined.")
            return
        
        self.repo.insert_processor_usage(date_id, timestamp, average_usage)
        self.cpu_data = []
        # pass

    def calculate_average_cpu_usage(self):
        if not self.cpu_data:
            print("No CPU data collected yet.")
            return 0
        
        print(f"Calculating average with data: {self.cpu_data}")
        average_usage = sum(self.cpu_data) / len(self.cpu_data)
        print("Average CPU usage:", round(average_usage, 2))
        return round(average_usage, 2)

    def get_previous_hour_timestamp(self):
        now = datetime.datetime.now()
        
        if now.minute != 0:
            previous_hour = now.replace(minute=0, second=0, microsecond=0)
        else:
            previous_hour = now - datetime.timedelta(hours=1)
        
        return previous_hour.strftime("%H:%M:%S")

    def check_hourly_reset(self):
        current_time = datetime.datetime.now()
        if current_time.minute == 0 and current_time.second == 0:
            self.save_data()
