# Generated by Django 4.2.3 on 2024-01-01 13:50

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_createdby_alter_user_updatedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phoneNumber',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]