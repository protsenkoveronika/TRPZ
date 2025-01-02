from abc import ABC, abstractmethod
import json

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# Changed to use Visitor
class GenerateDailyReportCommand(Command):
    def __init__(self, report, date, report_type, visitor):
        self.report = report
        self.date = date
        self.report_type = report_type
        self.visitor = visitor

    def execute(self):
        return self.visitor.visit_daily_report(self.report, self.date, self.report_type)

class GeneratePeriodicReportCommand(Command):
    def __init__(self, report, start_date, end_date, report_type, visitor):
        self.report = report
        self.start_date = start_date
        self.end_date = end_date
        self.report_type = report_type
        self.visitor = visitor

    def execute(self):
        return self.visitor.visit_periodic_report(self.report, self.start_date, self.end_date, self.report_type)


class ReportInvoker:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def execute_command(self):
        if self.command:
            return self.command.execute()
        else:
            print("No command set.")
            return None
        

# Visitor
class ReportVisitor(ABC):
    @abstractmethod
    def visit_daily_report(self, report, date, report_type):
        pass

    @abstractmethod
    def visit_periodic_report(self, report, start_date, end_date, report_type):
        pass


class JSONReportVisitor(ReportVisitor):
    def visit_daily_report(self, report, date, report_type):
        data = report.generate_daily_report(date, report_type)
        if not data:
            return None
        return json.dumps({"date": date, "data": data}, indent=4)

    def visit_periodic_report(self, report, start_date, end_date, report_type):
        data = report.generate_periodic_report(start_date, end_date, report_type)
        if not data:
            return None
        return json.dumps({"start_date": start_date, "end_date": end_date, "data": data}, indent=4)
    
class TextReportVisitor(ReportVisitor):
    def visit_daily_report(self, report, date, report_type):
        data = report.generate_daily_report(date, report_type)
        if not data:
            return None
        return f"Daily Report ({date}):\n{self.format_data(data)}"

    def visit_periodic_report(self, report, start_date, end_date, report_type):
        data = report.generate_periodic_report(start_date, end_date, report_type)
        if not data:
            return None
        return f"Periodic Report ({start_date} - {end_date}):\n{self.format_periodic_data(data)}"

    def format_data(self, data):
        return "\n".join(f"{key}: {value}" for key, value in data.items()) if data else "No data available."
    
    def format_periodic_data(self, data):
        if not data:
            return "No data available."
        
        formatted = []
        for date, daily_data in data.items():
            formatted.append(f"{date}:")
            for key, value in daily_data.items():
                formatted.append(f"  {key}: {value}")
        return "\n".join(formatted)
