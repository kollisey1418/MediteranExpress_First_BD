# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('garage/', views.garage, name='garage'),
    path('autopark/', views.autopark, name='autopark'),
    path('warehouse-new/', views.warehouse_new, name='warehouse_new'),
    path('add-item/', views.add_item, name='add_item'),
]
