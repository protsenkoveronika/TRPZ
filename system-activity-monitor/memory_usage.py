import psutil
import datetime
from repositories.memory_repository import MemoryRepository

class MemoryUsage:
    def __init__(self, db_file, gui_var):
        self.repo = MemoryRepository(db_file)
        self.gui_var = gui_var
        self.memory_data = [] 

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
            return 0
        return sum(self.memory_data) / len(self.memory_data)

    def process_hourly_data(self):
        average_usage = self.calculate_average_memory_usage()
        timestamp = self.get_previous_hour_timestamp()
        self.repo.insert_memory_usage(timestamp, average_usage)
        self.memory_data = []

    def get_previous_hour_timestamp(self):
        previous_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
        return previous_hour.strftime("%Y-%m-%d %H:%M:%S")
    
    def check_hourly_reset(self):
        current_time = datetime.datetime.now()
        if current_time.minute == 0 and current_time.second == 0:
            self.process_hourly_data()