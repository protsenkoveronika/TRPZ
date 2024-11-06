import datetime
import json
from repositories.monitor_repository import MonitorRepository
from repositories.memory_repository import MemoryRepository
from repositories.processor_repository import ProcessorRepository
from repositories.window_repository import WindowRepository

class Report:
    def __init__(self, db_file):
        self.monitorrepo = MonitorRepository(db_file)
        self.memoryrepo = MemoryRepository(db_file)
        self.processorrepo = ProcessorRepository(db_file)
        self.windowrepo = WindowRepository(db_file)

    def get_daily_report(self, date):
        date_id = self.monitorrepo.get_current_date_id()
        if date_id is None:
            print("Date not found.")
            return

        total_usage_time = self.monitorrepo.get_computer_usage_by_date(date_id)
        window_usage = self.windowrepo.get_window_usage_by_date(date_id)

        all_memory = self.memoryrepo.get_memory_usage_by_date(date_id)
        if not all_memory:
            print("No memory usage data found.")
            memory_data_list = []
            average_memory_usage = 0
        else:
            memory_data_list = []
            for record in all_memory:
                timestamp, memory_usage, total_memory = record
                memory_data_list.append({
                    "timestamp": timestamp,
                    "memory_usage": memory_usage,
                    "total_memory": total_memory
                })
        memory_data_json = json.dumps(memory_data_list, indent=4)
        total_memory_usage = 0
        memory_record_count = 0
        for memory_data in memory_data_list:
            total_memory_usage += memory_data['memory_usage']
            memory_record_count += 1
        if memory_record_count == 0:
            print("No records found to calculate the average memory.")
            average_memory_usage = 0
        else:
            average_memory_usage = total_memory_usage / memory_record_count
        
        all_cpu = self.processorrepo.get_processor_usage_by_date(date_id)
        if not all_cpu:
            print("No cpu usage data found.")
            cpu_data_list = []
            average_cpu_usage = 0
        else:
            cpu_data_list = []
            for record in all_cpu:
                timestamp, cpu_usage, = record
                cpu_data_list.append({
                    "timestamp": timestamp,
                    "cpu_usage": cpu_usage,
                })
        cpu_data_json = json.dumps(cpu_data_list, indent=4)
        total_cpu_usage = 0
        cpu_record_count = 0
        for cpu_data in cpu_data_list:
            total_cpu_usage += cpu_data['cpu_usage']
            cpu_record_count += 1
        if cpu_record_count == 0:
            print("No records found to calculate the average memory.")
            average_cpu_usage = 0
        else:
            average_cpu_usage = total_cpu_usage / cpu_record_count
        
        report = {
            "date": date,
            "total_usage_time": sum(total_usage_time),
            "window_usage": window_usage,
            "memory_json": memory_data_json,
            "average_memory": average_memory_usage,
            "cpu_json": cpu_data_json,
            "average_cpu": average_cpu_usage
        }
        return report

    def get_multi_day_report(self, date_from, date_to):
        date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d")
        date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d")
        current_date = date_from

        daily_reports = []
        total_usage_time = 0
        total_days = 0

        while current_date <= date_to:
            date_str = current_date.strftime("%Y-%m-%d")
            daily_report = self.get_daily_report(date_str)

            if daily_report:
                daily_reports.append(daily_report)
                total_usage_time += daily_report["total_usage_time"]
                total_days += 1

            current_date += datetime.timedelta(days=1)

        average_usage_time = total_usage_time / total_days if total_days > 0 else 0
        
        average_memory = self.memoryrepo.get_average_memory_over_period(date_from, date_to)  
        # Implement this
        average_cpu = self.processorrepo.get_average_cpu_over_period(date_from, date_to)  
        # Implement this

        summary_report = {
            "daily_reports": daily_reports,
            "average_usage_time": average_usage_time,
            "average_memory": average_memory,
            "average_cpu": average_cpu
        }
        return summary_report
