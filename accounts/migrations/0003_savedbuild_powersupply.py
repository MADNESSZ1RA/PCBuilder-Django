# Generated by Django 5.2 on 2025-04-18 07:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_savedbuild_build_name'),
        ('main', '0004_powersupply'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedbuild',
            name='powersupply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.powersupply'),
        ),
    ]
