from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, F, Q
from django.core.paginator import Paginator
from datetime import datetime, timedelta

from accounts.models import User, StaffProfile
from products.models import Product, Category
from orders.models import Order, OrderItem
from branches.models import Branch
from inventory.models import InventoryRecord, StockMovement, Warehouse
from suppliers.models import Supplier


def staff_required(function):
    """Decorator to check if user is staff"""
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Vui lòng đăng nhập để truy cập trang này.')
            return redirect('accounts:login')
            
        if request.user.role == 'customer':
            messages.error(request, 'Bạn không có quyền truy cập trang nhân viên.')
            return redirect('home')
            
        return function(request, *args, **kwargs)
    return wrap


@login_required
@staff_required
def dashboard(request):
    """
    Display appropriate dashboard based on user role
    """
    user = request.user
    today = timezone.now().date()
    
    # Common dashboard data
    today_orders = Order.objects.filter(created_at__date=today)
    today_orders_count = today_orders.count()
    
    # Get products with low stock
    low_stock_products = Product.objects.filter(quantity__lte=F('inventory_records__min_stock_level'))
    low_stock_count = low_stock_products.count()
    
    # Orders in processing status
    processing_orders = Order.objects.filter(status='processing')
    processing_orders_count = processing_orders.count()
    
    # Calculate monthly revenue
    start_of_month = today.replace(day=1)
    monthly_revenue = Order.objects.filter(
        created_at__date__gte=start_of_month, 
        payment_status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Common context
    context = {
        'today_orders_count': today_orders_count,
        'low_stock_count': low_stock_count,
        'processing_orders_count': processing_orders_count,
        'monthly_revenue': monthly_revenue,
        'recent_orders': Order.objects.all().order_by('-created_at')[:5],
    }
    
    # Role-specific dashboards
    if user.is_branch_manager:
        # Get branch managed by this user
        try:
            branch = Branch.objects.get(manager=user)
            staff_profiles = StaffProfile.objects.filter(branch=branch)
            
            # Branch-specific metrics
            branch_orders = Order.objects.filter(branch=branch)
            branch_orders_count = branch_orders.count()
            
            # Calculate branch revenue
            branch_revenue = branch_orders.filter(
                created_at__date__gte=start_of_month,
                payment_status='paid'
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            
            # Calculate completion rate
            total_branch_orders = branch_orders.count()
            completed_branch_orders = branch_orders.filter(status__in=['delivered', 'completed']).count()
            completion_rate = (completed_branch_orders / total_branch_orders * 100) if total_branch_orders > 0 else 0
            
            branch_context = {
                'branch': branch,
                'staff_count': staff_profiles.count(),
                'branch_staff': staff_profiles[:5],
                'branch_orders': branch_orders[:5],
                'branch_orders_count': branch_orders_count,
                'branch_revenue': branch_revenue,
                'completion_rate': round(completion_rate, 1),
            }
            context.update(branch_context)
            
            return render(request, 'staff/branch_manager/dashboard.html', context)
            
        except Branch.DoesNotExist:
            messages.warning(request, 'Bạn chưa được phân công quản lý chi nhánh nào.')
    
    elif user.is_sales_staff:
        # Sales-specific metrics for current user
        today_sales = today_orders.filter(payment_status='paid').aggregate(
            total=Sum('total_amount'))['total'] or 0
            
        # Pending orders
        pending_orders = Order.objects.filter(
            status__in=['pending', 'processing']).order_by('-created_at')[:10]
            
        # Completed orders
        completed_orders = Order.objects.filter(
            status='delivered').order_by('-created_at')[:5]
            
        # Get top products
        top_products = Product.objects.annotate(
            sold_count=Count('orderitem')).order_by('-sold_count')[:5]
            
        sales_context = {
            'today_sales': today_sales,
            'monthly_sales': monthly_revenue,
            'pending_orders': pending_orders,
            'pending_orders_count': pending_orders.count(),
            'completed_orders': completed_orders,
            'top_products': top_products,
        }
        context.update(sales_context)
        
        return render(request, 'staff/sales/dashboard.html', context)
    
    elif user.is_inventory_manager:
        # Inventory-specific metrics
        today_stock_in = StockMovement.objects.filter(
            movement_type='in', 
            created_at__date=today
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        today_stock_out = StockMovement.objects.filter(
            movement_type='out',
            created_at__date=today
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        # Low stock products
        low_stock_products = low_stock_products.select_related('category', 'supplier')[:10]
        
        # Recent stock movements
        recent_movements = StockMovement.objects.select_related(
            'product', 'performed_by').order_by('-created_at')[:10]
        
        # Pending orders for shipping
        pending_orders = Order.objects.filter(status='processing').order_by('created_at')[:10]
        
        # Categories for chart
        categories = Category.objects.all()[:6]
        
        inventory_context = {
            'total_products': Product.objects.count(),
            'today_stock_in': today_stock_in,
            'today_stock_out': today_stock_out,
            'low_stock_products': low_stock_products,
            'recent_movements': recent_movements,
            'pending_orders': pending_orders,
            'categories': categories,
        }
        context.update(inventory_context)
        
        return render(request, 'staff/inventory/dashboard.html', context)
    
    # Default to admin dashboard for business owner or other roles
    return render(request, 'staff/dashboard/index.html', context)


@login_required
@staff_required
def orders_list(request):
    """Display list of orders with filtering"""
    status_filter = request.GET.get('status', '')
    
    orders = Order.objects.all()
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Role-specific filtering
    if request.user.is_branch_manager:
        try:
            branch = Branch.objects.get(manager=request.user)
            orders = orders.filter(branch=branch)
        except Branch.DoesNotExist:
            orders = Order.objects.none()
    
    orders = orders.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'status_filter': status_filter,
    }
    
    return render(request, 'staff/orders/list.html', context)


@login_required
@staff_required
def order_detail(request, order_id):
    """Display detail of an order"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check permissions
    if request.user.is_branch_manager:
        try:
            branch = Branch.objects.get(manager=request.user)
            if order.branch != branch:
                messages.error(request, 'Bạn không có quyền xem đơn hàng này.')
                return redirect('staff:orders')
        except Branch.DoesNotExist:
            messages.error(request, 'Bạn không có quyền xem đơn hàng này.')
            return redirect('staff:orders')
    
    context = {
        'order': order,
    }
    
    return render(request, 'staff/orders/detail.html', context)


@login_required
@staff_required
def order_update(request, order_id):
    """Update order status"""
    # This is a stub, actual implementation would include forms
    # and proper permission handling
    return render(request, 'staff/orders/update.html', {})


@login_required
@staff_required
def new_order(request):
    """Create new order (POS function for staff)"""
    # This is a stub, actual implementation would include forms
    # for creating orders at the point of sale
    return render(request, 'staff/orders/new.html', {})


@login_required
@staff_required
def generate_invoice(request, order_id):
    """Generate invoice for an order"""
    # This is a stub, actual implementation would generate a PDF invoice
    return redirect('staff:order_detail', order_id=order_id)


# Product-related views
@login_required
@staff_required
def products_list(request):
    """List all products with filtering"""
    return render(request, 'staff/products/list.html', {})


@login_required
@staff_required
def product_detail(request, product_id):
    """Show product details"""
    return render(request, 'staff/products/detail.html', {})


# Inventory-related views
@login_required
@staff_required
def inventory_list(request):
    """List inventory records"""
    return render(request, 'staff/inventory/list.html', {})


@login_required
@staff_required
def low_stock(request):
    """Show products with low stock"""
    return render(request, 'staff/inventory/low_stock.html', {})


@login_required
@staff_required
def stock_in(request):
    """Add stock to inventory"""
    return render(request, 'staff/inventory/stock_in.html', {})


@login_required
@staff_required
def stock_out(request):
    """Remove stock from inventory"""
    return render(request, 'staff/inventory/stock_out.html', {})


@login_required
@staff_required
def stock_in_product(request, product_id):
    """Add stock for specific product"""
    return render(request, 'staff/inventory/stock_in_product.html', {})


@login_required
@staff_required
def stock_movements(request):
    """List stock movements"""
    return render(request, 'staff/inventory/movements.html', {})


@login_required
@staff_required
def process_shipment(request, order_id):
    """Process order shipment"""
    return render(request, 'staff/inventory/process_shipment.html', {})


# Staff management views
@login_required
@staff_required
def staff_members(request):
    """List staff members"""
    # Check if user has permission to view staff
    if not (request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền xem trang này.')
        return redirect('staff:dashboard')
        
    return render(request, 'staff/staff/list.html', {})


@login_required
@staff_required
def staff_detail(request, staff_id):
    """Show staff member details"""
    if not (request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền xem trang này.')
        return redirect('staff:dashboard')
        
    return render(request, 'staff/staff/detail.html', {})


# Branch management views
@login_required
@staff_required
def branches_list(request):
    """List branches"""
    # Only business owner can view all branches
    if not request.user.is_business_owner:
        messages.error(request, 'Bạn không có quyền xem trang này.')
        return redirect('staff:dashboard')
        
    return render(request, 'staff/branches/list.html', {})


@login_required
@staff_required
def branch_detail(request, branch_id):
    """Show branch details"""
    branch = get_object_or_404(Branch, id=branch_id)
    
    # Check if user has permission to view branch details
    if not (request.user.is_business_owner or 
           (request.user.is_branch_manager and StaffProfile.objects.filter(user=request.user, branch=branch).exists())):
        messages.error(request, 'Bạn không có quyền xem chi tiết chi nhánh này.')
        return redirect('staff:dashboard')
    
    return render(request, 'staff/branches/detail.html', {'branch': branch})


@login_required
@staff_required
def branch_edit(request, branch_id):
    """Edit branch details"""
    if not request.user.is_business_owner:
        messages.error(request, 'Bạn không có quyền chỉnh sửa chi nhánh.')
        return redirect('staff:dashboard')
        
    return render(request, 'staff/branches/edit.html', {})


# Report views
@login_required
@staff_required
def reports(request):
    """Show reports dashboard"""
    if not (request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền xem báo cáo.')
        return redirect('staff:dashboard')
        
    return render(request, 'staff/reports/index.html', {})


@login_required
@staff_required
def sales_report(request):
    """Show sales reports"""
    if not (request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền xem báo cáo.')
        return redirect('staff:dashboard')
        
    return render(request, 'staff/reports/sales.html', {})


@login_required
@staff_required
def inventory_report(request):
    """Show inventory reports"""
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền xem báo cáo.')
        return redirect('staff:dashboard')
        
    return render(request, 'staff/reports/inventory.html', {})


# Supplier views
@login_required
@staff_required
def suppliers_list(request):
    """List suppliers"""
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền xem trang này.')
        return redirect('staff:dashboard')
        
    return render(request, 'staff/suppliers/list.html', {})


# Settings view
@login_required
@staff_required
def settings(request):
    """System settings"""
    if not request.user.is_business_owner:
        messages.error(request, 'Bạn không có quyền xem trang này.')
        return redirect('staff:dashboard')
        
    return render(request, 'staff/settings/index.html', {}) 