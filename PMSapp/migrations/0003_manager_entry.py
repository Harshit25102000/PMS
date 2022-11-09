# Generated by Django 4.1.2 on 2022-11-09 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PMSapp', '0002_entries_reporting_manager_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='manager_entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_id', models.CharField(max_length=100, unique=True)),
                ('First_name', models.CharField(max_length=100)),
                ('Middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('Last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('Email_id', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]