# Generated by Django 4.2.3 on 2023-11-17 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0021_mstrelation'),
    ]

    operations = [
        migrations.CreateModel(
            name='MstProfession',
            fields=[
                ('isActive', models.BooleanField(default=False)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdBy', models.CharField(default=1, max_length=50)),
                ('updatedBy', models.CharField(default=1, max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50, unique=True)),
                ('order', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]