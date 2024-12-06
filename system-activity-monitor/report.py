import datetime
import json
from repositories.monitor_repository import MonitorRepository
from repositories.memory_repository import MemoryRepository
from repositories.processor_repository import ProcessorRepository
from repositories.window_repository import WindowRepository
from monitors.window_monitor import WindowMonitor

class Report:
    def __init__(self, db_file):
        # self.monitorrepo = MonitorRepository(db_file)
        self.memoryrepo = MemoryRepository(db_file)
        self.processorrepo = ProcessorRepository(db_file)
        self.windowrepo = WindowRepository(db_file)
        self.windowmonitor = WindowMonitor(db_file, None)

    def generate_daily_report(self, date, report_type):
        try:
            def is_current_date(date):
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                return date == today
            
            data = {}
                
            if report_type == 1: # cpu
                data['processor_usage'] = self.processorrepo.get_processor_usage_by_date(date)
            elif report_type == 2: # browser usage %
                if is_current_date(date):
                    window_usage = self.windowmonitor.get_window_usage()
                else: 
                    window_usage = self.windowrepo.get_window_usage_by_date(date)
                browser_names = ["Chrome", "Firefox", "Safari", "Edge", "Opera"]
                filtered_data = {name: usage for name, usage in window_usage.items() if any(browser in name for browser in browser_names)}
                data['browser_usage'] = filtered_data
            elif report_type == 3: # memory
                data['memory_usage'] = self.memoryrepo.get_memory_usage_by_date(date)
            # elif report_type == 4: # computer uptime
            elif report_type == 5: # programs used 
                if is_current_date(date):
                    data['window_usage'] = self.windowmonitor.get_window_usage()
                else: 
                    data['window_usage'] = self.windowrepo.get_window_usage_by_date(date)
            return data

        except Exception as e:
            print(f"Error generating daily report: {e}")
            return None
        

    def generate_periodic_report(self, start_date, end_date, report_type):
        try:
            data = []
            
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            delta = datetime.timedelta(days=1)
            
            current_date = start
            while current_date <= end:
                date_str = current_date.strftime("%Y-%m-%d")
                daily_data = self.generate_daily_report(date_str, report_type)
                if daily_data:
                    data.append({
                        "date": date_str,
                        "data": daily_data
                    })
                current_date += delta
            
        except Exception as e:
            print(f"Error generating periodic report: {e}")
            return None