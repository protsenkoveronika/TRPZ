class MonitorIterator:
    def __init__(self, monitors):
        self.monitors = monitors
        self.current_index = 0

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index >= len(self.monitors):
            raise StopIteration
        monitor = self.monitors[self.current_index]
        self.current_index += 1
        return monitor
    
class WidgetIterator:
    def __init__(self, widgets):
        self.widgets = widgets
        self.current_index = 0

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index >= len(self.widgets):
            raise StopIteration
        widget = self.widgets[self.current_index]
        self.current_index += 1
        return widget