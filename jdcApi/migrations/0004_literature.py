# Generated by Django 4.2.3 on 2023-10-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0003_rename_businessnumber_business_businessphonenumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Literature',
            fields=[
                ('isActive', models.BooleanField(default=False)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdBy', models.CharField(default=1, max_length=50)),
                ('updatedBy', models.CharField(default=1, max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('literatureId', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('order', models.IntegerField()),
                ('isVerified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
