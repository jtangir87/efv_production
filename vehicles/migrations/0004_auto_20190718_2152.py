# Generated by Django 2.1.8 on 2019-07-18 21:52

from django.db import migrations, models
import vehicles.models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_auto_20190703_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='damageimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=vehicles.models.update_filename),
        ),
    ]