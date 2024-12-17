import sqlite3

class ComputerUsageRepository:
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
        
    def insert_computer_usage(self, date_id, time):
        query = """
        INSERT INTO ComputerUsage (compusage_id, date_id, time)
        VALUES ((SELECT IFNULL(MAX(compusage_id), 0) + 1 FROM ComputerUsage), ?, ?)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date_id, time))
            self.connection.commit()
            print(f"Computer usage data saved: {time} seconds for date_id {date_id}.")
        except sqlite3.Error as e:
            print(f"Error saving computer usage data: {e}")

    def get_computer_usage_by_date(self, date):
        query = """
        SELECT ComputerUsage.time FROM ComputerUsage
        JOIN MonitoringDates ON ComputerUsage.date_id = MonitoringDates.date_id
        WHERE MonitoringDates.date = ?
        """
        "SELECT time FROM ComputerUsage WHERE date_id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date,))
            results = cursor.fetchall()
            # print(f"Fetched computer usage data for date {date}: {results}")
            return [row[0] for row in results]
        except sqlite3.Error as e:
            print(f"Error fetching computer usage by date: {e}")
            return []

# repo = ComputerUsageRepository("db.sqlite")

# resp = repo.get_computer_usage_by_date('2024-12-13')

# repo.close()
# print(resp)