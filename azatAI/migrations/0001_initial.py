# Generated by Django 3.1.2 on 2020-10-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=16)),
            ],
        ),
    ]