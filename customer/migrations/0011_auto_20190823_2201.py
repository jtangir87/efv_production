# Generated by Django 2.1.11 on 2019-08-23 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_auto_20190823_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingprofile',
            name='brand',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='billingprofile',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='billingprofile',
            name='last_4',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='billingprofile',
            name='name_on_card',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='billingprofile',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='billingprofile',
            name='street_one',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='billingprofile',
            name='street_two',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='billingprofile',
            name='zip',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]