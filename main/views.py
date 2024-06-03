# main/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import (Item, EngineParts, TransmissionParts, PneumaticParts, ChassisParts,
BrakeParts, SteeringParts, ElectricityParts, ClimateParts, CarBodyParts, InteriorParts, MaintenanceParts, LiquidsParts)
from .forms import ItemForm
import logging

logger = logging.getLogger(__name__)

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
    logger.debug(f"Метод запроса: {request.method}")

    if request.method == 'POST':
        logger.debug("Начало обработки POST запроса для добавления новой детали")
        logger.debug(f"Данные запроса: {request.POST}")

        form = ItemForm(request.POST)
        logger.debug(f"Данные формы: {request.POST}")

        if form.is_valid():
            logger.debug("Форма валидна")
            article = form.cleaned_data['article']
            name = form.cleaned_data['name']
            quantity = form.cleaned_data['quantity']
            brand = form.cleaned_data['brand']
            model = form.cleaned_data['model']
            manufacturer = form.cleaned_data['manufacturer']
            part_type = form.cleaned_data['part_type']

            try:
                item = Item.objects.get(article=form.cleaned_data['article'])
                logger.debug(f"Найдена существующая деталь с артикулом {article}")
                item.quantity += quantity
                item.save()
            except Item.DoesNotExist:
                try:
                    logger.debug("Создание нового объекта запчасти")
                    item = form.save(commit=False)
                    item.availability = 'green'  # Установите значение поля "Наличие" по умолчанию

                    # Создаем новый объект запчасти и соответствующий объект категории
                    if 'Топливная система' in part_type or 'Система охлаждения' in part_type or 'Выхлопная система' in part_type or 'Резиновые и иные уплотнения' in part_type or 'Детали двигателя' in part_type or 'Другое для двигателя' in part_type:
                        engine_part = EngineParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.engine_part = engine_part
                        logger.debug(f"Создан объект EngineParts: {engine_part}")

                    elif 'Коробка передач' in part_type or 'Карданный вал' in part_type or 'Редуктор' in part_type or 'Полуоси' in part_type or 'Ретардер' in part_type or 'Резиновые и иные уплотнения' in part_type or 'Дугое для трансмиссии' in part_type:
                        transmission_part = TransmissionParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.transmission_part = transmission_part

                    elif 'Воздух для тормозов' in part_type or 'Воздух для подвески' in part_type or 'Воздух для дверей и салона' in part_type or 'Другое для пневмосистемы' in part_type:
                        pneumatic_part = PneumaticParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.pneumatic_part = pneumatic_part

                    elif 'Амортизаторы' in part_type or 'Пружины' in part_type or 'Рессоры' in part_type or 'Пневмоподушки' in part_type or 'Колесные диски' in part_type or 'Шины' in part_type or 'Шаровые опоры' in part_type or 'Тяги или рычаги' in part_type or 'Сайлентблоки' in part_type or 'Другое для ходовой части' in part_type:
                        chassis_parts = ChassisParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.chassis_parts = chassis_parts

                    elif 'Суппорта' in part_type or 'Колодки дисковые' in part_type or 'Колодки барабанные' in part_type or 'Колодки ручника' in part_type or 'Диски' in part_type or 'Барабаны' in part_type or 'Тросы' in part_type or 'Трубки' in part_type or 'Другое для тормозной системы' in part_type:
                        brake_parts = BrakeParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.brake_parts = brake_parts

                    elif 'Рулевая колонка' in part_type or 'Рулевые тяги' in part_type or 'Усилитель руля' in part_type or 'Другое для для рулевого управления' in part_type:
                        steering_parts = SteeringParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.steering_parts = steering_parts

                    elif 'Генератор' in part_type or 'Стартер' in part_type or 'АКБ' in part_type or 'Проводка и разъемы' in part_type or 'Освещение' in part_type or 'Приборная панель и электроника управления' in part_type or 'Лампочки 24В' in part_type or 'Лампочки 12В' in part_type or 'Предохранители' in part_type or 'Другое для для электрики' in part_type:
                        electricity_parts = ElectricityParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.electricity_parts = electricity_parts

                    elif 'Компрессор кондиционера' in part_type or 'Радиаторы' in part_type or 'Вентиляторы' in part_type or 'Трубки' in part_type or 'Фрион' in part_type or 'Другое для конд. и отоп.' in part_type:
                        climate_parts = ClimateParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.climate_parts = climate_parts

                    elif 'Каркас кузова' in part_type or 'Двери и окна' in part_type or 'Капот и багажные отсеки' in part_type or 'Зеркала' in part_type or 'Стеклоочистители' in part_type or 'Другое для кузова' in part_type:
                        car_body_parts = CarBodyParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.car_body_parts = car_body_parts

                    elif 'Сиденья' in part_type or 'Обивка и декоративные панели' in part_type or 'Пол и потолок' in part_type or 'Система безопасности' in part_type or 'Аудио- и видеосистемы' in part_type or 'Другое для салона' or part_type:
                        interior_parts = InteriorParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.interior_parts = interior_parts

                    elif 'Ремень генератора' in part_type or 'Ремень кондиционера' in part_type or 'Приводной ремень' in part_type or 'Фильтр топливный' in part_type or 'Фильтр масляный' in part_type or 'Фильтр воздушный' in part_type or 'Фильтр пневмосистемы' in part_type or 'Фильтр салона' in part_type or 'Иной фильтр' in part_type or 'Другое для ТО' in part_type:
                        maintenance_parts = MaintenanceParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.maintenance_parts = maintenance_parts

                    elif 'Моторное масло' in part_type or 'Трансмиссионное масло' in part_type or 'Тормозная жидкость' in part_type or 'Антифриз' in part_type or 'Омывающая жидкость' in part_type or 'Другие жидкости' in part_type:
                        liquids_parts = LiquidsParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=form.cleaned_data['brand'],
                            model=form.cleaned_data['model'],
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.liquids_parts = liquids_parts

                    item.save()
                    logger.debug(f"Сохранена новая деталь: {item}")
                    return HttpResponse('<script>window.close();window.opener.location.reload();</script>')

                except Exception as e:
                    logger.error("Ошибка при сохранении новой детали: %s", e)
                    return HttpResponse('<script>alert("Ошибка при добавлении записи. Проверьте данные и попробуйте снова.");</script>')
        else:
            logger.error("Форма недействительна: %s", form.errors)
            return HttpResponse('<script>alert("Ошибка при добавлении записи. Проверьте данные и попробуйте снова.");</script>')

    else:
        logger.error("Некорректный метод запроса")
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
