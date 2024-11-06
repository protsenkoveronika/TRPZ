import psutil
import time
import datetime
from repositories.memory_repository import MemoryRepository
from repositories.monitor_repository import MonitorRepository


class MemoryUsage:
    def __init__(self, db_file):
        self.repo = MemoryRepository(db_file)
        self.monitorrepo = MonitorRepository(db_file)
        self.memory_data = []
        self.total_memory = self.get_total_memory()

    def get_current_memory_usage(self):
        memory_info = psutil.virtual_memory()
        return int(memory_info.used / (1024 ** 2))  # Return in MB

    def get_total_memory(self):
        memory_info = psutil.virtual_memory()
        return int(memory_info.total / (1024 ** 2))  # Return in MB
    
    def save_memory_usage(self, average_used_memory):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if not self.monitorrepo.current_date_exists(current_date):
            self.monitorrepo.insert_current_date()

        timestamp = self.get_previous_hour_timestamp()

        self.repo.insert_memory_usage(timestamp, average_used_memory, self.total_memory)

    def get_previous_hour_timestamp(self):
        previous_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
        return previous_hour.strftime("%H:%M:%S")

    def calculate_average_memory_usage(self):
        if not self.memory_data:
            return 0  # Avoid division by zero
        return sum(self.memory_data) / len(self.memory_data)

    def first_check_and_monitoring(self):
        current_time = datetime.datetime.now()
        if current_time.minute == 0 and current_time.second == 0:
            print("Start of an hour detected. Beginning regular monitoring.")
            self.start_monitoring_loop()
        else:
            next_hour = (current_time + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            time_to_next_hour = (next_hour - current_time).total_seconds()
            print(f"Waiting for the next full hour in {time_to_next_hour // 60} minutes.")
            self.collect_until_next_hour(time_to_next_hour)

    def collect_until_next_hour(self, time_to_next_hour):
        start_time = time.time()
        while time.time() - start_time < time_to_next_hour:
            used_memory = self.get_current_memory_usage()
            print(used_memory)
            self.memory_data.append(used_memory)
            time.sleep(1)

        average_used = self.calculate_average_memory_usage()
        self.save_memory_usage(average_used)
        self.memory_data = []
        self.start_monitoring_loop()

    def start_monitoring_loop(self):
        while True:
            start_time = time.time()
            for _ in range(3600):
                used_memory = self.get_current_memory_usage()
                print(used_memory)
                self.memory_data.append(used_memory)
                time.sleep(1)

            average_used = self.calculate_average_memory_usage()
            self.save_memory_usage(average_used)
            self.memory_data = []
