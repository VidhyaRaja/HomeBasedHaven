from django.db import models
from users.models import CustomUser, CookProfile, CustomerProfile


class FoodItem(models.Model):
    cook = models.ForeignKey(CookProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()
    is_instant = models.BooleanField(default=False)  # For instant orders
    pre_order_only = models.BooleanField(default=False)  # For pre-orders


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        order.calculate_total_price()
        return order


class DeliveryOption(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=50,
                                     choices=[('self', 'Self Collection'), ('free_delivery', 'Free Delivery'),
                                              ('third_party', 'Third Party')])
    delivery_partner = models.ForeignKey(DeliveryPartnerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
