# Generated by Django 2.1.11 on 2019-08-24 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20190823_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='next_payment',
            field=models.DateField(blank=True, null=True),
        ),
    ]