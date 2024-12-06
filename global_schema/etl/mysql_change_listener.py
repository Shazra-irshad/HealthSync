from django.db import connections
def dictfetchall(cursor):
    """
    Convert query results to dictionaries.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def watch_mysql_changes(callback_function):
    print("Watching MySQL changes...")
    while True:
        cursor = connections['default'].cursor()
        cursor.execute("SELECT * FROM patient_registry.patient_changes;")
        changes = dictfetchall(cursor)  # Convert to dictionaries for easy processing

        for change in changes:
            print(f"Detected MySQL change: {change}")
            callback_function(change)

        # Clear the changes after processing
        cursor.execute("TRUNCATE TABLE patient_registry.patient_changes;")
