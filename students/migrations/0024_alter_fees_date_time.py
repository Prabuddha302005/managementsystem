# Generated by Django 5.1.1 on 2024-11-06 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0023_alter_fees_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fees',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 21, 18, 4, 524496)),
        ),
    ]