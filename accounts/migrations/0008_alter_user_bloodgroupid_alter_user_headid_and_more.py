# Generated by Django 4.2.3 on 2024-01-04 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterApi', '0004_alter_mstbloodgroup_createdby_and_more'),
        ('accounts', '0007_alter_user_bloodgroupid_alter_user_createdby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bloodGroupId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterApi.mstbloodgroup'),
        ),
        migrations.AlterField(
            model_name='user',
            name='headId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='family_members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='maritalStatusId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterApi.mstmaritalstatus'),
        ),
        migrations.AlterField(
            model_name='user',
            name='professionId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterApi.mstprofession'),
        ),
        migrations.AlterField(
            model_name='user',
            name='relationId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterApi.mstrelation'),
        ),
    ]