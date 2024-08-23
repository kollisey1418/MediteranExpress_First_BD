# main/views.py

import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import (Item, EngineParts, TransmissionParts, PneumaticParts, ChassisParts,
BrakeParts, SteeringParts, ElectricityParts, ClimateParts, CarBodyParts, InteriorParts, MaintenanceParts, LiquidsParts, Brand, Model, Car, WorkPerformed, Fault, Work)
from .forms import ItemForm, CarForm, WorkForm, FaultForm
from django.db.models import Q
from django.db import connection
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

NHTSA_API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesBatch/"
WorkFormSet = modelformset_factory(WorkPerformed, form=WorkForm, extra=1)
def get_car_info_by_vin(vin_code):
    try:
        response = requests.post(NHTSA_API_URL, data={'format': 'json', 'data': vin_code})
        response.raise_for_status()
        data = response.json().get('Results', [{}])[0]

        car_info = {
            'brand': data.get('Make', 'Unknown'),
            'model': data.get('Model', 'Unknown'),
            'mileage': 0,  # Замените на соответствующее поле, если есть
            'state_number': '',  # Замените на соответствующее поле, если есть
            'other_data': data.get('VehicleType', 'No additional information available')
        }
        return car_info
    except requests.RequestException as e:
        logger.error(f"Error fetching car data for VIN {vin_code}: {e}")
        return {
            'brand': 'Unknown',
            'model': 'Unknown',
            'mileage': 0,
            'state_number': '',
            'other_data': 'No additional information available'
        }

def work_detail(request, work_id):
    work = get_object_or_404(WorkPerformed, id=work_id)
    return render(request, 'main/work_detail.html', {'work': work})

def fault_detail(request, fault_id):
    fault = get_object_or_404(Fault, id=fault_id)
    return render(request, 'main/fault_detail.html', {'fault': fault})
def car_detail(request, vin_code):
    # Получаем объект автомобиля
    car = get_object_or_404(Car, vin_code=vin_code)

    # Генерируем имя таблицы на основе VIN-кода
    vin_code_table = f"work_{vin_code.replace('-', '_')}"

    # Извлекаем данные о работах из соответствующей таблицы
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT date, mileage, work_name, part_name, quantity, article FROM {vin_code_table}")
        work_records = cursor.fetchall()

    # Подготавливаем данные для шаблона
    context = {
        'car': car,
        'works': work_records,  # Передаем работы в шаблон
    }

    return render(request, 'main/car_detail.html', context)
def home(request):
    return render(request, 'main/home.html')

def garage(request):
    return render(request, 'main/garage.html')

def warehouse_new(request):
    sort_by = request.GET.get('sort_by', 'name')  # Default sorting by name
    order = request.GET.get('order', 'asc')  # Default order is ascending

    if order == 'desc':
        sort_by = '-' + sort_by

    items = Item.objects.all()

    # Фильтрация по бренду
    brand_name = request.GET.get('brand')
    if brand_name:
        items = items.filter(brand=brand_name)

    # Фильтрация по модели
    model_name = request.GET.get('model')
    if model_name:
        items = items.filter(model=model_name)

    # Фильтрация по типу запчасти
    part_type = request.GET.get('part_type')
    if part_type:
        items = items.filter(part_type=part_type)

    items = items.order_by(sort_by)

    brands = Brand.objects.all()
    models = Model.objects.all()

    context = {
        'items': items,
        'brands': brands,
        'models': models,
        'order': order,
    }
    return render(request, 'main/warehouse_new.html', context)

def autopark(request):
    cars = Car.objects.all()
    query = request.GET.get('q')
    if query:
        cars = cars.filter(
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(vin_code__icontains=query) |
            Q(state_number__icontains=query)
        )
    return render(request, 'main/autopark.html', {'cars': cars})


def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():

            car = form.save()

            vin_code_table = f"work_{car.vin_code.replace('-', '_')}"

            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {vin_code_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    mileage INTEGER NOT NULL,
                    work_name TEXT NOT NULL,
                    part_name TEXT,
                    quantity INTEGER,
                    article TEXT
                );
                """)
    else:
        form = CarForm()

    # Если запрос не POST, отображаем форму для добавления автомобиля
    return render(request, 'main/add_car.html', {'form': form})


def edit_car(request, vin_code):
    car = get_object_or_404(Car, vin_code=vin_code)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', vin_code=vin_code)
    else:
        form = CarForm(instance=car)
    return render(request, 'main/edit_car.html', {'form': form})


def add_work(request, vin_code):
    car = get_object_or_404(Car, vin_code=vin_code)
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            work_data = form.cleaned_data

            # Генерируем имя таблицы на основе VIN-кода автомобиля
            vin_code_table = f"work_{vin_code.replace('-', '_')}"

            # Вставляем данные в таблицу
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(f"""
                INSERT INTO {vin_code_table} (date, mileage, work_name, part_name, quantity, article)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, [
                    work_data['date'] if 'date' in work_data else timezone.now(),
                    work_data['mileage'],
                    work_data['work_name'],
                    work_data.get('part_name', ''),
                    work_data.get('quantity', 1),
                    work_data.get('article', '')
                ])

            return redirect('car_detail', vin_code=vin_code)
    else:
        form = WorkForm()
    return render(request, 'main/add_work.html', {'form': form, 'car': car, 'vin_code': vin_code})


def search_part(request):
    article = request.GET.get('article')
    try:
        part = Item.objects.get(article=article)
        data = {
            'part': {
                'name': part.name,
                'manufacturer': part.manufacturer,
            }
        }
    except Item.DoesNotExist:
        data = {'part': None}
    return JsonResponse(data)


def save_work(request, vin_code):
    if request.method == 'POST':
        car = get_object_or_404(Car, vin_code=vin_code)
        date = request.POST.get('date')
        mileage = request.POST.get('mileage')
        description = request.POST.get('description')
        part_article = request.POST.get('part_article')
        part_name = request.POST.get('part_name')
        part_manufacturer = request.POST.get('part_manufacturer')

        # Сохранение работы в основной таблице Work
        work = Work(
            car=car,
            date=date,
            mileage=mileage,
            description=description,
            part_article=part_article,
            part_name=part_name,
            part_manufacturer=part_manufacturer
        )
        work.save()

        # Генерация имени таблицы на основе VIN-кода
        vin_code_table = f"work_{vin_code.replace('-', '_')}"

        # Вставка данных в соответствующую таблицу на основе VIN-кода
        with connection.cursor() as cursor:
            cursor.execute(f"""
            INSERT INTO {vin_code_table} (date, mileage, work_name, part_name, quantity, article)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, [
                date,
                mileage,
                description,
                part_name,
                1,  # Если количество не указано, используем 1 по умолчанию
                part_article
            ])

        # Перенаправление на страницу с деталями автомобиля после сохранения работы
        return redirect('car_detail', vin_code=vin_code)

def add_fault(request, vin_code):
    car = get_object_or_404(Car, vin_code=vin_code)
    FaultFormSet = modelformset_factory(Fault, form=FaultForm, extra=1, can_delete=True)
    if request.method == 'POST':
        formset = FaultFormSet(request.POST, queryset=Fault.objects.none())
        if formset.is_valid():
            for form in formset:
                fault = form.save(commit=False)
                fault.vin_code = car
                fault.date = timezone.now()
                if fault.mileage < car.mileage:
                    form.add_error('mileage', 'Пробег не может быть меньше текущего пробега автомобиля.')
                else:
                    fault.save()
            return redirect('car_detail', vin_code=vin_code)
    else:
        formset = FaultFormSet(queryset=Fault.objects.none())
    return render(request, 'main/add_fault.html', {'formset': formset, 'car': car})
def add_item_form(request):
    form = ItemForm()
    brands = Brand.objects.all()
    models = Model.objects.all()
    return render(request, 'main/add_item_form.html', {'form': form, 'brands': brands, 'models': models})

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
            size = form.cleaned_data['size']
            quantity = form.cleaned_data['quantity']
            brand_id = form.cleaned_data['brand'].id
            model_id = form.cleaned_data['model'].id
            manufacturer = form.cleaned_data['manufacturer']
            part_type = form.cleaned_data['part_type']

            brand = Brand.objects.get(id=brand_id)
            model = Model.objects.get(id=model_id)

            try:
                item = Item.objects.get(article=article)
                logger.debug(f"Найдена существующая деталь с артикулом {article}")
                item.quantity += quantity
                item.save()
            except Item.DoesNotExist:
                try:
                    logger.debug("Создание нового объекта запчасти")
                    item = form.save(commit=False)
                    item.availability = 'green'  # Установите значение поля "Наличие" по умолчанию
                    item.brand = brand
                    item.model = model

                    # Создаем новый объект запчасти и соответствующий объект категории
                    if 'Топливная система' in part_type or 'Система охлаждения' in part_type or 'Выхлопная система' in part_type or 'Резиновые и иные уплотнения' in part_type or 'Детали двигателя' in part_type or 'Другое для двигателя' in part_type:
                        engine_part = EngineParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.engine_part = engine_part
                        logger.debug(f"Создан объект EngineParts: {engine_part}")

                    elif 'Коробка передач' in part_type or 'Карданный вал' in part_type or 'Редуктор' in part_type or 'Полуоси' in part_type or 'Ретардер' in part_type or 'Резиновые и иные уплотнения' in part_type or 'Другое для трансмиссии' in part_type:
                        transmission_part = TransmissionParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.transmission_part = transmission_part

                    elif 'Воздух для тормозов' in part_type or 'Воздух для подвески' in part_type or 'Воздух для дверей и салона' in part_type or 'Другое для пневмосистемы' in part_type:
                        pneumatic_part = PneumaticParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.pneumatic_part = pneumatic_part

                    elif 'Амортизаторы' in part_type or 'Пружины' in part_type or 'Рессоры' in part_type or 'Пневмоподушки' in part_type or 'Колесные диски' in part_type or 'Шины' in part_type or 'Шаровые опоры' in part_type or 'Тяги или рычаги' in part_type or 'Сайлентблоки' in part_type or 'Другое для ходовой части' in part_type:
                        chassis_parts = ChassisParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.chassis_parts = chassis_parts

                    elif 'Суппорта' in part_type or 'Колодки дисковые' in part_type or 'Колодки барабанные' in part_type or 'Колодки ручника' in part_type or 'Диски' in part_type or 'Барабаны' in part_type or 'Тросы' in part_type or 'Трубки' in part_type or 'Другое для тормозной системы' in part_type:
                        brake_parts = BrakeParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.brake_parts = brake_parts

                    elif 'Рулевая колонка' in part_type or 'Рулевые тяги' in part_type or 'Усилитель руля' in part_type or 'Другое для рулевого управления' in part_type:
                        steering_parts = SteeringParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.steering_parts = steering_parts

                    elif 'Генератор' in part_type or 'Стартер' in part_type or 'АКБ' in part_type or 'Проводка и разъемы' in part_type or 'Освещение' in part_type or 'Приборная панель и электроника управления' in part_type or 'Лампочки 24В' in part_type or 'Лампочки 12В' in part_type or 'Предохранители' in part_type or 'Другое для электрики' in part_type:
                        electricity_parts = ElectricityParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.electricity_parts = electricity_parts

                    elif 'Компрессор кондиционера' in part_type or 'Радиаторы' in part_type or 'Вентиляторы' in part_type or 'Трубки' in part_type or 'Фреон' in part_type or 'Другое для конд. и отоп.' in part_type:
                        climate_parts = ClimateParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.climate_parts = climate_parts

                    elif 'Каркас кузова' in part_type or 'Двери и окна' in part_type or 'Капот и багажные отсеки' in part_type or 'Зеркала' in part_type or 'Стеклоочистители' in part_type or 'Другое для кузова' in part_type:
                        car_body_parts = CarBodyParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.car_body_parts = car_body_parts

                    elif 'Сиденья' in part_type or 'Обивка и декоративные панели' in part_type or 'Пол и потолок' in part_type or 'Система безопасности' in part_type or 'Аудио- и видеосистемы' in part_type or 'Другое для салона' in part_type:
                        interior_parts = InteriorParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.interior_parts = interior_parts

                    elif 'Ремень генератора' in part_type or 'Ремень кондиционера' in part_type or 'Приводной ремень' in part_type or 'Фильтр топливный' in part_type or 'Фильтр масляный' in part_type or 'Фильтр воздушный' in part_type or 'Фильтр пневмосистемы' in part_type or 'Фильтр салона' in part_type or 'Иной фильтр' in part_type or 'Другое для ТО' in part_type:
                        maintenance_parts = MaintenanceParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.maintenance_parts = maintenance_parts

                    elif 'Моторное масло' in part_type or 'Трансмиссионное масло' in part_type or 'Тормозная жидкость' in part_type or 'Антифриз' in part_type or 'Омывающая жидкость' in part_type or 'Другие жидкости' in part_type:
                        liquids_parts = LiquidsParts.objects.create(
                            article=form.cleaned_data['article'],
                            name=form.cleaned_data['name'],
                            quantity=form.cleaned_data['quantity'],
                            brand=brand_id,
                            model=model_id,
                            manufacturer=form.cleaned_data['manufacturer'],
                            part_type=part_type
                        )
                        item.liquids_parts = liquids_parts

                    item.save()
                    logger.debug(f"Сохранена новая деталь: {item}")
                    return HttpResponse('<script>window.close();window.opener.location.reload();</script>')

                except Exception as e:
                    logger.error("Ошибка при сохранении новой детали: %s", e)
                    return HttpResponse(
                        '<script>alert("Ошибка при добавлении записи. Проверьте данные и попробуйте снова.");</script>')
            else:
                logger.error("Форма недействительна: %s", form.errors)
                return HttpResponse(
                        '<script>alert("Ошибка при добавлении записи. Проверьте данные и попробуйте снова.");</script>')

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
