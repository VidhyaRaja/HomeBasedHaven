from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views import FoodItemViewSet, OrderViewSet, DeliveryOptionViewSet

router = DefaultRouter()
router.register(r'food-items', FoodItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'delivery-options', DeliveryOptionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
