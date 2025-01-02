import sqlite3

class MonitoringDaysRepository:
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
        
    def get_or_add_date_id(self, date):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT date_id FROM MonitoringDates WHERE date = ?", (date,))
            result = cursor.fetchone()
            if result:
                return result[0]
            cursor.execute("INSERT INTO MonitoringDates (date) VALUES (?)", (date,))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error in get_or_add_date_id: {e}")
            return None

    # def delete_last_date(self):
    #     """Delete the most recent date from the MonitoringDates table."""
    #     try:
    #         cursor = self.connection.cursor()
    #         cursor.execute("""
    #             DELETE FROM MonitoringDates
    #             WHERE date = (SELECT date FROM MonitoringDates ORDER BY date DESC LIMIT 1)
    #         """)
    #         self.connection.commit()
    #         print("Last date deleted successfully.")
    #     except sqlite3.Error as e:
    #         print(f"Error deleting last date: {e}")


# # Create an instance of the repository
# repo = MonitoringDaysRepository("db.sqlite")

# # Delete the most recent processor usage
# repo.delete_last_date()

# # Close the connection
# repo.close()