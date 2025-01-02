import sqlite3

class ProcessorRepository:
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

    def insert_processor_usage(self, date_id, timestamp, cpu_usage):
        query = """
        INSERT INTO ProcessorUsage (procusage_id, date_id, timestamp, cpu_usage)
        VALUES ((SELECT IFNULL(MAX(procusage_id), 0) + 1 FROM ProcessorUsage), ?, ?, ?)   
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date_id, timestamp, cpu_usage))
            self.connection.commit()
            print(f"CPU usage {cpu_usage} for {timestamp} inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting CPU usage: {e}")


    def get_processor_usage_by_date(self, date):
        query = """
        SELECT ProcessorUsage.timestamp, ProcessorUsage.cpu_usage
        FROM ProcessorUsage
        JOIN MonitoringDates ON ProcessorUsage.date_id = MonitoringDates.date_id
        WHERE MonitoringDates.date = ?
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving processor usage data: {e}")
            return None
        
    # def delete_last_processor_usage(self):
    #     try:
    #         cursor = self.connection.cursor()
    #         # Delete the last entry based on the most recent timestamp
    #         cursor.execute("""
    #             DELETE FROM ComputerUsage
    #             WHERE compusage_id = 1
    #         """)
    #         self.connection.commit()
    #         print("Last processor usage deleted successfully.")
    #     except sqlite3.Error as e:
    #         print(f"Error deleting last processor usage: {e}")


# repo = ProcessorRepository("db.sqlite")

# resp = repo.delete_last_processor_usage()

# repo.close()
# print(resp)