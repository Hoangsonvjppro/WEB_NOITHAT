from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=20, choices=[('regular', 'Regular'), ('premium', 'Premium')])

    def __str__(self):
        return self.user.username