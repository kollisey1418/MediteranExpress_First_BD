# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('garage/', views.garage, name='garage'),
    path('warehouse-new/', views.warehouse_new, name='warehouse_new'),
    path('autopark/', views.autopark, name='autopark'),
    path('add-item/', views.add_item, name='add_item'),
    path('add-item-form/', views.add_item_form, name='add_item_form'),  # Новый маршрут
    path('edit-item/<int:item_id>/', views.edit_item, name='warehouse_item_edit'),
    path('warehouse/delete/<int:item_id>/', views.delete_item, name='delete_item'),
]
