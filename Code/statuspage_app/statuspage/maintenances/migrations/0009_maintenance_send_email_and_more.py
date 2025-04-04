# Generated by Django 4.2.1 on 2023-12-30 02:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("maintenances", "0008_maintenancetemplate_end_automatically_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="maintenance",
            name="send_email",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="maintenancetemplate",
            name="send_email",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="maintenanceupdate",
            name="send_email",
            field=models.BooleanField(default=True),
        ),
    ]
