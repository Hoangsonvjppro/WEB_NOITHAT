from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_dashboard, name='dashboard'),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    path('stock-movements/', views.stock_movement_list, name='stock_movement_list'),
    path('stock-movements/create/', views.stock_movement_create, name='stock_movement_create'),
    path('reports/', views.inventory_reports, name='reports'),
]
