from django.db import models

class GlobalPatientSchema(models.Model):
    global_patient_id = models.IntegerField()  # Patient identifier, linking data across sources
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)  # Allow null and blank values
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    email_id = models.EmailField(null=True, blank=True)  # Allow null and blank values for email
    emergency_contact = models.CharField(max_length=15)
    severity=models.CharField(max_length=15)
 
    imaging_type = models.CharField(max_length=50, null=True, blank=True)
    imaging_date = models.DateField(null=True, blank=True)  # Allow null and blank values
    description = models.TextField(null=True, blank=True)
    imaging_url = models.URLField(null=True, blank=True) 
    

    # Lab results
    lab_test_name = models.CharField(max_length=100, null=True, blank=True)
    lab_test_results = models.TextField(null=True, blank=True)
    lab_name = models.CharField(max_length=100, null=True, blank=True)
    lab_doctor_name = models.CharField(max_length=100, null=True, blank=True)
    lab_comments = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['global_patient_id']),  # Index on global_patient_id for performance
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.global_patient_id}"
