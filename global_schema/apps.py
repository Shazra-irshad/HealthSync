from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
# from .etl.orchestrator import orchestrate_etl

class GlobalSchemaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'global_schema'
# global_schema/apps.py

# from django.apps import AppConfig
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from threading import Thread
# from .etl.orchestrator import schedule_etl_job  # Import the schedule_etl_job function from the orchestrator

# class GlobalSchemaConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'global_schema'

#     def ready(self):
#         # Connect the post_migrate signal to start the ETL process
#         post_migrate.connect(start_etl_scheduler, sender=self)

# # Signal receiver that starts the ETL scheduler after migrations
# @receiver(post_migrate)
# def start_etl_scheduler(sender, **kwargs):
#     """
#     This function will start the ETL scheduler in a background thread once the migrations are done.
#     """
#     print("Starting ETL Scheduler...")
#     # Start the scheduler in a separate thread
#     Thread(target=schedule_etl_job, daemon=True).start()
