# Generated by Django 2.2.6 on 2019-10-14 17:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_auto_20191014_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='day',
            field=models.DateField(default=datetime.date(2019, 10, 14)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='end_time',
            field=models.TimeField(default=datetime.time(12, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='start_time',
            field=models.TimeField(default=datetime.time(12, 0)),
            preserve_default=False,
        ),
    ]
