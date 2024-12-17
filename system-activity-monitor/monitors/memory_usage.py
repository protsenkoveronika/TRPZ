import psutil
import datetime
from repositories.memory_repository import MemoryRepository
from repositories.monitoring_days_repository import MonitoringDaysRepository

class MemoryUsage:
    def __init__(self, db_file, gui_var):
        self.repo = MemoryRepository(db_file)
        self.daysrepo = MonitoringDaysRepository(db_file)
        self.gui_var = gui_var
        self.memory_data = [] 
        self.average_data = []

    def collect_data(self):
        used_memory = int(psutil.virtual_memory().used / (1024 ** 2))
        self.memory_data.append(used_memory)
        self.check_hourly_reset()
        return {"memory_usage": used_memory}
    
    def update_widget(self):
        data = self.collect_data()
        self.gui_var.set(f"Memory Usage: {data['memory_usage']} MB")

    def calculate_average_memory_usage(self):
        if not self.memory_data:
            print("No memory data collected yet.")
            return 0
        
        print(f"Calculating average with data: {self.memory_data}")
        average_memory = sum(self.memory_data) / len(self.memory_data)
        print("Average memory usage:", round(average_memory, 2))
        return round(average_memory, 2)
    
    def save_data(self):
        if not self.memory_data:
            print("No memory data collected yet.")
            return

        average_usage = self.calculate_average_memory_usage()
        timestamp = self.get_previous_hour_timestamp()
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        date_id = self.daysrepo.get_or_add_date_id(today_date)
        if date_id is None:
            print("Failed to save data: date_id could not be determined.")
            return
        self.repo.insert_memory_usage(date_id, timestamp, average_usage)
        self.memory_data = []
        # pass

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