# Generated by Django 4.2.3 on 2023-10-04 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jdcApi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('isActive', models.BooleanField(default=False)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdBy', models.CharField(default=1, max_length=50)),
                ('updatedBy', models.CharField(default=1, max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('businessId', models.AutoField(primary_key=True, serialize=False)),
                ('businessName', models.CharField(max_length=200)),
                ('businessType', models.CharField(max_length=120)),
                ('businessNumber', models.CharField(max_length=10, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('website', models.CharField(max_length=220, null=True)),
                ('businessDescription', models.TextField()),
                ('isVerified', models.BooleanField(default=False)),
                ('gstNumber', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=120)),
                ('cityId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='GetAllBusinessByCityId', to='jdcApi.city')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='GetAllBusinessByUserId', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
