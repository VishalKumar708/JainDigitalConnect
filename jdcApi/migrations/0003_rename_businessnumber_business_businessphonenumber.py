# Generated by Django 4.2.3 on 2023-10-04 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0002_business'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='businessNumber',
            new_name='businessPhoneNumber',
        ),
    ]
