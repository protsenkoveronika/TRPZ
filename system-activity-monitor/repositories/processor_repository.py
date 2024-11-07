import sqlite3

class ProcessorRepository:
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

    def insert_processor_usage(self, timestamp, cpu_usage):
        query = """
        INSERT INTO ProcessorUsage (procusage_id, date_id, timestamp, cpu_usage)
        VALUES ((SELECT IFNULL(MAX(procusage_id), 0) + 1 FROM ProcessorUsage), (SELECT date_id FROM MonitoringDates ORDER BY date_id DESC LIMIT 1), ?, ?)   
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (timestamp, cpu_usage))
            self.connection.commit()
            print(f"CPU usage for {timestamp} inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting CPU usage: {e}")

    def get_processor_usage_by_date(self, date_id):
        query = """
        SELECT timestamp, cpu_usage
        FROM ProcessorUsage
        WHERE date_id = ?
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving memory usage data: {e}")
            return None
