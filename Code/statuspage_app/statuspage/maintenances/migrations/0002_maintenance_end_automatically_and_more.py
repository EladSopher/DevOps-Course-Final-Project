# Generated by Django 4.1.2 on 2022-10-27 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance',
            name='end_automatically',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='start_automatically',
            field=models.BooleanField(default=True),
        ),
    ]
