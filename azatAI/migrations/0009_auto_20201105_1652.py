# Generated by Django 3.1.2 on 2020-11-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azatAI', '0008_auto_20201105_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
    ]