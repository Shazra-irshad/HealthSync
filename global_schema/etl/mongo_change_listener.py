from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta
from django.db import IntegrityError

def sync_Lab_mongo_to_global_schema():
    try:
       
        client = MongoClient("mongodb://IP.X.X.X:27017/")
        db = client["Lab_result"]
        collection = db["Lab_result"]

       
        now = datetime.utcnow()
        last_24_hours = now - timedelta(days=1)

       
        recent_documents = collection.find({"creation_date": {"$gte": last_24_hours}})
        
        for document in recent_documents:
            update_lab_global_schema_mongo(document)

        print(" Mongo Sync completed successfully.")
    except PyMongoError as e:
        print(f"Error syncing with MongoDB: {e}")

def update_lab_global_schema_mongo(document):
    from global_schema.models import GlobalPatientSchema

    try:
        full_name = document.get("full_name", "")
        name_parts = full_name.split(maxsplit=1)  # Split into at most two parts
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        # Map MongoDB fields to Global Schema fields
        GlobalPatientSchema.objects.update_or_create(
            global_patient_id=document["record_id"],

            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "lab_test_name": document.get("test_name"),
                 "lab_test_date": document.get("test_date"),
                "lab_doctor_name": document.get("doctor_name"),
                "lab_comments": document.get("comments"),
                "lab_test_results": document.get("test_results"),
                
            },
        )
        print(f"Updated Global Schema for patient_id: {document['record_id']}")
    except IntegrityError as e:
        print(f"Integrity error: {e}")
    except Exception as e:
        print(f"Error updating Global Schema: {e}")



def sync_imaging_mongo_to_global_schema():
    try:
        
        client = MongoClient("mongodb://IP.X.X.X:27017/")
        db = client["Imaging_data"]
        collection = db["Imaging_data"]

       
        now = datetime.utcnow()
        last_24_hours = now - timedelta(days=1)

       
        recent_documents = collection.find({"creation_date": {"$gte": last_24_hours}})
        
        for document in recent_documents:
            update_imaging_global_schema_mongo(document)

        print("Imaging Mongo Sync completed successfully.")
    except PyMongoError as e:
        print(f"Error syncing with MongoDB: {e}")

def update_imaging_global_schema_mongo(document):
    from global_schema.models import GlobalPatientSchema

    try:
      
        
        
        GlobalPatientSchema.objects.update_or_create(
            global_patient_id=document["patient_id"],

            defaults={       
                "imaging_type": document.get("imaging_type"),
                "imaging_date": document.get("imaging_date"),
                "description": document.get("description"),
                "imaging_url": document.get("url"),
            },
        )
        print(f"Updated Global Schema for imaging_id: {document['patient_id']}")
    except IntegrityError as e:
        print(f"Integrity error: {e}")
    except Exception as e:
        print(f"Error updating Global Schema: {e}")
