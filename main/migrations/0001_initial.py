# Generated by Django 5.0.6 on 2024-05-22 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('location', models.CharField(max_length=255)),
                ('supplier', models.CharField(max_length=255)),
                ('date_received', models.DateField()),
            ],
        ),
    ]
