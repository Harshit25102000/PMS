# Generated by Django 4.1.2 on 2022-10-31 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PMSapp', '0009_comments_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='receiver_name',
            field=models.CharField(default='Anonymous', max_length=100),
        ),
        migrations.AddField(
            model_name='comments',
            name='sender_name',
            field=models.CharField(default='Anonymous', max_length=100),
        ),
    ]
