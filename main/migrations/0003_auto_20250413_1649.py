# Generated by Django 3.2.25 on 2025-04-13 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_formfactor_socket'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FormFactor',
        ),
        migrations.DeleteModel(
            name='Socket',
        ),
    ]
