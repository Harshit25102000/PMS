# Generated by Django 4.1.2 on 2022-11-05 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PMSapp', '0012_alter_comments_receiver_alter_comments_review_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='self_appraisals',
            name='application',
            field=models.CharField(default='Empty...', max_length=50000),
        ),
    ]