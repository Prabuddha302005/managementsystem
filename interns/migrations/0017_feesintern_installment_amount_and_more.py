# Generated by Django 5.1.1 on 2024-11-06 13:37

import datetime
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interns', '0016_internprofile_aadhaar_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feesintern',
            name='installment_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AlterField(
            model_name='feesintern',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 19, 7, 39, 849041)),
        ),
    ]