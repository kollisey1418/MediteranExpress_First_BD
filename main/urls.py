from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('autopark/save_work_or_add/<str:vin_code>/', views.save_work_or_add, name='save_work_or_add'),
    path('autopark/add_fault/<str:vin_code>/', views.add_fault, name='add_fault'),
    path('autopark/work_detail/<int:work_id>/', views.work_detail, name='work_detail'),
    path('autopark/fault_detail/<int:fault_id>/', views.fault_detail, name='fault_detail'),
    path('warehouse/search_part/', views.search_part, name='search_part'),
    path('mechanics/', views.mechanics_list, name='mechanics_list'),
    path('add_mechanic/', views.add_mechanic, name='add_mechanic'),
    path('mechanic/<int:pk>/', views.mechanic_detail, name='mechanic_detail'),
    path('mechanic/<int:pk>/add_mechanic_work/', views.add_mechanic_work, name='add_mechanic_work'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register_user, name='register_user'),
    path('autopark_main/', views.autopark_main, name='autopark_main'),
    path('drivers/', views.drivers, name='drivers'),


]
