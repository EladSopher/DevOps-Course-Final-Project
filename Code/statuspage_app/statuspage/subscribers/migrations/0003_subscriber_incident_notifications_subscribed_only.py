# Generated by Django 4.1.7 on 2023-03-20 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0002_alter_subscriber_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='incident_notifications_subscribed_only',
            field=models.BooleanField(default=False),
        ),
    ]
