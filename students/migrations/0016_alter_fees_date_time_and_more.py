# Generated by Django 5.1.1 on 2024-11-06 07:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0015_alter_fees_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fees',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 12, 33, 48, 964947)),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='aadhaar_number',
            field=models.BigIntegerField(null=True),
        ),
    ]
