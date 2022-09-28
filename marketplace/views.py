from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from marketplace.models import Customer, House, HouseImage, Address
from marketplace.serializers import CustomerSerializer, AddressSerializer, HouseImageSerializer, HouseSerializer
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
        return {'house_id': self.kwargs['house_pk'], 'user_id': self.request.user.id}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(
            user_id=user_id)
        if request.method == 'GET':
            customer = Customer.objects.filter(user_id=user_id).first()
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
