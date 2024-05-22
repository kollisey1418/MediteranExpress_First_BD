# main/forms.py

from django import forms
from .models import WarehouseItem

class WarehouseItemForm(forms.ModelForm):
    class Meta:
        model = WarehouseItem
        fields = ['part_number', 'name', 'quantity', 'brand', 'model', 'manufacturer']
        widgets = {
            'part_number': forms.TextInput(attrs={'required': True}),
            'name': forms.TextInput(attrs={'required': True}),
            'quantity': forms.NumberInput(attrs={'required': True}),
            'brand': forms.TextInput(attrs={'required': True}),
            'model': forms.TextInput(attrs={'required': True}),
            'manufacturer': forms.TextInput(attrs={'required': True}),
        }
