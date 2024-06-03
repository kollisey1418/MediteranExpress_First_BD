from django.db import models

# Новые модели для категорий запчастей
class EngineParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TransmissionParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PneumaticParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ChassisParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BrakeParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SteeringParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ElectricityParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ClimateParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CarBodyParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class InteriorParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MaintenanceParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LiquidsParts(models.Model):
    availability = models.BooleanField(default=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    availability = models.CharField(max_length=10, default='green', blank=True)
    article = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    part_type = models.CharField(max_length=100)

    # Внешний ключ на соответствующую категорию
    engine_part = models.ForeignKey(EngineParts, on_delete=models.CASCADE, null=True, blank=True)
    transmission_part = models.ForeignKey(TransmissionParts, on_delete=models.CASCADE, null=True, blank=True)
    pneumatic_part = models.ForeignKey(PneumaticParts, on_delete=models.CASCADE, null=True, blank=True)
    chassis_parts = models.ForeignKey(ChassisParts, on_delete=models.CASCADE, null=True, blank=True)
    brake_part = models.ForeignKey(BrakeParts, on_delete=models.CASCADE, null=True, blank=True)
    steering_part = models.ForeignKey(SteeringParts, on_delete=models.CASCADE, null=True, blank=True)
    electricity_part = models.ForeignKey(ElectricityParts, on_delete=models.CASCADE, null=True, blank=True)
    climate_part = models.ForeignKey(ClimateParts, on_delete=models.CASCADE, null=True, blank=True)
    carbody_part = models.ForeignKey(CarBodyParts, on_delete=models.CASCADE, null=True, blank=True)
    interior_part = models.ForeignKey(InteriorParts, on_delete=models.CASCADE, null=True, blank=True)
    maintenance_part = models.ForeignKey(MaintenanceParts, on_delete=models.CASCADE, null=True, blank=True)
    liquids_part = models.ForeignKey(LiquidsParts, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.availability = 'red'
        elif self.quantity == 1:
            self.availability = 'yellow'
        else:
            self.availability = 'green'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
