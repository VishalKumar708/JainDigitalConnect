# Generated by Django 4.2.3 on 2023-11-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdcApi', '0016_alter_mstbloodgroup_bloodgroupname'),
    ]

    operations = [
        migrations.AddField(
            model_name='mstbloodgroup',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]