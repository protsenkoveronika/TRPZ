from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class GenerateDailyReportCommand(Command):
    def __init__(self, report, date, report_type):
        self.report = report
        self.date = date
        self.report_type = report_type

    def execute(self):
        return self.report.generate_daily_report(self.date, self.report_type)


class GeneratePeriodicReportCommand(Command):
    def __init__(self, report, start_date, end_date, report_type):
        self.report = report
        self.start_date = start_date
        self.end_date = end_date
        self.report_type = report_type

    def execute(self):
        return self.report.generate_periodic_report(self.start_date, self.end_date, self.report_type)


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