from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='category_products'),
    path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('api/categories/', views.get_categories, name='get_categories'),
]
