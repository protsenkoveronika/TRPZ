import json
import threading
import time
import datetime
from tkinter import Tk, Text, Scrollbar, Label, StringVar, Button, Toplevel, Entry, Frame, Radiobutton, IntVar
from patterns.activity_monitor_iterator import MonitorIterator
from patterns.activity_monitor_abstract_factory_bridge import ConcreteWindowsFactory
from patterns.activity_monitor_command_visitor import GenerateDailyReportCommand, GeneratePeriodicReportCommand, ReportInvoker, JSONReportVisitor, TextReportVisitor
from report import Report

class ActivityMonitor:
    def __init__(self, db_file):
        self.db_file = db_file
        self.current_index = 0
        self.is_monitoring = False
        self.factory = ConcreteWindowsFactory()

        self.root = Tk()
        self.root.title("Activity Monitor")
        self.root.minsize(600, 340)

        self.gui_vars = {
            "cpu_usage": StringVar(value="CPU Usage: Loading..."),
            "memory_usage": StringVar(value="Memory Usage: Loading..."),
            "active_window": StringVar(value="Active Window: Loading..."),
            "mouse_position": StringVar(value="Mouse Activity: Loading..."),
            "keyboard_activity": StringVar(value="Keyboard Activity: Loading..."),
            "computer_usage": StringVar(value="Computer Usage Time: Loading..."),
        }

        self.setup_monitors()
        self.setup_main_window()   
        self.start_monitoring()
        
    def setup_monitors(self):
        self.saveable_monitors = [
            self.factory.create_processor_monitor(self.db_file, self.gui_vars["cpu_usage"]),
            self.factory.create_memory_monitor(self.db_file, self.gui_vars["memory_usage"]),
            self.factory.create_window_monitor(self.db_file, self.gui_vars["active_window"]),
        ]

        self.flag_monitors = [
            self.factory.create_mouse_monitor(self.gui_vars["mouse_position"]),
            self.factory.create_keyboard_monitor(self.gui_vars["keyboard_activity"]),
        ]

        self.exceptional_monitors = [
            self.factory.create_computer_usage_monitor(self.db_file, self.gui_vars["computer_usage"]),
        ]

        self.report = Report(
            self.db_file,
            processor_monitor=self.saveable_monitors[0],
            memory_monitor=self.saveable_monitors[1],
            window_monitor=self.saveable_monitors[2],
            computer_usage_monitor=self.exceptional_monitors[0]
        )

    def setup_main_window(self):
        header = Label(self.root, text="Activity Monitor", font=("Arial", 18, "bold"))
        header.pack(pady=10, padx=20)

        self.widgets = [
            Label(self.root, textvariable=self.gui_vars["cpu_usage"], font=("Arial", 14)),
            Label(self.root, textvariable=self.gui_vars["memory_usage"], font=("Arial", 14)),
            Label(self.root, textvariable=self.gui_vars["active_window"], font=("Arial", 14)),
            Label(self.root, textvariable=self.gui_vars["mouse_position"], font=("Arial", 14)),
            Label(self.root, textvariable=self.gui_vars["keyboard_activity"], font=("Arial", 14)),
            Label(self.root, textvariable=self.gui_vars["computer_usage"], font=("Arial", 14)),
        ]

        for widget in self.widgets:
            widget.pack(pady=5, padx=20, anchor="w")

        self.create_buttons()

    def create_buttons(self):
        button_frame = Frame(self.root)
        button_frame.pack(side="bottom", fill="x", pady=10)

        Button(
            button_frame,
            text="Generate Report",
            command=self.open_report_window
        ).pack(padx=10)

    def start_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            print(f"Monitoring started (is_monitoring: {self.is_monitoring})")
            monitoring_thread = threading.Thread(target=self._monitoring_loop)
            monitoring_thread.daemon = True
            monitoring_thread.start()
        else:
            print("Monitoring already started.")

    def __iter__(self):
        return MonitorIterator(self.monitors)

    def _monitoring_loop(self):
        while self.is_monitoring:
            for monitor in self.saveable_monitors + self.exceptional_monitors + self.flag_monitors:
                monitor.update_widget()

            self.check_activity()
            # time.sleep(1)
        pass

    def check_activity(self):
        is_active = any(monitor.get_activity_flag() for monitor in self.flag_monitors)
        for monitor in self.exceptional_monitors:
            monitor.check_activity(is_active)

    def stop_monitoring(self):
        print("Saving data...")
        for monitor in self.saveable_monitors + self.exceptional_monitors:
            monitor.save_data()
        self.is_monitoring = False

    def start_gui(self):
        self.root.protocol("WM_DELETE_WINDOW", lambda: (self.stop_monitoring(), self.root.destroy()))
        self.root.mainloop()

    def handle_report_submission(self, selection, day, start_date, end_date, report_type, format_type, window):
        report_generator = self.report
        invoker = ReportInvoker()
        
        visitor = None
        if format_type == "Text":
            visitor = TextReportVisitor()
        elif format_type == "JSON":
            visitor = JSONReportVisitor()
        
        try:
            if report_type == 0:
                print("Please select a report type.")
                return

            if selection == 1:
                if not day or not self.is_valid_date(day):
                    print("Valid date (YYYY-MM-DD) is required.")
                    return

                entered_date = datetime.datetime.strptime(day, "%Y-%m-%d")
                if entered_date > datetime.datetime.now():
                    print("The entered date is in the future.")
                    return

                print(f"Fetching daily statistics for {day}, Report Type: {report_type}")
                command = GenerateDailyReportCommand(report_generator, day, report_type, visitor)

            elif selection == 2:
                if not start_date or not end_date or not self.is_valid_date(start_date) or not self.is_valid_date(end_date):
                    print("Valid start and end dates (YYYY-MM-DD) are required.")
                    return

                start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

                if start_date_obj > end_date_obj:
                    print("Start date cannot be later than end date.")
                    return

                if end_date_obj > datetime.datetime.now():
                    print("The entered dates include future dates.")
                    return

                print(f"Fetching periodic statistics from {start_date} to {end_date}, Report Type: {report_type}")
                command = GeneratePeriodicReportCommand(report_generator, start_date, end_date, report_type, visitor)

            else:
                print("Invalid selection type.")
                return
            
            invoker.set_command(command)
            result = invoker.execute_command()

            if result:
                window.destroy()
                self.display_report(result)
            else:
                self.display_report("No data available for the selected report.")

        except Exception as e:
            print(f"Error: {e}")
                
    def is_valid_date(self, date_string):
        try:
            datetime.datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def display_report(self, report_data):
        results_window = Toplevel(self.root)
        results_window.title("Report")

        results_window.minsize(400, 100)

        Label(results_window, text="Report Results:", font=("Arial", 14, "bold")).pack(pady=10)

        if isinstance(report_data, str):
            Label(results_window, text=report_data, font=("Arial", 12), justify="left").pack(pady=10)
        else:
            text_frame = Frame(results_window)
            text_frame.pack(padx=10, pady=10, fill="both", expand=True)

            text_widget = Text(text_frame, wrap="word", font=("Arial", 12))
            text_widget.pack(side="left", fill="both", expand=True)

            scrollbar = Scrollbar(text_frame, command=text_widget.yview)
            scrollbar.pack(side="right", fill="y")
            text_widget.config(yscrollcommand=scrollbar.set)

            report_text = json.dumps(report_data, indent=4)
            text_widget.insert("1.0", report_text)
            text_widget.configure(state="disabled")

        Button(results_window, text="Close", command=results_window.destroy).pack(pady=10)

    def open_report_window(self):
        window = Toplevel(self.root)
        window.title("Generate Report")

        main_frame = Frame(window)
        main_frame.pack(padx=10, pady=10)

        selection_var = IntVar(value=1)
        report_type_var = IntVar()
        format_var = StringVar(value="Text")

        Label(main_frame, text="Choose daily or periodic report:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        input_frame = Frame(main_frame)
        report_type_frame = Frame(main_frame)

        # By Day
        day_frame = Frame(input_frame)
        Label(day_frame, text="Enter Date (YYYY-MM-DD):").pack(side="left", padx=5)
        day_entry = Entry(day_frame)
        day_entry.pack(side="left")

        # By Period
        period_frame = Frame(input_frame)
        Label(period_frame, text="Start Date (YYYY-MM-DD):").pack(side="left", padx=5)
        start_date_entry = Entry(period_frame)
        start_date_entry.pack(side="left")
        Label(period_frame, text="End Date (YYYY-MM-DD):").pack(side="left", padx=5)
        end_date_entry = Entry(period_frame)
        end_date_entry.pack(side="left")

        def show_day_report_types():
            for widget in report_type_frame.winfo_children():
                widget.destroy()

            Label(report_type_frame, text="Choose Type of Report:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

            Radiobutton(report_type_frame, text="CPU Usage by Hours", variable=report_type_var, value=1).pack(anchor="w", padx=10)
            Radiobutton(report_type_frame, text="Browser Usage Percentage", variable=report_type_var, value=2).pack(anchor="w", padx=10)
            Radiobutton(report_type_frame, text="Memory Usage by Hours", variable=report_type_var, value=3).pack(anchor="w", padx=10)
            Radiobutton(report_type_frame, text="Computer Uptime by Day", variable=report_type_var, value=4).pack(anchor="w", padx=10)
            Radiobutton(report_type_frame, text="Programs Used by Day", variable=report_type_var, value=5).pack(anchor="w", padx=10)

        def show_period_report_types():
            for widget in report_type_frame.winfo_children():
                widget.destroy()

            Label(report_type_frame, text="Choose Type of Report:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

            Radiobutton(report_type_frame, text="Average CPU Usage by Days", variable=report_type_var, value=6).pack(anchor="w", padx=10)
            Radiobutton(report_type_frame, text="Browser Usage Percentage by Days", variable=report_type_var, value=7).pack(anchor="w", padx=10)
            Radiobutton(report_type_frame, text="Average Memory Usage by Days", variable=report_type_var, value=8).pack(anchor="w", padx=10)
            Radiobutton(report_type_frame, text="Computer Uptime by Days", variable=report_type_var, value=9).pack(anchor="w", padx=10)
            Radiobutton(report_type_frame, text="Top 5 Programs Used by Days", variable=report_type_var, value=10).pack(anchor="w", padx=10)

        def update_input_fields():
            day_frame.pack_forget()
            period_frame.pack_forget()
            if selection_var.get() == 1:
                day_frame.pack(pady=5)
                show_day_report_types()
            else:
                period_frame.pack(pady=5)
                show_period_report_types()

        # початковий стан
        day_frame.pack(pady=5)
        show_day_report_types()

        Radiobutton(main_frame, text="By Day", variable=selection_var, value=1, command=update_input_fields).pack(anchor="w", pady=5)
        Radiobutton(main_frame, text="By Period", variable=selection_var, value=2, command=update_input_fields).pack(anchor="w", pady=5)

        input_frame.pack(fill="x", pady=10)
        report_type_frame.pack(fill="x", pady=10)

        # Visitor Selection
        Label(main_frame, text="Choose Report Format:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        Radiobutton(main_frame, text="Text Report", variable=format_var, value="Text").pack(anchor="w", padx=10)
        Radiobutton(main_frame, text="JSON Report", variable=format_var, value="JSON").pack(anchor="w", padx=10)

        submit_button = Button(
            main_frame,
            text="Submit",
            command=lambda: self.handle_report_submission(
                selection_var.get(),
                day_entry.get(),
                start_date_entry.get(),
                end_date_entry.get(),
                report_type_var.get(),
                format_var.get(),
                window
            )
        )
        submit_button.pack(pady=10)