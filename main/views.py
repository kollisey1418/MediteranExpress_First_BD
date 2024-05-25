# main/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm

def home(request):
    return render(request, 'main/home.html')

def garage(request):
    return render(request, 'main/garage.html')

def warehouse_new(request):
    items = Item.objects.all()
    return render(request, 'main/warehouse_new.html', {'items': items})

def autopark(request):
    return render(request, 'main/autopark.html')

def add_item_form(request):
    form = ItemForm()
    return render(request, 'main/add_item_form.html', {'form': form})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            part_number = form.cleaned_data['part_number']
            quantity = form.cleaned_data['quantity']
            try:
                item = Item.objects.get(part_number=part_number)
                item.quantity += quantity
                item.save()
            except Item.DoesNotExist:
                item = form.save(commit=False)
                item.availability = 'green'  # Установите значение поля "Наличие" по умолчанию
                item.save()
            return HttpResponse('<script>window.close();window.opener.location.reload();</script>')
        else:
            return HttpResponse('<script>alert("Ошибка при добавлении записи. Проверьте данные и попробуйте снова.");</script>')
    return HttpResponse('<script>alert("Некорректный метод запроса.");</script>')

def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('warehouse_new')
    else:
        form = ItemForm(instance=item)
    return render(request, 'main/edit_item.html', {'form': form})

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('warehouse_new')
