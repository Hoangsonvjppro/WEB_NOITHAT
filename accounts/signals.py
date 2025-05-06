from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import User, CustomerProfile, StaffProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a profile for the user when a user is created based on their role
    """
    if created:
        try:
            with transaction.atomic():
                if instance.is_customer:
                    CustomerProfile.objects.get_or_create(user=instance)
                elif instance.is_sales_staff or instance.is_inventory_manager or instance.is_branch_manager or instance.is_business_owner:
                    StaffProfile.objects.get_or_create(
                        user=instance,
                        defaults={
                            'employee_id': f"EMP{instance.id:06d}",
                            'position': dict(User.ROLE_CHOICES).get(instance.role, "Staff")
                        }
                    )
        except Exception as e:
            print(f"Error creating profile for user {instance.email}: {e}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Update the user's profile when the user is updated
    """
    try:
        if hasattr(instance, 'customer_profile'):
            instance.customer_profile.save()
        elif hasattr(instance, 'staff_profile'):
            instance.staff_profile.save()
    except Exception as e:
        print(f"Error saving profile for user {instance.email}: {e}") 