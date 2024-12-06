
from django.urls import path,include
from global_schema.views import run_etl_view
from . import views

urlpatterns = [
    path('run-etl/', run_etl_view, name='run_etl'),
    path('patient-details/', views.get_patient_details, name='patient_details'),  # Patient details route
    path('doctor-patients/', views.get_doctor_patients, name='doctor_patients'),
    path('radiologist-imaging/', views.get_radiologist_imaging_data, name='radiologist_imaging_data'),
    path('get-suggestion/', views.get_suggestion, name='get_suggestion'),
     path('home/', views.main_page, name='main_page'),
]