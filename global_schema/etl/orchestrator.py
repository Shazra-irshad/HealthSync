import schedule
import time
from threading import Thread
from .etl_process import process_change
from .mysql_change_listener import watch_mysql_changes
from .mongo_change_listener import sync_Lab_mongo_to_global_schema,sync_imaging_mongo_to_global_schema

def orchestrate_etl():
    """
    Start the ETL process, which monitors MySQL changes.
    """
    print("Starting ETL Orchestrator...")

    # Run the MySQL change listener in a separate thread
    Thread(target=watch_mysql_changes, args=(process_change,)).start()
    Thread(target=sync_Lab_mongo_to_global_schema).start()
    Thread(target=sync_imaging_mongo_to_global_schema).start()



def schedule_etl_job():
    """
    Schedule the ETL job to run at a specific interval.
    """
    schedule.every(12).hours.do(orchestrate_etl)  # Run every 12 hours

    print("Scheduling ETL job...")
    while True:
        schedule.run_pending()  
        time.sleep(1)  

