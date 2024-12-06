def match_schema(imaging_data, lab_data, patient_data):
    """
    Match and merge data from different sources into a single global schema.
    """
    global_data = []

    for patient in patient_data:
        # Extract relevant patient fields
        global_patient_id = patient['id']  
        first_name = patient['first_name']
        last_name = patient['last_name']
        dob = patient['dob']
        gender = patient['gender']
        contact_number = patient['contact_number']
        email_id = patient['email_id']
        emergency_contact = patient['emergency_contact']
        severity=patient['severity']

        # Get related imaging and lab data
        imaging_info = next((item for item in imaging_data if item['patient_id'] == global_patient_id), None)
        lab_info = next((item for item in lab_data  if item['record_id'] == global_patient_id and item['full_name'] == f"{first_name} {last_name}"), None)

        # Create merged data for global schema
        global_record = {
            'global_patient_id': global_patient_id,
            'first_name': first_name,
            'last_name': last_name,
            'dob': dob,
            'gender': gender,
            'contact_number': contact_number,
            'email_id': email_id,
            'emergency_contact': emergency_contact,
            'severity':severity,
            'imaging_type': imaging_info['imaging_type'] if imaging_info else None,
            'imaging_date': imaging_info['imaging_date'] if imaging_info else None,
            'description': imaging_info['description'] if imaging_info else None,
            'lab_test_name': lab_info['test_name'] if lab_info else None,
            'lab_test_results': lab_info['test_results'] if lab_info else None,
            'lab_name': lab_info['lab_name'] if lab_info else None,
            'lab_doctor_name': lab_info['doctor_name'] if lab_info else None,
            'lab_comments': lab_info['comments'] if lab_info else None,
            'imaging_url': convert_drive_link_to_direct_url(imaging_info.get('url')) if imaging_info else None,  # Convert and save Google Drive URL
        }

        global_data.append(global_record)

    return global_data


def convert_drive_link_to_direct_url(shareable_link):
    """
    Convert Google Drive shareable link to a direct URL for embedding.
    """
    try:
        file_id = shareable_link.split('/d/')[1].split('/')[0]
        return f"https://drive.google.com/uc?id={file_id}"
    except IndexError:
        raise ValueError("Invalid Google Drive shareable link")