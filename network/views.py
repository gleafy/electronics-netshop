from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer, ProductSerializer
from .permissions import IsActiveEmployee


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.select_related("supplier").all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    
    # Фильтрация и поиск
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["country"]
    search_fields = ["name", "city"]