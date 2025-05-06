from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile, StaffProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a profile for the user when a user is created based on their role
    """
    if created:
        if instance.is_customer:
            CustomerProfile.objects.create(user=instance)
        elif instance.is_sales_staff or instance.is_inventory_manager or instance.is_branch_manager or instance.is_business_owner:
            StaffProfile.objects.create(
                user=instance,
                employee_id=f"EMP{instance.id:06d}",
                position=dict(User.ROLE_CHOICES).get(instance.role, "Staff")
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Update the user's profile when the user is updated
    """
    if hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
    elif hasattr(instance, 'staff_profile'):
        instance.staff_profile.save() 