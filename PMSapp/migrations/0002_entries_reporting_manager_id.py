# Generated by Django 4.1.2 on 2022-11-09 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PMSapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entries',
            name='Reporting_manager_id',
            field=models.CharField(default='1', max_length=100),
        ),
    ]
