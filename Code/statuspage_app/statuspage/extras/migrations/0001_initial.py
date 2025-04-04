# Generated by Django 4.1.2 on 2022-10-19 21:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user_name', models.CharField(editable=False, max_length=150)),
                ('request_id', models.UUIDField(editable=False)),
                ('action', models.CharField(choices=[('create', 'Created'), ('update', 'Updated'), ('delete', 'Deleted')], max_length=50)),
                ('changed_object_id', models.PositiveBigIntegerField()),
                ('related_object_id', models.PositiveBigIntegerField(blank=True, null=True)),
                ('object_repr', models.CharField(editable=False, max_length=200)),
                ('prechange_data', models.JSONField(blank=True, editable=False, null=True)),
                ('postchange_data', models.JSONField(blank=True, editable=False, null=True)),
                ('changed_object_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='contenttypes.contenttype')),
                ('related_object_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='changes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
