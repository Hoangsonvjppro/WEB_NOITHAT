from django.urls import path
from .views import sales_report

app_name = 'reports'

urlpatterns = [
    path('sales_report/', sales_report, name='sales_report'),
]