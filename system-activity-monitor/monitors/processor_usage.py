import psutil
import datetime
from repositories.processor_repository import ProcessorRepository

class ProcessorUsage:
    def __init__(self, db_file, gui_var):
        self.repo = ProcessorRepository(db_file)
        self.gui_var = gui_var
        self.cpu_data = []

    def collect_data(self):
        usage = psutil.cpu_percent(interval=1)
        self.cpu_data.append(usage)
        self.check_hourly_reset()
        return {"cpu_usage": usage}
    
    def update_widget(self):
        data = self.collect_data()
        self.gui_var.set(f"CPU Usage: {data['cpu_usage']}%")

    def save_data(self):
        pass

    def calculate_average_cpu_usage(self):
        if not self.cpu_data:
            return 0
        return sum(self.cpu_data) / len(self.cpu_data)

    def process_hourly_data(self):
        average_usage = self.calculate_average_cpu_usage()
        timestamp = self.get_previous_hour_timestamp()
        self.repo.insert_processor_usage(timestamp, average_usage)
        self.cpu_data = []

    def get_previous_hour_timestamp(self):
        previous_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
        return previous_hour.strftime("%Y-%m-%d %H:%M:%S")

    def check_hourly_reset(self):
        current_time = datetime.datetime.now()
        if current_time.minute == 0 and current_time.second == 0:
            self.process_hourly_data()
