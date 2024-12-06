from __future__ import annotations
from abc import ABC, abstractmethod
from monitors.processor_usage import ProcessorUsage
from monitors.memory_usage import MemoryUsage
from monitors.window_monitor import WindowMonitor
from monitors.mouse_monitor import MouseMonitor
from monitors.keyboard_monitor import KeyboardMonitor

class AbstractFactory(ABC):
    @abstractmethod
    def create_processor_monitor(self, db_file, gui_var) -> AbstractProcessorMonitor:
        pass

    @abstractmethod
    def create_memory_monitor(self, db_file, gui_var) -> AbstractMemoryMonitor:
        pass

    @abstractmethod
    def create_window_monitor(self, db_file, gui_var) -> AbstractWindowMonitor:
        pass

    @abstractmethod
    def create_mouse_monitor(self, gui_var) -> AbstractMouseMonitor:
        pass

    @abstractmethod
    def create_keyboard_monitor(self, gui_var) -> AbstractKeyboardMonitor:
        pass


class ConcreteWindowsFactory(AbstractFactory):
    def create_processor_monitor(self, db_file, gui_var) -> AbstractProcessorMonitor:
        return ProcessorUsage(db_file, gui_var)

    def create_memory_monitor(self, db_file, gui_var) -> AbstractMemoryMonitor:
        return MemoryUsage(db_file, gui_var)
    
    def create_window_monitor(self, db_file, gui_var) -> AbstractWindowMonitor:
        return WindowMonitor(db_file, gui_var)

    def create_mouse_monitor(self, gui_var) -> AbstractMouseMonitor:
        return MouseMonitor(gui_var)
    
    def create_keyboard_monitor(self, gui_var) -> AbstractKeyboardMonitor:
        return KeyboardMonitor(gui_var)


class AbstractProcessorMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

class AbstractMemoryMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

class AbstractWindowMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

class AbstractMouseMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

class AbstractKeyboardMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass
