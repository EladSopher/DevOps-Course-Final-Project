# Generated by Django 4.1.2 on 2022-10-25 22:47

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('enabled', models.BooleanField(default=True)),
                ('actions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), help_text='The list of actions granted by this permission', size=None)),
                ('constraints', models.JSONField(blank=True, help_text='Queryset filter matching the applicable objects of the selected type(s)', null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='object_permissions', to='auth.group')),
                ('object_types', models.ManyToManyField(limit_choices_to=models.Q(models.Q(models.Q(('app_label__in', ['admin', 'auth', 'contenttypes', 'sessions', 'taggit', 'users']), _negated=True), models.Q(('app_label', 'auth'), ('model__in', ['group', 'user'])), models.Q(('app_label', 'users'), ('model__in', ['objectpermission', 'token'])), _connector='OR')), related_name='object_permissions', to='contenttypes.contenttype')),
                ('users', models.ManyToManyField(blank=True, related_name='object_permissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'permission',
                'ordering': ['name'],
            },
        ),
    ]
