from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_dashboard, name='dashboard'),
    path('sales/', views.sales_report, name='sales'),
    path('inventory/', views.inventory_report, name='inventory'),
    path('performance/', views.performance_report, name='performance'),
]
