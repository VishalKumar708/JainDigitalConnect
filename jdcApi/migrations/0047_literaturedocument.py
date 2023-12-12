# Generated by Django 4.2.3 on 2023-12-08 09:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0046_livelocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiteratureDocument',
            fields=[
                ('isActive', models.BooleanField(default=False)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdBy', models.CharField(default=1, max_length=50)),
                ('updatedBy', models.CharField(default=1, max_length=50)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('link', models.TextField(null=True)),
                ('file', models.FileField(null=True, upload_to='literature_Documents', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt', 'pdf', 'doc', 'docx'])])),
                ('sectId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jdcApi.mstsect')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
