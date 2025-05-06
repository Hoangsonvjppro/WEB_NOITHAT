from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category, ProductReview
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category_slug = self.kwargs.get('category_slug')
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
            
        # Filter by price
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        # Filter by other attributes
        color = self.request.GET.get('color')
        material = self.request.GET.get('material')
        if color:
            queryset = queryset.filter(color=color)
        if material:
            queryset = queryset.filter(material=material)
            
        # Sorting
        sort_by = self.request.GET.get('sort')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'name_asc':
            queryset = queryset.order_by('name')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        
        # Get colors and materials for filtering
        context['colors'] = Product.objects.exclude(color='').values_list('color', flat=True).distinct()
        context['materials'] = Product.objects.exclude(material='').values_list('material', flat=True).distinct()
        
        # Get the current category if filtering by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
            
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Get related products
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        
        # Check if the user has already reviewed the product
        if self.request.user.is_authenticated:
            context['user_has_reviewed'] = ProductReview.objects.filter(
                product=product,
                user=self.request.user
            ).exists()
            
        return context


@login_required
def add_review(request, product_id):
    """Add a review to a product"""
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if not rating:
            return JsonResponse({'status': 'error', 'message': 'Vui lòng chọn đánh giá'})
            
        product = get_object_or_404(Product, id=product_id)
        
        # Check if user already reviewed this product
        existing_review = ProductReview.objects.filter(product=product, user=request.user).first()
        
        if existing_review:
            # Update existing review
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
            message = 'Cảm ơn bạn đã cập nhật đánh giá!'
        else:
            # Create new review
            ProductReview.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            message = 'Cảm ơn bạn đã đánh giá sản phẩm!'
            
        return JsonResponse({'status': 'success', 'message': message})
        
    return JsonResponse({'status': 'error', 'message': 'Phương thức không được hỗ trợ'})


def get_categories(request):
    """Get all categories for navbar dropdown"""
    categories = Category.objects.filter(parent=None, is_active=True)
    
    result = []
    for category in categories:
        cat_dict = {
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'children': []
        }
        
        children = Category.objects.filter(parent=category, is_active=True)
        for child in children:
            cat_dict['children'].append({
                'id': child.id,
                'name': child.name,
                'slug': child.slug
            })
            
        result.append(cat_dict)
        
    return JsonResponse({'categories': result})
