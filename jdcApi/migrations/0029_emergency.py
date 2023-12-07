# Generated by Django 4.2.3 on 2023-11-27 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0028_alter_business_address_alter_business_gstnumber_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emergency',
            fields=[
                ('isActive', models.BooleanField(default=False)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdBy', models.CharField(default=1, max_length=50)),
                ('updatedBy', models.CharField(default=1, max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('departmentName', models.CharField(max_length=30)),
                ('phoneNumber', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('isVerified', models.BooleanField(default=False)),
                ('cityId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='jdcApi.city')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]