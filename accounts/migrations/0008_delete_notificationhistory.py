# Generated by Django 4.2.3 on 2023-09-25 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_notificationhistory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NotificationHistory',
        ),
    ]
