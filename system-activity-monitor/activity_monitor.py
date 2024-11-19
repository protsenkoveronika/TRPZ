import threading
import time
from tkinter import Tk, Label, StringVar
from processor_usage import ProcessorUsage
from memory_usage import MemoryUsage
from keyboard_monitor import KeyboardMonitor
from mouse_monitor import MouseMonitor
from window_monitor import WindowMonitor
from activity_monitor_iterator import MonitorIterator, WidgetIterator

class ActivityMonitor:
    def __init__(self, db_file):
        self.db_file = db_file
        self.monitors = [
            ProcessorUsage(db_file),
            MemoryUsage(db_file),
            WindowMonitor(db_file),
            # KeyboardMonitor(),
            # MouseMonitor(),
        ]
        self.current_index = 0
        self.is_monitoring = False
        self.data = {}

        # створення Tkinter root
        self.root = Tk()
        self.root.title("Activity Monitor")

        # GUI змінні для відображення
        self.gui_vars = {
            "cpu_usage": StringVar(value="CPU Usage: Loading..."),
            "memory_usage": StringVar(value="Memory Usage: Loading..."),
            "active_window": StringVar(value="Active Window: Loading..."),
        }

        # віджети для відображення
        self.widgets = [
            Label(self.root, textvariable=self.gui_vars["cpu_usage"], font=("Arial", 14)),
            Label(self.root, textvariable=self.gui_vars["memory_usage"], font=("Arial", 14)),
            Label(self.root, textvariable=self.gui_vars["active_window"], font=("Arial", 14)),
        ]

        for widget in self.widgets:
            widget.pack(pady=5)

        # Ініціалізація ітератора для віджетів
        self.widget_iterator = WidgetIterator(self.widgets)

        # автоматичний запуск моніторингу
        self.start_monitoring()


    def __iter__(self):
        return MonitorIterator(self.monitors)

    def start_monitoring(self):
        self.is_monitoring = True
        monitoring_thread = threading.Thread(target=self._monitoring_loop)
        monitoring_thread.daemon = True
        monitoring_thread.start()

    def _monitoring_loop(self):
        while self.is_monitoring:
            for monitor in self:
                data = monitor.collect_data()
                self.data[monitor.__class__.__name__] = data

            # оновлення GUI змінних
            for widget in self.widget_iterator:
                if widget == self.widgets[0]: 
                    self.gui_vars["cpu_usage"].set(
                        f"CPU Usage: {self.data.get('ProcessorUsage', {}).get('cpu_usage', 'N/A')}%"
                    )
                elif widget == self.widgets[1]:
                    self.gui_vars["memory_usage"].set(
                        f"Memory Usage: {self.data.get('MemoryUsage', {}).get('memory_usage', 'N/A')} MB"
                    )
                elif widget == self.widgets[2]:
                    self.gui_vars["active_window"].set(
                        f"Active Window: {self.data.get('WindowMonitor', {}).get('active_window', 'N/A')}"
                    )
                    
            time.sleep(1)

    def stop_monitoring(self):
        self.is_monitoring = False

    def start_gui(self):
        self.root.protocol("WM_DELETE_WINDOW", lambda: (self.stop_monitoring(), self.root.destroy()))
        self.root.mainloop()
