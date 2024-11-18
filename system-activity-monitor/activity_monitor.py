import time
import datetime
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from report import Report
from keyboard_monitor import KeyboardMonitor
from mouse_monitor import MouseMonitor
from memory_usage import MemoryUsage
from processor_usage import ProcessorUsage
from window_monitor import WindowMonitor
from repositories.memory_repository import MemoryRepository
from repositories.processor_repository import ProcessorRepository
from repositories.window_repository import WindowRepository
from repositories.monitor_repository import MonitorRepository


class ActivityMonitor:
    def __init__(self, db_file):
        self.monitorrepo = MonitorRepository(db_file)
        self.windowrepo = WindowRepository(db_file)
        self.memoryrepo = MemoryRepository(db_file)
        self.processorrepo = ProcessorRepository(db_file)
        self.windowclass = WindowMonitor(db_file)
        self.memoryclass = MemoryUsage(db_file)
        self.processorclass = ProcessorUsage(db_file)
        self.mouseclass = MouseMonitor(db_file)
        self.keyboardclass = KeyboardMonitor(db_file)
        self.reportclass = Report(db_file)
        self.is_monitoring = False
        self.computer_usage_time = 0
        self.mouse_activity_flag = True
        self.keyboard_activity_flag = True
        self.cpu_usage = []
        self.memory_usage = []
        self.window_usage = {}
        self.current_key = ""
        self.current_position = (0, 0)

    def update_data(self, cpu_data, memory_data, window_usage, current_key, current_position):
        # Implement

    def generate_daily_report(self, date):
        # Implement

    def generate_multi_report(self, date_from, date_to):
        # Implement

    def display_report(self):
        # Implement

    def display_report(self, report_data):
        # Implement

    def display_historical_data(self, historical_data):
        # Implement

    def check_activity(self, historical_data):
        # Implement

    def count_activity_time(self):
        # Implement

    def save_activity_time(self):
        # Implement

    def check_midnight_reset(self):
        # Implement

    def start_monitoring(self):
        # Implement

    def stop_monitoring(self):
        # Implement

        