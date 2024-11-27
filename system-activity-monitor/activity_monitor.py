import threading
import time
from tkinter import Tk, Label, StringVar
from processor_usage import ProcessorUsage
from memory_usage import MemoryUsage
from keyboard_monitor import KeyboardMonitor
from mouse_monitor import MouseMonitor
from window_monitor import WindowMonitor
from activity_monitor_iterator import MonitorIterator

class ActivityMonitor:
    def __init__(self, db_file):
        self.db_file = db_file
        self.current_index = 0
        self.is_monitoring = False
        self.data = {}

        self.root = Tk()
        self.root.title("Activity Monitor")


        self.gui_vars = {
            "cpu_usage": StringVar(value="CPU Usage: Loading..."),
            "memory_usage": StringVar(value="Memory Usage: Loading..."),
            "active_window": StringVar(value="Active Window: Loading..."),
        }

        self.monitors = [
            ProcessorUsage(db_file, self.gui_vars["cpu_usage"]),
            MemoryUsage(db_file, self.gui_vars["memory_usage"]),
            WindowMonitor(db_file, self.gui_vars["active_window"]),
            # KeyboardMonitor(),
            # MouseMonitor(),
        ]

        self.widgets = [
            Label(self.root, textvariable=self.gui_vars["cpu_usage"], font=("Arial", 14)),
            Label(self.root, textvariable=self.gui_vars["memory_usage"], font=("Arial", 14)),
            Label(self.root, textvariable=self.gui_vars["active_window"], font=("Arial", 14)),
        ]

        for widget in self.widgets:
            widget.pack(pady=5)

        self.start_monitoring()

    def start_monitoring(self):
        self.is_monitoring = True
        monitoring_thread = threading.Thread(target=self._monitoring_loop)
        monitoring_thread.daemon = True
        monitoring_thread.start()
        
    def __iter__(self):
        return MonitorIterator(self.monitors)

    def _monitoring_loop(self):
        while self.is_monitoring:
            for monitor in self.monitors:
                monitor.update_widget()

            time.sleep(1)

    def stop_monitoring(self):
        self.is_monitoring = False

    def start_gui(self):
        self.root.protocol("WM_DELETE_WINDOW", lambda: (self.stop_monitoring(), self.root.destroy()))
        self.root.mainloop()
