# Generated by Django 2.1.8 on 2019-08-05 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20190805_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
