from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('garage/', views.garage, name='garage'),
    path('warehouse-new/', views.warehouse_new, name='warehouse_new'),
    path('autopark/', views.autopark, name='autopark'),
    path('add-item/', views.add_item, name='add_item'),
    path('add-item-form/', views.add_item_form, name='add_item_form'),
    path('edit-item/<int:item_id>/', views.edit_item, name='warehouse_item_edit'),
    path('warehouse/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('autopark/add_car/', views.add_car, name='add_car'),
    path('autopark/edit_car/<str:vin_code>/', views.edit_car, name='edit_car'),
    path('autopark/car/<str:vin_code>/', views.car_detail, name='car_detail'),
    path('autopark/add_work/<str:vin_code>/', views.add_work, name='add_work'),
    path('autopark/add_fault/<str:vin_code>/', views.add_fault, name='add_fault'),
    path('autopark/work_detail/<int:work_id>/', views.work_detail, name='work_detail'),
    path('autopark/fault_detail/<int:fault_id>/', views.fault_detail, name='fault_detail'),
    path('warehouse/search_part/', views.search_part, name='search_part'),
    path('autopark/save_work/<str:vin_code>/', views.save_work, name='save_work'),

]
