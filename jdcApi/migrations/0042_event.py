# Generated by Django 4.2.3 on 2023-12-02 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0041_dharamsthanmember_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('isActive', models.BooleanField(default=False)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdBy', models.CharField(default=1, max_length=50)),
                ('updatedBy', models.CharField(default=1, max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('isVerified', models.BooleanField(default=False)),
                ('cityId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jdcApi.city')),
                ('sectId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jdcApi.mstsect')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
