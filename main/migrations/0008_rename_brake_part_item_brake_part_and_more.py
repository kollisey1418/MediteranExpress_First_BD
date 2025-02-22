# Generated by Django 5.0.6 on 2024-06-03 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_brakeparts_carbodyparts_chassisparts_climateparts_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='Brake_part',
            new_name='brake_part',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='CarBodyParts_part',
            new_name='carbody_part',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Climate_part',
            new_name='climate_part',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Electricity_part',
            new_name='electricity_part',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Interior_part',
            new_name='interior_part',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Liquids_Parts',
            new_name='liquids_part',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Maintenance_part',
            new_name='maintenance_part',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='Steering_part',
            new_name='steering_part',
        ),
        migrations.AlterField(
            model_name='item',
            name='availability',
            field=models.CharField(default='green', max_length=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
