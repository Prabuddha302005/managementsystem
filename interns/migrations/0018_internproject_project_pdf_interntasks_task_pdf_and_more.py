# Generated by Django 5.1.1 on 2024-11-06 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interns', '0017_feesintern_installment_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='internproject',
            name='project_pdf',
            field=models.FileField(default=1, upload_to='intern_projects/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='interntasks',
            name='task_pdf',
            field=models.FileField(default=1, upload_to='intern_taks/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feesintern',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 6, 21, 11, 6, 565393)),
        ),
    ]