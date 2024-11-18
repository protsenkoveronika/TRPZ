import sqlite3
import datetime

class MonitorRepository:
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
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def current_date_exists(self, current_date):
        query = "SELECT 1 FROM MonitoringDates WHERE date = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (current_date,))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Error checking for current date: {e}")
            return False

    def insert_current_date(self):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        if not self.current_date_exists(current_date):
            query = """
            INSERT INTO MonitoringDates (date_id, date)
            VALUES ((SELECT IFNULL(MAX(date_id), 0) + 1 FROM MonitoringDates), ?)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, (current_date,))
                self.connection.commit()
                print(f"Current date {current_date} inserted successfully.")
            except sqlite3.Error as e:
                print(f"Error inserting current date: {e}")
        else:
            print(f"Date {current_date} already exists in the database.")

    def get_current_date_id(self):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        query = "SELECT date_id FROM MonitoringDates WHERE date = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (current_date))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error fetching current date_id: {e}")
            return None
        
    def insert_computer_usage(self, time):
        query = """
        INSERT INTO ComputerUsage (compusage_id, date_id, time)
        VALUES ((SELECT IFNULL(MAX(compusage_id), 0) + 1 FROM ComputerUsage), (SELECT date_id FROM MonitoringDates ORDER BY date_id DESC LIMIT 1), ?)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (time))
            self.connection.commit()
            print(f"Computer usage data saved: {time} minutes for today.")
        except sqlite3.Error as e:
            print(f"Error saving computer usage data: {e}")

    def get_date_id_by_date(self, date):
        query = "SELECT date_id FROM MonitoringDates WHERE date = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error fetching current date_id: {e}")
            return None
        
    def get_computer_usage_by_date(self, date_id):
        query = "SELECT time FROM ComputerUsage WHERE date_id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date_id,))
            results = cursor.fetchall()
            return [row[0] for row in results]
        except sqlite3.Error as e:
            print(f"Error fetching computer usage by date: {e}")
            return None
