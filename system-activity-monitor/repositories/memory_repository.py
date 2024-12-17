import sqlite3

class MemoryRepository:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connect()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            # print("Connected to database successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(f"Error closing the database: {e}")

    def insert_memory_usage(self, date_id, timestamp, memory_usage):
        query = """
        INSERT INTO MemoryUsage (memusage_id, date_id, timestamp, memory_usage)
        VALUES ((SELECT IFNULL(MAX(memusage_id), 0) + 1 FROM MemoryUsage), ?, ?, ?)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date_id, timestamp, memory_usage))
            self.connection.commit()
            print(f"Memory usage {memory_usage} MB for {timestamp} inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error saving memory usage data: {e}")

    def get_memory_usage_by_date(self, date):
        query = """
        SELECT MemoryUsage.timestamp, MemoryUsage.memory_usage
        FROM MemoryUsage
        JOIN MonitoringDates ON MemoryUsage.date_id = MonitoringDates.date_id
        WHERE MonitoringDates.date = ?
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving memory usage data: {e}")
            return None
        
    def delete_last_memory_usage(self):
        """Delete the most recent row from the ProcessorUsage table."""
        try:
            cursor = self.connection.cursor()
            # Delete the last entry based on the most recent timestamp
            cursor.execute("""
                DELETE FROM MemoryUsage
                WHERE memusage_id = (SELECT memusage_id FROM MemoryUsage ORDER BY memusage_id DESC LIMIT 1)
            """)
            self.connection.commit()
            print("Last processor usage deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting last processor usage: {e}")


# repo = MemoryRepository("db.sqlite")

# resp = repo.delete_last_memory_usage()

# repo.close()
# print(resp)
