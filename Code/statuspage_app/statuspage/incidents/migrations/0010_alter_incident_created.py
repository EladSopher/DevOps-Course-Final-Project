# Generated by Django 4.1.7 on 2023-03-10 14:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0009_alter_incidentupdate_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
