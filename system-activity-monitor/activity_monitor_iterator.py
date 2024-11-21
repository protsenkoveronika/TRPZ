class MonitorIterator:
    def __init__(self, monitors):
        self.monitors = monitors
        self.current_index = 0

    def __iter__(self):
        self.current_index = 0
        return self

    def get_next(self):
        if not self.has_more():
            raise StopIteration
        monitor = self.monitors[self.current_index]
        self.current_index += 1
        return monitor

    def has_more(self):
        return self.current_index < len(self.monitors)