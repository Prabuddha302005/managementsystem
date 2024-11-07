# Generated by Django 5.1.1 on 2024-11-06 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interns', '0018_internproject_project_pdf_interntasks_task_pdf_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feesintern',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 21, 15, 15, 399769)),
        ),
        migrations.AlterField(
            model_name='internproject',
            name='project_file',
            field=models.FileField(blank=True, null=True, upload_to='intern_projects_submission/'),
        ),
        migrations.AlterField(
            model_name='internproject',
            name='project_pdf',
            field=models.FileField(upload_to='assigned_intern_projects/'),
        ),
    ]