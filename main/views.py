# main/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import WarehouseItem
from .forms import WarehouseItemForm
from django.views.decorators.csrf import csrf_exempt
import json

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
        form = WarehouseItemForm(request.POST)
        if form.is_valid():
            part_number = form.cleaned_data['part_number']
            quantity = form.cleaned_data['quantity']
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
            return JsonResponse({'success': True})
        else:
            if 'part_number' in form.errors:
                item = WarehouseItem.objects.get(part_number=form.data['part_number'])
                item.quantity += int(form.data['quantity'])
                item.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

@csrf_exempt
def delete_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = WarehouseItem.objects.get(id=data['id'])
            item.delete()
            return JsonResponse({'success': True})
        except WarehouseItem.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'Item does not exist'})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

@csrf_exempt
def edit_item(request):
    if request.method == 'POST':
        try:
            data = request.POST
            item = WarehouseItem.objects.get(id=data['id'])
            form = WarehouseItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        except WarehouseItem.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'Item does not exist'})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})
