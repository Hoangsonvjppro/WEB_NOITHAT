from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve
from django.conf import settings

class RoleBasedAccessMiddleware:
    """
    Middleware to control access to pages based on user roles.
    Prevent staff from accessing customer pages and vice versa.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check authenticated users
        if request.user.is_authenticated:
            # Get the current URL
            current_url = request.path_info
            
            # Skip check for media and static files
            if current_url.startswith(settings.MEDIA_URL) or current_url.startswith(settings.STATIC_URL):
                return self.get_response(request)
            
            # Staff users should be redirected from customer-focused pages to the staff dashboard
            if (request.user.role != 'customer' and 
                not current_url.startswith('/admin/') and 
                not current_url.startswith('/staff/') and
                not current_url.startswith('/accounts/') and
                current_url != '/'):
                
                # Common paths that should be accessible to everyone (like logout)
                allowed_paths = ['/accounts/logout/', '/accounts/profile/']
                if current_url in allowed_paths:
                    return self.get_response(request)
                
                messages.info(request, 'Bạn đã được chuyển hướng đến trang nhân viên.')
                return redirect('staff:dashboard')
                
            # Customers should not see internal staff pages
            if request.user.role == 'customer' and current_url.startswith('/staff/'):
                messages.error(request, 'Bạn không có quyền truy cập trang nhân viên.')
                return redirect('home')
                
        return self.get_response(request) 