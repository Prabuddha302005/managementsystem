# Generated by Django 5.1.1 on 2024-11-06 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interns', '0012_alter_feesintern_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feesintern',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 13, 51, 34, 682153)),
        ),
    ]
