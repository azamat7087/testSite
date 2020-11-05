# Generated by Django 3.1.2 on 2020-11-04 04:59

import azatAI.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azatAI', '0005_auto_20201103_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date_joined'),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(auto_now=True, verbose_name='last_login'),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='session_expire',
            field=models.DateTimeField(default=azatAI.models.get_deadline),
        ),
    ]