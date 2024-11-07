from repositories.monitor_repository import MonitorRepository
from repositories.memory_repository import MemoryRepository
from memory_usage import MemoryUsage


def main():
    db_file = 'db.sqlite'

    monitor_repo = MonitorRepository(db_file)
    monitor_repo.insert_current_date()
    monitor_repo.close()

    memory_usage_monitor = MemoryUsage(db_file)
    memory_usage_monitor.first_check_and_monitoring()
    

    # Other initialization code...

    # Close the database connection when done
    memory_usage_monitor.close()
    

if __name__ == "__main__":
    main()