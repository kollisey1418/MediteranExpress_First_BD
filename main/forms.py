# main/forms.py

from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['part_number', 'name', 'quantity', 'brand', 'model', 'manufacturer']
