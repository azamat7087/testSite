# Generated by Django 3.1.2 on 2020-11-03 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azatAI', '0004_auto_20201103_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_os',
            field=models.CharField(max_length=50),
        ),
    ]
