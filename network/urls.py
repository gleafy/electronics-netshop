from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'nodes', NetworkNodeViewSet, basename='nodes')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]