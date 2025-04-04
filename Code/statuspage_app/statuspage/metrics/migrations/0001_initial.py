# Generated by Django 4.1.2 on 2022-10-29 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('suffix', models.CharField(max_length=15)),
                ('visibility', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=1)),
                ('expand', models.CharField(choices=[('always', 'Expand Always'), ('on_click', 'Expand on Click')], default='on_click', max_length=255)),
            ],
            options={
                'ordering': ['order', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='MetricPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('value', models.FloatField()),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='metrics.metric')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
    ]
