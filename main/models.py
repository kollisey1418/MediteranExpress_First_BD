from django.db import models
from django.utils import timezone


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Car(models.Model):
    STATUS_CHOICES = [
        ('Исправен на линии', 'Исправен на линии'),
        ('Неисправен на линии', 'Неисправен на линии'),
        ('В ремонте', 'В ремонте'),
        ('Утиль', 'Утиль'),
    ]
    brand = models.CharField(max_length=100)  # Марка автомобиля
    model = models.CharField(max_length=100)  # Модель автомобиля
    vin_code = models.CharField(max_length=17, unique=True, primary_key=True)  # Вин-код
    engine_number = models.CharField(max_length=100)  # Номер двигателя
    engine_volume = models.DecimalField(max_digits=5, decimal_places=2)  # Объем двигателя
    year_of_manufacture = models.IntegerField()  # Год выпуска
    mileage = models.IntegerField(default=0)  # Пробег
    gearbox_type = models.CharField(max_length=50)  # Вид КПП
    state_number = models.CharField(max_length=20)  # Госномер
    status = models.CharField(max_length=50)  # Статус


    def __str__(self):
        return f"{self.brand} {self.model} ({self.vin_code})"

class WorkPerformed(models.Model):
    vin_code = models.ForeignKey(Car, on_delete=models.CASCADE)
    mileage = models.IntegerField()
    work_name = models.CharField(max_length=255)
    used_parts = models.CharField(max_length=255)
    quantity = models.IntegerField()
    article = models.CharField(max_length=255)
    part_manufacturer = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    executor = models.CharField(max_length=255, null=True, blank=True)

    from django.db import models

class Work(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    mileage = models.IntegerField()
    work_name = models.TextField()
    article = models.CharField(max_length=100, blank=True, null=True)
    part_name = models.CharField(max_length=100, blank=True, null=True)
    part_manufacturer = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.work_name} ({self.vin_code})"

class Recommendation(models.Model):
    date = models.DateField()  # Дата
    vin_code = models.ForeignKey(Car, on_delete=models.CASCADE)  # Вин-код
    recommendation = models.TextField()  # Рекомендации

    def __str__(self):
        return f"{self.date} - {self.recommendation}"

class DriverComplaint(models.Model):
    date = models.DateField()  # Дата
    vin_code = models.ForeignKey(Car, on_delete=models.CASCADE)  # Вин-код
    complaint_text = models.TextField()  # Текст жалобы

    def __str__(self):
        return f"{self.date} - {self.complaint_text}"

class Fault(models.Model):
    vin_code = models.ForeignKey(Car, on_delete=models.CASCADE)  # Вин-код
    description = models.CharField(max_length=255)  # Неисправность
    date = models.DateField(auto_now_add=True)  # Дата
    criticality = models.CharField(max_length=50)  # Критичность
    mileage = models.IntegerField()  # Пробег

    def __str__(self):
        return f"{self.date} - {self.description} ({self.criticality})"

class Model(models.Model):
    name = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

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
    article = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
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

    from django.db import models





class Mechanic(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

