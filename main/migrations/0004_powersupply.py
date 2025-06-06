# Generated by Django 5.2 on 2025-04-18 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20250413_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='PowerSupply',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('efficiency', models.TextField(blank=True, null=True)),
                ('wattage', models.IntegerField(blank=True, null=True)),
                ('modular', models.TextField(blank=True, null=True)),
                ('color', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'power_supply',
                'managed': False,
            },
        ),
    ]
