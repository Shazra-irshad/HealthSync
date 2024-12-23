# Generated by Django 5.1.3 on 2024-11-30 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPatientSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('global_patient_id', models.IntegerField()),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(max_length=10)),
                ('contact_number', models.CharField(max_length=15)),
                ('email_id', models.EmailField(blank=True, max_length=254, null=True)),
                ('emergency_contact', models.CharField(max_length=15)),
                ('severity', models.CharField(max_length=15)),
                ('imaging_type', models.CharField(blank=True, max_length=50, null=True)),
                ('imaging_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('imaging_url', models.URLField(blank=True, null=True)),
                ('lab_test_name', models.CharField(blank=True, max_length=100, null=True)),
                ('lab_test_results', models.TextField(blank=True, null=True)),
                ('lab_name', models.CharField(blank=True, max_length=100, null=True)),
                ('lab_doctor_name', models.CharField(blank=True, max_length=100, null=True)),
                ('lab_comments', models.TextField(blank=True, null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['global_patient_id'], name='global_sche_global__7c7865_idx')],
            },
        ),
    ]
