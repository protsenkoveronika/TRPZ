import sqlite3

class WindowRepository:
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

    def insert_window_usage(self, window_name, usage_time):
        window_id = self.get_window_id_by_name(window_name)
        query = """
        INSERT INTO WindowUsage (winusage_id, date_id, window_id, time)
        VALUES ((SELECT IFNULL(MAX(winusage_id), 0) + 1 FROM WindowUsage), (SELECT date_id FROM MonitoringDates ORDER BY date_id DESC LIMIT 1), ?, ?)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (window_id, usage_time))
            self.connection.commit()
            print(f"Window usage for {window_name} saved: {usage_time} seconds.")
        except sqlite3.Error as e:
            print(f"Error saving window usage: {e}")

    def get_window_id_by_name(self, window_name):
        query = "SELECT window_id FROM Windows WHERE name = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (window_name,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return self.insert_new_window(window_name)
        except sqlite3.Error as e:
            print(f"Error getting window ID for {window_name}: {e}")
            return None

    def insert_new_window(self, window_name):
        query = "INSERT INTO Windows (name) VALUES (?)"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (window_name,))
            self.connection.commit()
            new_window_id = cursor.lastrowid
            print(f"New window {window_name} inserted with ID: {new_window_id}")
            return new_window_id
        except sqlite3.Error as e:
            print(f"Error inserting new window {window_name}: {e}")
            return None    

    def get_window_usage_by_date(self, date):
        query = """
        SELECT window_name, usage_time FROM WindowUsage
        JOIN MonitoringDates ON WindowUsage.date_id = MonitoringDates.date_id
        WHERE MonitoringDates.date = ?
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching window usage for date {date}: {e}")
            return []
