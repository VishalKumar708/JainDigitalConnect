# Generated by Django 4.2.3 on 2024-01-02 10:59

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0003_alter_aarti_createdby_alter_aarti_updatedby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='areaContactNumber',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='business',
            name='businessPhoneNumber',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='dharamsthanmember',
            name='phoneNumber',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='livelocation',
            name='phoneNumber1',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='livelocation',
            name='phoneNumber2',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]