# Generated by Django 5.0.6 on 2024-05-22 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouseitem',
            name='date_received',
        ),
        migrations.RemoveField(
            model_name='warehouseitem',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='warehouseitem',
            name='location',
        ),
        migrations.RemoveField(
            model_name='warehouseitem',
            name='supplier',
        ),
        migrations.AddField(
            model_name='warehouseitem',
            name='brand',
            field=models.CharField(default='Unknown', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouseitem',
            name='manufacturer',
            field=models.CharField(default='Unknown', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouseitem',
            name='model',
            field=models.CharField(default='Unknown', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouseitem',
            name='name',
            field=models.CharField(default='Unknown', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouseitem',
            name='part_number',
            field=models.CharField(default='Unknown', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='warehouseitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
