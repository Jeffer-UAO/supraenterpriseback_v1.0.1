from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from products.models import Gallery, Category, Product, CategoryProduct
from products.api.serializers import GallerySerializer, CategorySerializer, ProductSerializer, CategoryProductSerializer


class CategoryApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']


class ProductApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('name')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['slug', 'name']


class CategoryProductApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategoryProductSerializer
    queryset = CategoryProduct.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class GalleryApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']
