# main/models.py

from django.db import models

class Item(models.Model):
    part_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    availability = models.CharField(max_length=10)

    def __str__(self):
        return self.name
