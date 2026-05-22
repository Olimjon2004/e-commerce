from django.db import models
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Product, Category, Review
from products.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from rest_framework import generics, filters

from django_filters import rest_framework as django_filters
from rest_framework.pagination import PageNumberPagination
from .filters import ProductFilter


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    seralizer_class = ReviewSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CustomerPagination(PageNumberPagination):
    page_size = 3


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = CustomerPagination

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fileds = ['name', 'description']


    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Products.objetcs.filter(category=instance.category).exclude(id-instance.id)[:5]
        related_serializer = ProductSerializer(related_products, many=True)
        return Response({
            'product':serializer.data,
            'related_products':related_serializer.data
        })
    

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:2]
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({'average_rating': 'No reviews yet!'})
        
        avg_rating = sum([reviews.rating for review in reviews]) / reviews.count()

        return Response({'average_rating': avg_rating})