# Generated by Django 4.2.3 on 2023-12-11 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0050_appconfigurations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appconfigurations',
            name='configurationKey',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
