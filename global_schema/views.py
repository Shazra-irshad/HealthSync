# global_schema/views.py

from django.http import JsonResponse
from global_schema.etl.etl_process import run_etl_process,DatabaseDownException
from django.shortcuts import render
from .models import GlobalPatientSchema
import google.generativeai as genai
import requests

# views.py

# def main_page(request):
#     return render(request, 'global_schema/main_page.html') 


def main_page(request):
    # Count total doctors (distinct lab_doctor_name)
    total_doctors = GlobalPatientSchema.objects.values('lab_doctor_name').distinct().count()

    # Count total patients
    total_patients = GlobalPatientSchema.objects.count()

    # Distribution of patients by severity
    severity_distribution = {
        "Severe": GlobalPatientSchema.objects.filter(severity__iexact="severe").count(),
        "Mild": GlobalPatientSchema.objects.filter(severity__iexact="mild severe").count(),
        "Healthy": GlobalPatientSchema.objects.filter(severity__iexact="healthy").count(),
    }

    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'severity_distribution': severity_distribution,
    }

    return render(request, 'global_schema/main_page.html', context)






def run_etl_view(request):
    try:
        # Call the ETL process
        run_etl_process()
        return JsonResponse({"message": "ETL process completed successfully."}, status=200)

    except DatabaseDownException as e:
        # Catch the custom exception and return an error message
        print(f"Database issue: {e}")
        return JsonResponse({"error": "Database is down. Please try again later."}, status=503)

    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error: {e}")
        return JsonResponse({"error": "An unexpected error occurred. Please try again later."}, status=500)




# from django.shortcuts import render
from .models import GlobalPatientSchema
from django.db import OperationalError

#      
from django.db import OperationalError
from .models import GlobalPatientSchema
from django.shortcuts import render

def get_patient_details(request):
    """
    Query GlobalSchema based on full_name and patient_id, and display selected details.
    """
    if request.method == 'GET':
        # Get query parameters
        full_name = request.GET.get('full_name', '').strip()
        patient_id = request.GET.get('patient_id', '').strip()

        # If no input provided, show the form
        if not full_name and not patient_id:
            return render(request, 'global_schema/search_form.html')

        # Validate input: Both full_name and patient_id are required or one of them can be used for searching
        if not full_name and not patient_id:
            return render(request, 'global_schema/error.html', {'error': 'Please provide either full_name or patient_id.'})

        # Split the full_name into first and last name and strip whitespace
        if full_name:
            name_parts = full_name.split()
            if len(name_parts) >= 2:
                first_name = name_parts[0].strip()
                last_name = ' '.join(name_parts[1:]).strip()  # In case there's a middle name
            else:
                first_name = name_parts[0].strip()
                last_name = ''
        else:
            first_name = last_name = ''

        try:
            # Query GlobalPatientSchema based on the provided fields
            if full_name and patient_id:
                patient = GlobalPatientSchema.objects.get(first_name__iexact=first_name, last_name__iexact=last_name, global_patient_id=patient_id)
            elif full_name:
                patient = GlobalPatientSchema.objects.get(first_name__iexact=first_name, last_name__iexact=last_name)
            elif patient_id:
                patient = GlobalPatientSchema.objects.get(global_patient_id=patient_id)

            # Extract and return selected fields
            selected_data = {
                'full_name': f"{patient.first_name} {patient.last_name}",
                'patient_id': patient.global_patient_id,
                'dob': patient.dob,
                'gender': patient.gender,
                'contact_number': patient.contact_number,
                'lab_test_name': patient.lab_test_name,
                # 'test_date': patient.test_date,
                'lab_test_results': patient.lab_test_results,
                'imaging_type': patient.imaging_type,
                'imaging_url': patient.imaging_url,
                # 'description': patient.description,
            }

            return render(request, 'global_schema/patient_details.html', {'patient': selected_data})

        except GlobalPatientSchema.DoesNotExist:
            return render(request, 'global_schema/error.html', {'error': 'Patient not found.'})

        except OperationalError as e:
            # Handle database connection errors (e.g., database down)
            print(f"OperationalError: {e}")
            return render(request, 'global_schema/error.html', {'error': 'Database is down. Please try again later.'})

    # In case of any other request method
    return render(request, 'global_schema/error.html', {'error': 'Invalid request method. Use GET.'})


# def get_doctor_patients(request):
#     """
#     Query GlobalSchema to find all patients associated with a specific doctor,
#     a specified severity category, or both, and display their details.
#     """
#     if request.method == 'GET':
#         # Get query parameters
#         doctor_name = request.GET.get('doctor_name', '').strip()
#         severity_category = request.GET.get('severity', '').strip().lower()  # Normalize the input

#         # Validate input: At least one of doctor_name or severity must be provided
#         if not doctor_name and not severity_category:
#             return render(request, 'global_schema/doctor_search_form.html', {
#                 'error': 'Please provide at least Doctor Name or Severity Category.'
#             })

#         try:
#             # Build the query dynamically based on provided inputs
#             query = {}
#             if doctor_name:
#                 query['lab_doctor_name__iexact'] = doctor_name
#             if severity_category:
#                 query['severity__iexact'] = severity_category

#             # Query the GlobalSchema model
#             patients = GlobalPatientSchema.objects.filter(**query)

#             if not patients.exists():
#                 return render(request, 'global_schema/error.html', {
#                     'error': f"No patients found for the given criteria."
#                 })

#             # Prepare the data to pass to the template
#             selected_data = []
#             for patient in patients:
#                 selected_data.append({
#                     'patient_id': patient.global_patient_id,
#                     'full_name': f"{patient.first_name} {patient.last_name}",
#                     'dob': patient.dob,
#                     'gender': patient.gender,
#                     'contact_number': patient.contact_number,
#                     'lab_test_name': patient.lab_test_name,
#                     'lab_test_results': patient.lab_test_results,
#                     'imaging_type': patient.imaging_type,
#                     'description': patient.description,
#                     'severity': patient.severity,
#                     'imaging_url': patient.imaging_url,  # Include severity in the response
#                 })

#             # Render the template with the filtered patients
#             return render(request, 'global_schema/doctor_patients.html', {
#                 'doctor_name': doctor_name,
#                 'severity': severity_category,
#                 'patients': selected_data
#             })

#         except Exception as e:
#             return render(request, 'global_schema/error.html', {'error': f"An error occurred: {str(e)}"})

#     return render(request, 'global_schema/error.html', {'error': 'Invalid request method. Use GET.'})
import json
import ast
import json

def get_doctor_patients(request):
    """
    Query GlobalSchema to find all patients associated with a specific doctor,
    a specified severity category, or both, and display their details.
    """
    if request.method == 'GET':
        # Get query parameters
        doctor_name = request.GET.get('doctor_name', '').strip()
        severity_category = request.GET.get('severity', '').strip().lower()  # Normalize the input

        # Validate input: At least one of doctor_name or severity must be provided
        if not doctor_name and not severity_category:
            return render(request, 'global_schema/doctor_search_form.html', {
                'error': 'Please provide at least Doctor Name or Severity Category.'
            })

        try:
            # Build the query dynamically based on provided inputs
            query = {}
            if doctor_name:
                query['lab_doctor_name__iexact'] = doctor_name
            if severity_category:
                query['severity__iexact'] = severity_category

            # Query the GlobalSchema model
            patients = GlobalPatientSchema.objects.filter(**query)

            if not patients.exists():
                return render(request, 'global_schema/error.html', {
                    'error': f"No patients found for the given criteria."
                })

            # Prepare the data to pass to the template
            selected_data = []
            for patient in patients:
                # Convert lab_test_results to dictionary if needed
                lab_test_results = {}
                if isinstance(patient.lab_test_results, str):
                    try:
                        lab_test_results = json.loads(patient.lab_test_results)
                    except json.JSONDecodeError:
                        try:
                            lab_test_results = ast.literal_eval(patient.lab_test_results)
                        except (ValueError, SyntaxError) as e:
                            print(f"Error decoding Lab Test Results for Patient ID {patient.global_patient_id}: {e}")
                elif isinstance(patient.lab_test_results, dict):
                    lab_test_results = patient.lab_test_results
                else:
                    lab_test_results = {}

                print(f"Patient ID {patient.global_patient_id}, Processed Lab Test Results: {lab_test_results},Type: {type(lab_test_results)}")

                selected_data.append({
                    'patient_id': patient.global_patient_id,
                    'full_name': f"{patient.first_name} {patient.last_name}",
                    'dob': patient.dob,
                    'gender': patient.gender,
                    'contact_number': patient.contact_number,
                    'lab_test_name': patient.lab_test_name,
                    'lab_test_results': lab_test_results,
                    'imaging_type': patient.imaging_type,
                    'description': patient.description,
                    'severity': patient.severity,
                    'imaging_url': patient.imaging_url,
                })

            # Render the template with the filtered patients
            return render(request, 'global_schema/doctor_patients.html', {
                'doctor_name': doctor_name,
                'severity': severity_category,
                'patients': selected_data
            })

        except Exception as e:
            return render(request, 'global_schema/error.html', {
                'error': f"An error occurred while processing your request: {str(e)}"
            })

    return render(request, 'global_schema/error.html', {'error': 'Invalid request method. Use GET.'})


import google.generativeai as genai
from django.http import JsonResponse
from .models import GlobalPatientSchema
from django.conf import settings  # Import settings to access the API key

def get_suggestion(request):
    """
    Fetch LLM suggestions for a specific patient using Gemini.
    """
    patient_id = request.GET.get('patient_id', '').strip()

    if not patient_id:
        return JsonResponse({'error': 'Patient ID is required'}, status=400)

    try:
        # Query the database for the patient's lab results and description
        print(f"Fetching patient with ID: {patient_id}")
        patient = GlobalPatientSchema.objects.get(global_patient_id=patient_id)
        # print(f"Found patient: {patient.full_name}")

        # Prepare the prompt
        prompt = (
            f"Given the lab results: {patient.lab_test_results}, "
            f"lab comments: {patient.lab_comments}, "
            f"and imaging description: {patient.description}, "
            "suggest possible diseases."
        )
        print(f"Generated prompt: {prompt}")

        # Hardcode the Gemini API key in the settings.py
        gemini_api_key = settings.GEMINI_API_KEY  # Ensure GEMINI_API_KEY is set in your settings.py
        if not gemini_api_key:
            return JsonResponse({'error': 'Gemini API key is missing in settings.'}, status=500)

        # Initialize the Gemini model with the API key from settings
        genai.configure(api_key=gemini_api_key)  # Configure Gemini with the API key
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])

        # Send the prompt to Gemini and get the response
        response = chat.send_message(prompt)
        print(f"Gemini response: {response.text}")

        suggested_diseases = response.text if response else "No suggestions available"

        return JsonResponse({'suggested_diseases': suggested_diseases}, status=200)
    
    except GlobalPatientSchema.DoesNotExist:
        print(f"Patient with ID {patient_id} does not exist.")
        return JsonResponse({'error': 'Patient not found'}, status=404)
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return JsonResponse({'error': f'Error processing request: {str(e)}'}, status=500)


from django.shortcuts import render
from .models import GlobalPatientSchema

# def get_radiologist_imaging_data(request):
#     """
#     Query GlobalSchema based on full_name and patient_id, and display imaging data.
#     """
#     if request.method == 'GET':
#         # Get query parameters
#         full_name = request.GET.get('full_name', '').strip()
#         patient_id = request.GET.get('patient_id', '').strip()

#         # If no input provided, render the form
#         if not full_name and not patient_id:
#             return render(request, 'global_schema/radiologist_search_form.html')

#         # Validate input: Both full_name and patient_id are required or one of them can be used for searching
#         if not full_name and not patient_id:
#             return render(request, 'global_schema/error.html', {'error': 'Please provide either full_name or patient_id.'})

#         # Split the full_name into first and last name and strip whitespace
#         if full_name:
#             name_parts = full_name.split()
#             if len(name_parts) >= 2:
#                 first_name = name_parts[0].strip()
#                 last_name = ' '.join(name_parts[1:]).strip()  # In case there's a middle name
#             else:
#                 first_name = name_parts[0].strip()
#                 last_name = ''
#         else:
#             first_name = last_name = ''

#         try:
#             # Query GlobalPatientSchema based on the provided fields
#             if full_name and patient_id:
#                 patient = GlobalPatientSchema.objects.get(first_name__iexact=first_name, last_name__iexact=last_name, global_patient_id=patient_id)
#             elif full_name:
#                 patient = GlobalPatientSchema.objects.get(first_name__iexact=first_name, last_name__iexact=last_name)
#             elif patient_id:
#                 patient = GlobalPatientSchema.objects.get(global_patient_id=patient_id)

#             # Extract and return imaging-related fields
#             imaging_data = {
#                 'patient_id': patient.global_patient_id,
#                 'full_name': f"{patient.first_name} {patient.last_name}",
#                 'dob': patient.dob,
#                 'gender': patient.gender,
#                 'imaging_type': patient.imaging_type,
#                 'imaging_date': patient.imaging_date,
#                 'description': patient.description,
#                 'imaging_url': patient.imaging_url,
#             }

#             return render(request, 'global_schema/radiologist_imaging_data.html', {'imaging_data': imaging_data})

#         except GlobalPatientSchema.DoesNotExist:
#             return render(request, 'global_schema/error.html', {'error': 'Patient not found.'})

#     return render(request, 'global_schema/error.html', {'error': 'Invalid request method. Use GET.'})


def get_radiologist_imaging_data(request):
    """
    Query GlobalSchema based on full_name, patient_id, or imaging_type, and display imaging data.
    """
    if request.method == 'GET':
        # Get query parameters
        full_name = request.GET.get('full_name', '').strip()
        patient_id = request.GET.get('patient_id', '').strip()
        imaging_type = request.GET.get('imaging_type', '').strip()

        # If no input provided, render the form
        if not full_name and not patient_id and not imaging_type:
            return render(request, 'global_schema/radiologist_search_form.html')

        # Validate input: At least one of the search criteria must be provided
        if not full_name and not patient_id and not imaging_type:
            return render(request, 'global_schema/error.html', {'error': 'Please provide at least one of full_name, patient_id, or imaging_type for search.'})

        # Split the full_name into first and last name and strip whitespace
        if full_name:
            name_parts = full_name.split()
            if len(name_parts) >= 2:
                first_name = name_parts[0].strip()
                last_name = ' '.join(name_parts[1:]).strip()  # In case there's a middle name
            else:
                first_name = name_parts[0].strip()
                last_name = ''
        else:
            first_name = last_name = ''

        try:
            # Build the query filter dynamically based on the inputs
            query_filter = {}

            if full_name:
                query_filter['first_name__iexact'] = first_name
                query_filter['last_name__iexact'] = last_name

            if patient_id:
                query_filter['global_patient_id'] = patient_id

            if imaging_type:
                query_filter['imaging_type__iexact'] = imaging_type

            # If imaging_type is provided, return all matching patients
            if imaging_type:
                patients = GlobalPatientSchema.objects.filter(**query_filter)

                if not patients:
                    return render(request, 'global_schema/error.html', {'error': 'No patients found with the provided imaging type.'})

                # Collect the imaging data for all patients matching the filter
                imaging_data_list = []
                for patient in patients:
                    imaging_data_list.append({
                        'patient_id': patient.global_patient_id,
                        'full_name': f"{patient.first_name} {patient.last_name}",
                        'dob': patient.dob,
                        'gender': patient.gender,
                        'imaging_type': patient.imaging_type,
                        'imaging_date': patient.imaging_date,
                        'description': patient.description,
                        'imaging_url': patient.imaging_url,
                    })

                return render(request, 'global_schema/radiologist_imaging_data_list.html', {'imaging_data_list': imaging_data_list})

            # Query for a single patient if all the criteria are met
            patient = GlobalPatientSchema.objects.get(**query_filter)

            # Extract and return imaging-related fields for the single patient
            imaging_data = {
                'patient_id': patient.global_patient_id,
                'full_name': f"{patient.first_name} {patient.last_name}",
                'dob': patient.dob,
                'gender': patient.gender,
                'imaging_type': patient.imaging_type,
                'imaging_date': patient.imaging_date,
                'description': patient.description,
                'imaging_url': patient.imaging_url,
            }

            return render(request, 'global_schema/radiologist_imaging_data.html', {'imaging_data': imaging_data})

        except GlobalPatientSchema.DoesNotExist:
            return render(request, 'global_schema/error.html', {'error': 'Patient not found with the provided search criteria.'})

    return render(request, 'global_schema/error.html', {'error': 'Invalid request method. Use GET.'})