# Generated by Django 4.2.3 on 2023-12-27 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0053_feedbacktitle_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='feedBackTitleId',
            new_name='feedbackTitleId',
        ),
    ]
