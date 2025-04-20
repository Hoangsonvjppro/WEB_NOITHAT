from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category

def product_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'name')

    products = Product.objects.all()
    if selected_category:
        products = products.filter(category_id=selected_category)
    if search_query:
        products = products.filter(name__icontains=search_query)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'products': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
        'page_obj': page_obj,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})