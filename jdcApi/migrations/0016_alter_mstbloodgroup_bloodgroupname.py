# Generated by Django 4.2.3 on 2023-11-16 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0015_mstbloodgroup_mstdoctor_mstmaritalstatus_mstrelation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mstbloodgroup',
            name='bloodGroupName',
            field=models.CharField(max_length=7, unique=True),
        ),
    ]