from django.contrib.auth.models import User
from django.db import models


class CookProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    bio = models.TextField(blank=True)

    # Additional fields for the cook

    def __str__(self):
        return self.user.username


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()

    # Additional fields for the customer

    def __str__(self):
        return self.user.username


class DeliveryPartnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=50)
    available = models.BooleanField(default=True)

    # Additional fields for the delivery partner

    def __str__(self):
        return self.user.username
