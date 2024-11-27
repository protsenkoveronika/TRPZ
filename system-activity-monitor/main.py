from activity_monitor import ActivityMonitor

def main():
    db_file = 'db.sqlite'

    monitor = ActivityMonitor(db_file)
    monitor.start_gui()
    

if __name__ == "__main__":
    main()