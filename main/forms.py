# main/forms.py

from django import forms
from .models import Item, Brand, Model

class ItemForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label='Бренд')
    model = forms.ModelChoiceField(queryset=Model.objects.all(), label='Модель')
    class Meta:
        model = Item
        fields = ['article', 'name', 'size', 'quantity', 'brand', 'model', 'manufacturer', 'part_type']

    # brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=True)
    # model = forms.ModelChoiceField(queryset=Model.objects.all(), required=True)