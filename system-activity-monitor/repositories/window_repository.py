import sqlite3

class WindowRepository:
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

    def get_or_add_window_id(self, name):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT window_id FROM Windows WHERE name = ?", (name,))
            result = cursor.fetchone()
            if result:
                return result[0]
            cursor.execute("INSERT INTO Windows (name) VALUES (?)", (name,))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error in get_or_add_window_id: {e}")
            return None

    def insert_window_usage(self, date_id, window_id, time):
        query = """
        INSERT INTO WindowUsage (winusage_id, date_id, window_id, time)
        VALUES ((SELECT IFNULL(MAX(winusage_id), 0) + 1 FROM WindowUsage), ?, ?, ?)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date_id, window_id, time))
            self.connection.commit()
            # print(f"Window usage saved: Date ID {date_id}, Window ID {window_id}, Time {time} seconds.")
        except sqlite3.Error as e:
            print(f"Error saving window usage: {e}")
            raise


    def get_window_usage_by_date(self, date):
        query = """
        SELECT Windows.name, WindowUsage.time 
        FROM WindowUsage
        JOIN MonitoringDates ON WindowUsage.date_id = MonitoringDates.date_id
        JOIN Windows ON WindowUsage.window_id = Windows.window_id
        WHERE MonitoringDates.date = ?;
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (date,))
            data = cursor.fetchall()
            # print("Window usage data for date", date, ":", data)
            return data
        except sqlite3.Error as e:
            print(f"Error fetching window usage for date {date}: {e}")
            return []

    # def delete_last_window_usage(self):
    #         try:
    #             cursor = self.connection.cursor()
    #             # Delete the last entry based on the most recent timestamp
    #             cursor.execute("""
    #                 DELETE FROM WindowUsage
    #         WHERE winusage_id = ;
    #             """)
    #             self.connection.commit()
    #             print("Last processor usage deleted successfully.")
    #         except sqlite3.Error as e:
    #             print(f"Error deleting last processor usage: {e}")


# repo = WindowRepository("db.sqlite")

# resp = repo.delete_last_window_usage()

# repo.close()
# print(resp)