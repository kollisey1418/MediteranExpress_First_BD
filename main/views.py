# main/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import WarehouseItem
from .forms import WarehouseItemForm


def home(request):
    return render(request, 'main/home.html')


def garage(request):
    return render(request, 'main/garage.html')


def autopark(request):
    return render(request, 'main/autopark.html')


def warehouse_new(request):
    items = WarehouseItem.objects.all()
    form = WarehouseItemForm()  # Инициализируем форму
    return render(request, 'main/warehouse_new.html', {'items': items, 'form': form})


def add_item(request):
    if request.method == 'POST':
        try:
            print("POST request received")
            print("Request POST data:", request.POST)
            form = WarehouseItemForm(request.POST)
            if form.is_valid():
                print("Form is valid")
                part_number = form.cleaned_data['part_number']
                quantity = form.cleaned_data['quantity']
                print(f"Extracted part_number: {part_number}, quantity: {quantity}")

                item, created = WarehouseItem.objects.get_or_create(
                    part_number=part_number,
                    defaults={
                        'name': form.cleaned_data['name'],
                        'brand': form.cleaned_data['brand'],
                        'model': form.cleaned_data['model'],
                        'manufacturer': form.cleaned_data['manufacturer'],
                        'quantity': quantity,
                    }
                )
                if not created:
                    item.quantity += quantity
                    item.save()
                print(f"Saved item with part_number: {part_number}, quantity: {item.quantity}")
                return JsonResponse({'success': True})
            else:
                # Если форма не валидна из-за уникальности поля, попробуем обновить количество
                if 'part_number' in form.errors:
                    item = WarehouseItem.objects.get(part_number=form.data['part_number'])
                    item.quantity += int(form.data['quantity'])
                    item.save()
                    return JsonResponse({'success': True})
                else:
                    print("Form is not valid", form.errors)
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            print("Error occurred: ", str(e))
            return JsonResponse({'success': False, 'errors': str(e)})
    print("Invalid request method")
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})
