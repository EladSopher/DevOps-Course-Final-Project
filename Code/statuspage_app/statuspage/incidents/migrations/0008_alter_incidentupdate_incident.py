# Generated by Django 4.1.2 on 2022-11-02 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0007_alter_incident_components'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentupdate',
            name='incident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='incidents.incident'),
        ),
    ]
