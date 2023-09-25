# Generated by Django 4.2.3 on 2023-09-25 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_notification_delete_notificationhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isActive', models.BooleanField(default=True)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdBy', models.CharField(default=1, max_length=50)),
                ('updatedBy', models.CharField(default=1, max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('notificationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_history', to='accounts.notification')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
