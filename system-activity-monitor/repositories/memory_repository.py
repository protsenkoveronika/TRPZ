import sqlite3

class MemoryRepository:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connect()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            print("Connected to database successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(f"Error closing the database: {e}")

    def insert_memory_usage(self, timestamp, memory_usage, total_memory):
        query = """
        INSERT INTO MemoryUsage (memusage_id, date_id, timestamp, memory_usage, total_memory)
        VALUES ((SELECT IFNULL(MAX(memusage_id), 0) + 1 FROM MemoryUsage), (SELECT date_id FROM MonitoringDates ORDER BY date_id DESC LIMIT 1), ?, ?, ?)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (timestamp, memory_usage, total_memory))
            self.connection.commit()
            print(f"Memory usage data saved: {memory_usage} MB at {timestamp}")
        except sqlite3.Error as e:
            print(f"Error saving memory usage data: {e}")

    def get_memory_usage_by_date(self, date_id):
        query = """
        SELECT timestamp, memory_usage, total_memory
        FROM MemoryUsage
        WHERE date_id = ?
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving memory usage data: {e}")
            return None
