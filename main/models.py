# main/models.py

from django.db import models

class WarehouseItem(models.Model):
    part_number = models.CharField(max_length=255, unique=True)  # Артикул
    name = models.CharField(max_length=255)  # Название
    quantity = models.PositiveIntegerField()  # Количество
    brand = models.CharField(max_length=255)  # Марка
    model = models.CharField(max_length=255)  # Модель
    manufacturer = models.CharField(max_length=255)  # Производитель

    def __str__(self):
        return self.name
