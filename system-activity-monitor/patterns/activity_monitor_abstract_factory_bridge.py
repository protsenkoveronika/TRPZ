from __future__ import annotations
from abc import ABC, abstractmethod
from monitors.processor_usage import ProcessorUsage
from monitors.memory_usage import MemoryUsage
from monitors.window_monitor import WindowMonitor
from monitors.mouse_monitor import MouseMonitor
from monitors.keyboard_monitor import KeyboardMonitor
from monitors.computer_usage_monitor import ComputerUsage



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

    @abstractmethod
    def create_computer_usage_monitor(self, db_file, gui_var) -> AbstractComputerUsageMonitor:
        pass


# Changed to use bridge
class ConcreteWindowsFactory(AbstractFactory):
    def create_processor_monitor(self, db_file, gui_var) -> SaveableMonitorAbstraction:
        implementation = ProcessorMonitorImplementation(db_file, gui_var)
        return SaveableMonitorAbstraction(implementation)
    
    def create_memory_monitor(self, db_file, gui_var) -> SaveableMonitorAbstraction:
        implementation = MemoryMonitorImplementation(db_file, gui_var)
        return SaveableMonitorAbstraction(implementation)
    
    def create_window_monitor(self, db_file, gui_var) -> SaveableMonitorAbstraction:
        implementation = WindowMonitorImplementation(db_file, gui_var)
        return SaveableMonitorAbstraction(implementation)
    
    def create_mouse_monitor(self, gui_var) -> ActivityFlagMonitorAbstraction:
        implementation = MouseMonitorImplementation(gui_var)
        return ActivityFlagMonitorAbstraction(implementation)
    
    def create_keyboard_monitor(self, gui_var) -> ActivityFlagMonitorAbstraction:
        implementation = KeyboardMonitorImplementation(gui_var)
        return ActivityFlagMonitorAbstraction(implementation)
    
    def create_computer_usage_monitor(self, db_file, gui_var) -> ExceptionalMonitorAbstraction:
        implementation = ComputerUsageMonitorImplementation(db_file, gui_var)
        return ExceptionalMonitorAbstraction(implementation)


class AbstractProcessorMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

    @abstractmethod
    def save_data(self):
        pass

class AbstractMemoryMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

    @abstractmethod
    def save_data(self):
        pass

class AbstractWindowMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

    @abstractmethod
    def save_data(self):
        pass

class AbstractMouseMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

    @abstractmethod
    def get_activity_flag(self) -> bool:
        pass

class AbstractKeyboardMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

    @abstractmethod
    def get_activity_flag(self) -> bool:
        pass

class AbstractComputerUsageMonitor(ABC):
    @abstractmethod
    def update_widget(self):
        pass

    @abstractmethod
    def save_data(self):
        pass

    @abstractmethod
    def check_activity(self, is_active: bool) -> bool:
        pass




# Bridge
class BaseMonitorAbstraction(ABC):
    def __init__(self, implementation: SaveableMonitorImplementation | ActivityFlagMonitorImplementation):
        self.implementation = implementation

    def update_widget(self) -> None:
        self.implementation.perform_update()

class SaveableMonitorAbstraction(BaseMonitorAbstraction):
    def save_data(self) -> None:
        self.implementation.save_data()

class ActivityFlagMonitorAbstraction(BaseMonitorAbstraction):
    def get_activity_flag(self) -> bool:
        return self.implementation.get_activity_flag()
    
class ExceptionalMonitorAbstraction(BaseMonitorAbstraction):
    def save_data(self) -> None:
        self.implementation.save_data()

    def check_activity(self, is_active: bool) -> bool:
        return self.implementation.check_activity(is_active)


class SaveableMonitorImplementation(ABC):
    @abstractmethod
    def perform_update(self) -> None:
        pass

    @abstractmethod
    def save_data(self) -> None:
        pass

class ActivityFlagMonitorImplementation(ABC):
    @abstractmethod
    def perform_update(self) -> None:
        pass

    @abstractmethod
    def get_activity_flag(self) -> bool:
        pass

class ExceptionalMonitorImplementation(ABC):
    @abstractmethod
    def perform_update(self) -> None:
        pass

    @abstractmethod
    def save_data(self) -> None:
        pass

    @abstractmethod
    def check_activity(self) -> None:
        pass
    
    
class ProcessorMonitorImplementation(SaveableMonitorImplementation):
    def __init__(self, db_file, gui_var):
        self.processor_usage = ProcessorUsage(db_file, gui_var)

    def perform_update(self) -> None:
        self.processor_usage.update_widget()

    def save_data(self) -> None:
        self.processor_usage.save_data()

class MemoryMonitorImplementation(SaveableMonitorImplementation):
    def __init__(self, db_file, gui_var):
        self.memory_usage = MemoryUsage(db_file, gui_var)

    def perform_update(self) -> None:
        self.memory_usage.update_widget()

    def save_data(self) -> None:
        self.memory_usage.save_data()

class WindowMonitorImplementation(SaveableMonitorImplementation):
    def __init__(self, db_file, gui_var):
        self.window_monitor = WindowMonitor(db_file, gui_var)

    def perform_update(self) -> None:
        self.window_monitor.update_widget()

    def save_data(self) -> None:
        self.window_monitor.save_data()
        
class MouseMonitorImplementation(ActivityFlagMonitorImplementation):
    def __init__(self, gui_var):
        self.mouse_monitor = MouseMonitor(gui_var)

    def perform_update(self) -> None:
        self.mouse_monitor.update_widget()

    def get_activity_flag(self) -> bool:
        return self.mouse_monitor.activity_flag

class KeyboardMonitorImplementation(ActivityFlagMonitorImplementation):
    def __init__(self, gui_var):
        self.keyboard_monitor = KeyboardMonitor(gui_var)

    def perform_update(self) -> None:
        self.keyboard_monitor.update_widget()

    def get_activity_flag(self) -> bool:
        return self.keyboard_monitor.activity_flag
    
class ComputerUsageMonitorImplementation(ExceptionalMonitorImplementation):
    def __init__(self, db_file, gui_var):
        self.computer_usage_monitor = ComputerUsage(db_file, gui_var)

    def perform_update(self) -> None:
        self.computer_usage_monitor.update_widget()

    def save_data(self) -> None:
        self.computer_usage_monitor.save_data()

    def check_activity(self, is_active: bool) -> bool:
        return self.computer_usage_monitor.check_activity(is_active)