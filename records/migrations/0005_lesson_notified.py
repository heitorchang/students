# Generated by Django 2.2.1 on 2019-10-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_auto_20191009_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='notified',
            field=models.BooleanField(default=False),
        ),
    ]
