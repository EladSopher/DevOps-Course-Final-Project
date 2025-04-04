# Generated by Django 4.2.1 on 2023-12-30 02:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0012_incidenttemplate"),
    ]

    operations = [
        migrations.AddField(
            model_name="incident",
            name="send_email",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="incidenttemplate",
            name="send_email",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="incidentupdate",
            name="send_email",
            field=models.BooleanField(default=True),
        ),
    ]
