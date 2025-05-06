from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('complete/', views.order_complete, name='order_complete'),
    path('history/', views.order_history, name='order_history'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
]
