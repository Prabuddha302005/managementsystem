# Generated by Django 5.1.1 on 2024-11-06 06:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interns', '0007_alter_feesintern_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feesintern',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 12, 15, 51, 957706)),
        ),
    ]