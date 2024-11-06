# Generated by Django 5.1.1 on 2024-11-06 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0016_alter_fees_date_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentstasks',
            name='task_description',
        ),
        migrations.AddField(
            model_name='studentstasks',
            name='task_pdf',
            field=models.FileField(default=1, upload_to='intern_taks/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fees',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 13, 51, 34, 678162)),
        ),
    ]
