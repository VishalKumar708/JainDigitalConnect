# Generated by Django 4.2.3 on 2023-11-28 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0030_rename_literatureid_literature_id_literature_sectid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='literature',
            name='sectId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jdcApi.mstsect'),
        ),
    ]