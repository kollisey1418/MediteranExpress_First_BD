# main/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from .models import Car, WorkPerformed, Fault, Brand, Model, Item, Mechanic
from django.db import transaction

class CarForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Исправен на линии', 'Исправен на линии'),
        ('Неисправен на линии', 'Неисправен на линии'),
        ('В ремонте', 'В ремонте'),
        ('Утиль', 'Утиль'),
    ]

    vin_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'oninput': 'this.value = this.value.toUpperCase()'
        })
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Car
        fields = [
            'brand', 'model', 'vin_code', 'engine_number',
            'engine_volume', 'year_of_manufacture', 'mileage',
            'gearbox_type', 'state_number', 'status'
        ]

    def clean_year_of_manufacture(self):
        year = self.cleaned_data['year_of_manufacture']
        if year < 1886 or year > 2024:
            raise ValidationError('Недопустимый год выпуска.')
        return year

    def clean_mileage(self):
        mileage = self.cleaned_data['mileage']
        if mileage < 0:
            raise ValidationError('Пробег не может быть отрицательным.')
        return mileage

class WorkForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    

    class Meta:
        model = WorkPerformed
        fields = ['date','mileage', 'work_name', 'used_parts', 'quantity', 'article', 'part_manufacturer']

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)
        super(WorkForm, self).__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise ValidationError('Количество должно быть положительным.')
        return quantity

    def clean_mileage(self):
        mileage = self.cleaned_data['mileage']
        if self.car and mileage < self.car.mileage:
            raise ValidationError('Пробег не может быть меньше текущего пробега автомобиля.')
        return mileage

    @transaction.atomic
    def save(self, commit=True):
        instance = super(WorkForm, self).save(commit=False)

        # Снижение количества запчастей на складе
        part_article = self.cleaned_data.get('article')
        if part_article:
            try:
                part = Item.objects.get(article=part_article)
                if part.quantity > 0:
                    part.quantity -= 1
                    part.save()
                else:
                    raise ValidationError('Недостаточное количество запчастей на складе.')
            except Item.DoesNotExist:
                raise ValidationError('Запчасть не найдена на складе.')

        if commit:
            instance.save()
        return instance

class FaultForm(forms.ModelForm):
    CRITICALITY_CHOICES = [
        ('Низкая', 'Низкая'),
        ('Средняя', 'Средняя'),
        ('Высокая', 'Высокая'),
    ]

    criticality = forms.ChoiceField(choices=CRITICALITY_CHOICES)

    class Meta:
        model = Fault
        fields = ['description', 'criticality', 'mileage']

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)
        super(FaultForm, self).__init__(*args, **kwargs)

    def clean_mileage(self):
        mileage = self.cleaned_data['mileage']
        if self.car and mileage < self.car.mileage:
            raise ValidationError('Пробег не может быть меньше текущего пробега автомобиля.')
        if mileage < 0:
            raise ValidationError('Пробег не может быть отрицательным.')
        return mileage

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 5 or len(description) > 50:
            raise ValidationError('Описание неисправности должно содержать от 5 до 50 символов.')
        return description

class ItemForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label='Бренд')
    model = forms.ModelChoiceField(queryset=Model.objects.all(), label='Модель')

    class Meta:
        model = Item
        fields = ['article', 'name', 'size', 'quantity', 'brand', 'model', 'manufacturer', 'part_type']








class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['first_name', 'last_name']

class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')
    group = forms.ChoiceField(choices=[
        ('Водители', 'Водители'),
        ('Механики', 'Механики'),
        ('Администраторы', 'Администраторы')
    ], label='Группа')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password1', 'password2', 'group']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        return password2

    def clean_group(self):
        group = self.cleaned_data.get('group')
        if not group:
            raise ValidationError('Необходимо выбрать группу.')
        return group