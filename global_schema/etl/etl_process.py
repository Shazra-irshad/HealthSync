
import logging
from .schema_matching import match_schema
from global_schema.models import GlobalPatientSchema

logger = logging.getLogger(__name__)

class DatabaseDownException(Exception):
    pass

def run_etl_process():
    """
    Run the ETL process to extract data from MongoDB and MySQL,
    transform it into the global schema format, and load it into the
    global schema.
    """
    try:
        
        print("Starting extraction of imaging data...")
        imaging_data = extract_imaging_data()
        print(f"Extracted imaging data: {len(imaging_data)} records")

        print("Starting extraction of lab data...")
        lab_data = extract_lab_data()
        print(f"Extracted lab data: {len(lab_data)} records")

        print("Starting extraction of patient data...")
        patient_data = extract_patient_data()
        print(f"Extracted patient data: {len(patient_data)} records")

        # Step 2: Transform the data into a global schema format
        print("Starting schema matching...")
        global_data = match_schema(imaging_data, lab_data, patient_data)
        print(f"Transformed data into global schema format: {len(global_data)} records")

        # Step 3: Load data into the global schema
        print("Starting loading process...")
        load_global_data(global_data)
        print("ETL process completed successfully.")

    except Exception as e:
        print(f"Error during ETL process: {e}")
        logger.error(f"ETL process failed: {e}", exc_info=True)
        raise DatabaseDownException("The database is down or there was a failure in the ETL process.")


from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, NetworkTimeout

def extract_imaging_data():
    try:
        print("Connecting to MongoDB for imaging data...")
        client = MongoClient('mongodb://IP.X.X.X:27017/', serverSelectionTimeoutMS=5000)
        db = client['Imaging_data']
        collection = db['Imaging_data']
        data = list(collection.find())
        print(f"Retrieved {len(data)} imaging records")
        return data
    except ServerSelectionTimeoutError as e:
        print(f"Error: Could not connect to MongoDB (imaging data) - {e}")
        raise
    except NetworkTimeout as e:
        print(f"Error: Network timeout while accessing MongoDB (imaging data) - {e}")
        raise
    except Exception as e:
        print(f"General error while extracting imaging data: {e}")
        raise

def extract_lab_data():
    try:
        print("Connecting to MongoDB for lab data...")
        client = MongoClient('mongodb://IP.X.X.X:27017/', serverSelectionTimeoutMS=5000)
        db = client['Lab_result']
        collection = db['Lab_result']
        data = list(collection.find())
        print(f"Retrieved {len(data)} lab records")
        return data
    except ServerSelectionTimeoutError as e:
        print(f"Error: Could not connect to MongoDB (lab data) - {e}")
        raise
    except NetworkTimeout as e:
        print(f"Error: Network timeout while accessing MongoDB (lab data) - {e}")
        raise
    except Exception as e:
        print(f"General error while extracting lab data: {e}")
        raise


def dictfetchall(cursor):
    """
    Convert query results to dictionaries.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


from django.db import connections
from django.db.utils import OperationalError
def extract_patient_data():
    """
    Extract patient data from MySQL and return it as a list of dictionaries.
    """
    try:
        print("Connecting to MySQL for patient data...")
        cursor = connections['default'].cursor()
        query = "SELECT * FROM patient_registry.patient_registry;"
        print(f"Executing query: {query}")
        cursor.execute(query)
        data = dictfetchall(cursor)
        print(f"Retrieved {len(data)} patient records")
        return data
    except OperationalError as e:
        print(f"Database connection error: {e}")
        raise OperationalError("MySQL connection failed for patient data.")
    except Exception as e:
        print(f"Error while extracting patient data: {e}")
        raise


def load_global_data(global_data):
    try:
        print(f"Loading {len(global_data)} records into the global schema...")
        for index, data in enumerate(global_data, start=1):
            GlobalPatientSchema.objects.update_or_create(
                global_patient_id=data['global_patient_id'],
                defaults=data
            )
            if index % 100 == 0: 
                print(f"Loaded {index} records so far...")
        print("All data loaded into the global schema successfully.")
    except Exception as e:
        print(f"Error while loading global data: {e}")
        raise





import json
from datetime import datetime
def process_change(change):
    """
    Process a single change detected in MongoDB or MySQL and update the global schema.
    """
    try:
        print(f"Change object: {change}")
    
        if change['change_type'] in ['INSERT', 'UPDATE']:  
            new_data = change.get('new_data')
            if new_data:
                full_document = json.loads(new_data)
                print(f"Processing update/insert for MySQL record: {full_document}")
                update_global_schema(full_document)

        elif change['change_type'] == 'DELETE':
            old_data = change.get('old_data')
            if old_data:
                print(f"Processing delete for MySQL record: {old_data}")
                delete_global_schema(old_data)  

        else:
            print(f"Unknown change type: {change['change_type']}")

    except Exception as e:
        print(f"Error processing change: {e}")
        raise


def update_global_schema(data):
    """
    Update or create a global schema entry based on the given data.
    """
    print(f"Data object: {data}")

    global_patient_id = data.get('id')  
    
    GlobalPatientSchema.objects.update_or_create(
        global_patient_id=global_patient_id,  
        defaults={
            "first_name": data.get('first_name', ''),
            "last_name": data.get('last_name', ''),
            "dob": data.get('dob', ''),
            "gender": data.get('gender', ''),
            "contact_number": data.get('contact_number', ''),
            "email_id": data.get('email_id', ''),
            "emergency_contact": data.get('emergency_contact', ''),
           
        },
    )
import json

def delete_global_schema(old_data):
    """
    Delete an entry from the global schema using the data from the deleted record.
    """
    try:      
        if isinstance(old_data, str):
            old_data = json.loads(old_data)
        global_patient_id = old_data.get('id')  
        
        if global_patient_id:
            GlobalPatientSchema.objects.filter(global_patient_id=global_patient_id).delete()
            print(f"Deleted record for global_patient_id: {global_patient_id}")
        else:
            print("No global_patient_id found in old data. Deletion aborted.")
    
    except Exception as e:
        print(f"Error deleting record: {e}")
