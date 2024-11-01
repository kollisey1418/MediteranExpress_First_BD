# main/views.py

import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import (Item, EngineParts, TransmissionParts, PneumaticParts, ChassisParts,
BrakeParts, SteeringParts, ElectricityParts, ClimateParts, CarBodyParts, InteriorParts, MaintenanceParts,
LiquidsParts, Brand, Model, Car, Fault, Mechanic)
from .forms import ItemForm, CarForm, WorkForm, FaultForm, MechanicForm
from django.db.models import Q
from django.db import connection
from django.forms import modelformset_factory
from .models import WorkPerformed
from django.contrib import messages
import logging
import random

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from .forms import RegisterUserForm
from datetime import datetime



# Представление для регистрации нового пользователя
# Представление для регистрации нового пользователя
@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data.get('group')
            prefix = ''
            if group_name == 'Водители':
                prefix = 'driver'
            elif group_name == 'Механики':
                prefix = 'mechanic'
            elif group_name == 'Администраторы':
                prefix = 'admin'

            while True:
                username = f"{prefix}{random.randint(1000, 9999)}"
                if not User.objects.filter(username=username).exists():
                    break

            # Создание пользователя
            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data.get('password1'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name')
            )
            user.is_active = True
            user.save()

            # Добавление пользователя в группу в зависимости от выбранной роли
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                messages.error(request, f'Группа "{group_name}" не найдена. Обратитесь к администратору.')
                user.delete()
                return render(request, 'main/register.html', {'form': form})

            messages.success(request,
                             f'Пользователь "{username}" успешно зарегистрирован и добавлен в группу "{group_name}".')
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'main/register.html', {'form': form})


# Ограничение доступа по ролям
@login_required
def restricted_view(request):
    if request.user.groups.filter(name='Механики').exists():
        # Доступ для механиков
        return render(request, 'main/mechanic_view.html')
    elif request.user.groups.filter(name='Водители').exists():
        # Доступ для водителей (только просмотр)
        return render(request, 'main/driver_view.html')
    elif request.user.is_superuser:
        # Доступ для администратора
        return render(request, 'main/admin_view.html')
    else:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('home')

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

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Механики').exists() or u.is_superuser)

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
        cursor.execute(f"SELECT date, mileage, work_name, used_parts, quantity, article, executor FROM {vin_code_table}")
        work_records = cursor.fetchall()



    # Подготавливаем данные для шаблона
    context = {
        'car': car,
        'works': work_records,  # Передаем работы в шаблон
    }

    return render(request, 'main/car_detail.html', context)
def home(request):
    return render(request, 'main/home.html')

def autopark_main(request):
    return render(request, 'main/autopark_main.html')

def drivers(request):
    return render(request, 'main/drivers.html')

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
            try:
                car = form.save()
                vin_code_table = f"work_{car.vin_code.replace('-', '_')}"

                # Создаем таблицу, если её не существует
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {vin_code_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        mileage INTEGER NOT NULL,
                        work_name TEXT NOT NULL,
                        used_parts TEXT,
                        quantity INTEGER,
                        article TEXT,
                        executor TEXT
                    );
                    """)
                messages.success(request, 'Автомобиль успешно добавлен.')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении автомобиля: {e}')
                print(f"Ошибка при сохранении автомобиля: {e}")
        else:
            messages.error(request, 'Форма заполнена некорректно.')
            print(f"Ошибки формы: {form.errors}")

    else:
        form = CarForm()

    return render(request, 'main/add_car.html', {'form': form})


def edit_car(request, vin_code):
    car = get_object_or_404(Car, vin_code=vin_code)
    if request.method == 'POST':
        print("POST-запрос успешно получен")
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', vin_code=vin_code)
    else:
        print(f"Метод запроса: {request.method}")
        form = CarForm(instance=car)
    return render(request, 'main/edit_car.html', {'form': form})


from django.utils import timezone


def save_work_or_add(request, vin_code):
    print("Функция save_work_or_add вызвана")
    # Получаем объект автомобиля
    car = get_object_or_404(Car, vin_code=vin_code)

    if request.method == 'POST':
        print(f"POST данные: {request.POST}")
        # Получаем списки данных из формы
        dates = request.POST.getlist('date')
        mileages = request.POST.getlist('mileage')
        work_names = request.POST.getlist('work_name[]')
        used_parts = request.POST.getlist('used_parts[]')
        quantities = request.POST.getlist('quantity[]')
        articles = request.POST.getlist('article[]')
        print(f"work_names: {work_names}")
        print(f"mileages: {mileages}")

        # Получаем дату и пробег из основной формы
        date = request.POST.get('date')
        mileage = request.POST.get('mileage')

        mileage = int(mileage)  # Преобразуем строку в целое число

        # Если дата пустая, используем текущую дату и время с временной зоной
        if not date or date == '':
            date = timezone.now()  # Используем текущую дату и время
        else:
            # Преобразуем дату в формат datetime и учитываем временную зону
            date = timezone.make_aware(timezone.datetime.strptime(date, "%Y-%m-%d"), timezone.get_current_timezone())
            # Добавляем текущее время к указанной дате
            now = timezone.now()
            date = date.replace(hour=now.hour, minute=now.minute, second=now.second)

    print(f"Длина work_names: {len(work_names)}")
    print(f"Длина part_names: {len(used_parts)}")
    print(f"Длина quantities: {len(quantities)}")
    print(f"Длина articles: {len(articles)}")


    if len(work_names) == len(used_parts) == len(quantities) == len(articles):

        vin_code_table = f"work_{vin_code.replace('-', '_')}"

        try:
            # Перебираем все записи и сохраняем каждую по отдельности
            with connection.cursor() as cursor:
                for i in range(len(work_names)):
                    print(f"Сохраняемые данные: {work_names[i]}, {mileages}, {used_parts[i]}, {quantities[i]}, {articles[i]},")

                    # Получаем исполнителя
                    executor = f"{request.user.first_name} {request.user.last_name}"

                performed_work = WorkPerformed(
                    vin_code=car,
                    date=date,
                    mileage=mileage,
                    work_name=work_names[i],
                    used_parts=used_parts[i],
                    quantity=quantities[i],
                    article=articles[i],
                    executor = executor
                )
                # Вывод всех списков для проверки
                print(f"work_names: {work_names}")
                print(f"mileages: {mileages}")
                print(f"used_parts: {used_parts}")
                print(f"quantities: {quantities}")
                print(f"articles: {articles}")



                performed_work.save()  # Сохраняем каждую запись в performed_work
                print(f"WorkPerformed сохранено: {performed_work}")

                if not date or date == '':
                    date = timezone.now()  # Используем текущую дату и время
                else:
                    # Преобразуем дату в объект datetime
                    if isinstance(date, str):
                        date = datetime.strptime(date, "%Y-%m-%d")
                    # Преобразуем в строку нужного формата и добавляем текущее время
                    now = timezone.now()
                    date = date.replace(hour=now.hour, minute=now.minute, second=now.second)
                    date = date.strftime("%Y-%m-%d %H:%M:%S")

                # Сохранение в динамическую таблицу
                sql_query = f"""
                                           INSERT INTO {vin_code_table} (date, mileage, work_name, used_parts, quantity, article, executor)
                                           VALUES (%s, %s, %s, %s, %s, %s, %s)
                                       """
                cursor.execute(sql_query,
                               (date, mileage, work_names[i], used_parts[i], quantities[i], articles[i], executor))
                print("Запись успешно сохранена в таблицу:", vin_code_table)

        except Exception as e:
            print(f"Ошибка при сохранении в WorkPerformed: {e}")
            return render(request, 'main/car_detail.html', {'form': None, 'car': car, 'vin_code': vin_code})

        # Перенаправление на страницу деталей автомобиля
        return redirect('car_detail', vin_code=vin_code)

    else:
        print("Длины списков не совпадают!")
        form = WorkForm()

    # Возврат шаблона с формой для добавления работы
    return render(request, 'main/car_detail.html', {'form': form, 'car': car, 'vin_code': vin_code})


#поиск запчастей
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

#неисправности
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


def mechanics_list(request):
    # Фильтрация пользователей, которые принадлежат группе "Механики"
    mechanics_group = Group.objects.get(name='Механики')
    mechanics = User.objects.filter(groups=mechanics_group)

    return render(request, 'main/mechanics.html', {'mechanics': mechanics})


def drivers(request):
    # Фильтрация пользователей, которые принадлежат группе "Водители"
    drivers_group = Group.objects.get(name='Водители')
    drivers = User.objects.filter(groups=drivers_group)

    return render(request, 'main/drivers.html', {'drivers': drivers})

def add_mechanic(request):
    if request.method == 'POST':
        form = MechanicForm(request.POST)
        if form.is_valid():
            mechanic = form.save()  # Сохраняем нового механика в БД
            table_name = f"{mechanic.first_name}_{mechanic.last_name}_{mechanic.id}".replace(' ', '_')

            # Создаем новую таблицу в БД для механика
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    CREATE TABLE {table_name} (
                        id SERIAL PRIMARY KEY,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        state_number VARCHAR(20),
                        work_name VARCHAR(255)
                    )
                """)
            return JsonResponse({'success': True, 'message': 'Механик успешно добавлен!'})

        return JsonResponse({'success': False, 'message': 'Некорректные данные формы.'}, status=400)
    else:
        form = MechanicForm()
    return render(request, 'main/add_mechanic.html', {'form': form})

@login_required
def mechanic_detail(request, pk):
    mechanic = get_object_or_404(Mechanic, pk=pk)
    table_name = f"{mechanic.first_name}_{mechanic.last_name}_{mechanic.id}".replace(' ', '_')



    # Извлечение данных из таблицы механика
    try:
        with connection.cursor() as cursor:
            # Проверка, существует ли таблица
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            table_exists = cursor.fetchone()

            # Извлечение данных, если таблица существует
            if table_exists:
                cursor.execute(f"SELECT date, state_number, work_name FROM {table_name}")
                rows = cursor.fetchall()  # Получение всех строк из таблицы
            else:
                rows = []  # Если таблицы нет, создаем пустой список

    except Exception as e:
        print(f"Ошибка при извлечении данных: {e}")
        rows = []  # На случай ошибки при выполнении SQL-запроса

    return render(request, 'main/mechanic_detail.html', {'mechanic': mechanic, 'rows': rows})
def add_mechanic_work(request, pk):
    mechanic = get_object_or_404(Mechanic, pk=pk)

    if request.method == 'POST':
        mechanic = get_object_or_404(Mechanic, pk=pk)
        table_name = f"{mechanic.first_name}_{mechanic.last_name}_{mechanic.id}".replace(' ', '_')
        date = request.POST.get('date')
        state_number = request.POST.get('state_number')
        work_names = request.POST.getlist('work_name[]')  # Получаем все наименования работ

        try:
            with connection.cursor() as cursor:
                # Создание таблицы, если она не существует (выполняется один раз)
                cursor.execute(f"""
                            CREATE TABLE IF NOT EXISTS {table_name} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT,
                                state_number TEXT,
                                work_name TEXT
                            )
                        """)

                # Вставка каждой строки работы в таблицу
                for work_name in work_names:
                    cursor.execute(f"""
                                INSERT INTO {table_name} (date, state_number, work_name)
                                VALUES (%s, %s, %s)
                            """, [date, state_number, work_name])

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
            return JsonResponse({'success': False, 'message': str(e)})

        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})