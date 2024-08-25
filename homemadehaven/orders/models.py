from django.db import models
from users.models import CustomUser, CookProfile, CustomerProfile


from django.db import models
from users.models import CustomerProfile, CookProfile


class FoodItem(models.Model):
    cook = models.ForeignKey(CookProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()
    is_instant = models.BooleanField(default=False)  # For instant orders
    pre_order_only = models.BooleanField(default=False)  # For pre-orders


class Order(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    cook = models.ForeignKey(CookProfile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Calculated field

    def calculate_total_price(self):
        total = sum(item.item_total_price for item in self.items.all())
        self.total_price = total
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_total_price()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Calculated field

    def save(self, *args, **kwargs):
        self.item_total_price = self.quantity * self.food_item.price
        super().save(*args, **kwargs)


class DeliveryOption(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=50,
                                     choices=[('self', 'Self Collection'), ('free_delivery', 'Free Delivery'),
                                              ('third_party', 'Third Party')])
    delivery_partner = models.ForeignKey(DeliveryPartnerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
