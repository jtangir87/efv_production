# Generated by Django 2.1.8 on 2019-08-05 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuellog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelentry',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
