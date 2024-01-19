# Generated by Django 4.2.3 on 2024-01-10 07:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterApi', '0004_alter_mstbloodgroup_createdby_and_more'),
        ('jdcApi', '0005_alter_aarti_createdby_alter_aarti_updatedby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='literaturedocument',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='literature_Documents', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt', 'pdf', 'jpeg', 'png'])]),
        ),
        migrations.AlterField(
            model_name='saint',
            name='sectId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_saint', to='masterApi.mstsect'),
        ),
    ]
