from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from marketplace.models import House, HouseImage, Address
from marketplace.serializers import AddressSerializer, HouseImageSerializer, HouseSerializer
from .filters import HouseFilter
# Create your views here.


class HouseViewSet(ModelViewSet):
    queryset = House.objects.prefetch_related('images').all()
    serializer_class = HouseSerializer
    filter_backends = [DjangoFilterBackend,
                       SearchFilter, OrderingFilter]
    filterset_class = HouseFilter
    filterset_fields = ['bedrooms', 'bathrooms']
    search_fields = ['name', 'description', 'address__name']
    ordering_fields = ['id', 'date_created', 'price']


class HouseImageViewSet(ModelViewSet):
    serializer_class = HouseImageSerializer

    def get_queryset(self):
        return HouseImage.objects.filter(house_id=self.kwargs['house_pk'])

    def get_serializer_context(self):
        return {'house_id': self.kwargs['house_pk']}
