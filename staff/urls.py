from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    # Common dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Orders management
    path('orders/', views.orders_list, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/update/', views.order_update, name='order_update'),
    path('orders/new/', views.new_order, name='new_order'),
    path('orders/<int:order_id>/invoice/', views.generate_invoice, name='generate_invoice'),
    
    # Products
    path('products/', views.products_list, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Inventory management
    path('inventory/', views.inventory_list, name='inventory'),
    path('inventory/low-stock/', views.low_stock, name='low_stock'),
    path('inventory/stock-in/', views.stock_in, name='stock_in'),
    path('inventory/stock-out/', views.stock_out, name='stock_out'),
    path('inventory/stock-in/<int:product_id>/', views.stock_in_product, name='stock_in_product'),
    path('inventory/stock-movements/', views.stock_movements, name='stock_movements'),
    path('inventory/report/', views.inventory_report, name='inventory_report'),
    path('inventory/process-shipment/<int:order_id>/', views.process_shipment, name='process_shipment'),
    
    # Staff management
    path('staff-members/', views.staff_members, name='staff_members'),
    path('staff-members/<int:staff_id>/', views.staff_detail, name='staff_detail'),
    
    # Branch management
    path('branches/', views.branches_list, name='branches'),
    path('branches/<int:branch_id>/', views.branch_detail, name='branch_detail'),
    path('branches/<int:branch_id>/edit/', views.branch_edit, name='branch_edit'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
    
    # Settings
    path('settings/', views.settings, name='settings'),
    
    # Suppliers
    path('suppliers/', views.suppliers_list, name='suppliers'),
] 