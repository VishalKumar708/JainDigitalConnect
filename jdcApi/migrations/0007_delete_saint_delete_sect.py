# Generated by Django 4.2.3 on 2023-10-30 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0006_alter_sect_sectname'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Saint',
        ),
        migrations.DeleteModel(
            name='Sect',
        ),
    ]
