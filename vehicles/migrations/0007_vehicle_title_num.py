# Generated by Django 2.2.24 on 2022-01-04 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0006_auto_20190730_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='title_num',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Title #'),
        ),
    ]
