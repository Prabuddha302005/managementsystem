# Generated by Django 5.1.1 on 2024-11-06 07:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_alter_fees_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fees',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 12, 30, 59, 696237)),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='aadhaar_number',
            field=models.IntegerField(max_length=13, null=True),
        ),
    ]
