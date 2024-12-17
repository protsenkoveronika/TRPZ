from collections import defaultdict
import datetime
from repositories.computer_usage_repository import ComputerUsageRepository
from repositories.memory_repository import MemoryRepository
from repositories.processor_repository import ProcessorRepository
from repositories.window_repository import WindowRepository

class Report:
    def __init__(self, db_file, processor_monitor, memory_monitor, window_monitor, computer_usage_monitor):
        self.computerusagerepo = ComputerUsageRepository(db_file)
        self.memoryrepo = MemoryRepository(db_file)
        self.processorrepo = ProcessorRepository(db_file)
        self.windowrepo = WindowRepository(db_file)
        self.processormonitor = processor_monitor
        self.memorymonitor = memory_monitor
        self.computerusagemonitor = computer_usage_monitor
        self.windowmonitor = window_monitor
    
    def aggregate_data(self, data):
        usage_by_time = defaultdict(list)

        for time, usage in data:
            usage_by_time[time].append(usage)
            
        aggregated_data = {
            time: sum(usages) for time, usages in usage_by_time.items()
        }

        return aggregated_data

    def generate_daily_report(self, date, report_type):
        try:
            def is_current_date(date):
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                return date == today
            
            data = {}
                
            if report_type == 1: # cpu
                if is_current_date(date):
                    self.processormonitor.save_data()
                data = self.processorrepo.get_processor_usage_by_date(date)

            elif report_type == 2: # % browser usage
                if is_current_date(date):
                    self.windowmonitor.save_data()
                    self.computerusagemonitor.save_data()
                data = self.windowrepo.get_window_usage_by_date(date)
                data = self.aggregate_data(data)
                browser_names = ["Google Chrome", "Firefox", "Safari", "Edge", "Opera"]
                filtered_data = {
                    name: usage 
                    for name, usage in data.items() 
                    if any(browser in name for browser in browser_names)
                }
                filtered_sum = sum(filtered_data.values())
                total_usage_data = self.computerusagerepo.get_computer_usage_by_date(date)
                total_usage_sum = sum(total_usage_data)
                if total_usage_sum > 0:
                    browser_percentage = (filtered_sum / total_usage_sum) * 100
                else:
                    browser_percentage = 0
                formatted_data = {'Total usage': total_usage_sum, 'Browser usage': filtered_sum, 'Percent of browser usage': round(browser_percentage,2)}
                return formatted_data
            
            elif report_type == 3: # memory
                if is_current_date(date):
                    self.memorymonitor.save_data()
                data = self.memoryrepo.get_memory_usage_by_date(date)

            elif report_type == 4: # computer uptime
                if is_current_date(date):
                    self.computerusagemonitor.save_data()
                data = self.computerusagerepo.get_computer_usage_by_date(date)
                data={'Total usage': sum(data)}
                return formatted_data
                
            elif report_type == 5: # programs usage
                if is_current_date(date):
                    self.windowmonitor.save_data()
                data = self.windowrepo.get_window_usage_by_date(date)
                
            formatted_data = self.aggregate_data(data)
            return formatted_data

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