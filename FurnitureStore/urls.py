from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import view từ products để ánh xạ URL gốc
from apps.products.views import product_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('products/', include('apps.products.urls')),
    path('reports/', include('apps.reports.urls')),
    path('', product_list, name='home'),  # Ánh xạ URL gốc (/) đến product_list
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)