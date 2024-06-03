# main/forms.py

from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['article', 'name', 'quantity', 'brand', 'model', 'manufacturer', 'part_type']  # Убедитесь, что здесь нет поля 'part_number'
