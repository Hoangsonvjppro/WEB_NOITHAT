from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email là bắt buộc'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.BUSINESS_OWNER)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser phải có is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser phải có is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # User roles
    CUSTOMER = 'customer'
    SALES_STAFF = 'sales_staff'
    INVENTORY_MANAGER = 'inventory_manager'
    BRANCH_MANAGER = 'branch_manager'
    BUSINESS_OWNER = 'business_owner'
    
    ROLE_CHOICES = [
        (CUSTOMER, _('Khách hàng')),
        (SALES_STAFF, _('Nhân viên bán hàng')),
        (INVENTORY_MANAGER, _('Nhân viên quản lý kho')),
        (BRANCH_MANAGER, _('Quản lý chi nhánh')),
        (BUSINESS_OWNER, _('Chủ doanh nghiệp')),
    ]
    
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(_('Họ'), max_length=30, blank=True)
    last_name = models.CharField(_('Tên'), max_length=30, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Số điện thoại phải có định dạng: '+999999999'. Tối đa 15 ký tự.")
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    role = models.CharField(_('Vai trò'), max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    is_staff = models.BooleanField(_('Nhân viên'), default=False,
                                   help_text=_('Xác định người dùng có thể đăng nhập vào trang quản trị hay không.'))
    is_active = models.BooleanField(_('Hoạt động'), default=True,
                                    help_text=_('Chỉ định người dùng có hoạt động hay không.'))
    date_joined = models.DateTimeField(_('Ngày tham gia'), default=timezone.now)
    last_login = models.DateTimeField(_('Đăng nhập lần cuối'), null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Người dùng')
        verbose_name_plural = _('Người dùng')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_short_name(self):
        return self.last_name or self.email.split('@')[0]
    
    @property
    def is_customer(self):
        return self.role == self.CUSTOMER
    
    @property
    def is_sales_staff(self):
        return self.role == self.SALES_STAFF
    
    @property
    def is_inventory_manager(self):
        return self.role == self.INVENTORY_MANAGER
    
    @property
    def is_branch_manager(self):
        return self.role == self.BRANCH_MANAGER
    
    @property
    def is_business_owner(self):
        return self.role == self.BUSINESS_OWNER


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(_('Địa chỉ'), blank=True)
    birth_date = models.DateField(_('Ngày sinh'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Thông tin khách hàng')
        verbose_name_plural = _('Thông tin khách hàng')
    
    def __str__(self):
        return f"Thông tin của {self.user.get_full_name()}"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(_('Mã nhân viên'), max_length=20, unique=True)
    position = models.CharField(_('Chức vụ'), max_length=100)
    hire_date = models.DateField(_('Ngày tuyển dụng'), default=timezone.now)
    branch = models.ForeignKey('branches.Branch', on_delete=models.SET_NULL, null=True, related_name='staff')
    
    class Meta:
        verbose_name = _('Thông tin nhân viên')
        verbose_name_plural = _('Thông tin nhân viên')
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
