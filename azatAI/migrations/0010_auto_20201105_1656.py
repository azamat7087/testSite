# Generated by Django 3.1.2 on 2020-11-05 10:56

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('azatAI', '0009_auto_20201105_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, unique=True),
        ),
    ]