# Generated by Django 4.1.2 on 2022-10-26 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0002_alter_component_options'),
        ('incidents', '0006_alter_incident_components'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='components',
            field=models.ManyToManyField(blank=True, related_name='incidents', to='components.component'),
        ),
    ]
