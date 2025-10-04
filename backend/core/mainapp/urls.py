from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mainapp.views import CatalogViewSet, ProductViewSet, OrderViewSet

# Быстрая регистрация всех ViewSet'ов
router = DefaultRouter()
router.register('catalogs', CatalogViewSet)
router.register('products', ProductViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('api/', include(router.urls)),
]