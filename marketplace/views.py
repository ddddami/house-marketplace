from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, House, HouseImage, Address, Review
from .serializers import CustomerSerializer, AddressSerializer, HouseImageSerializer, HouseSerializer, ReviewSerializer
from .filters import HouseFilter
# Create your views here.


class HouseViewSet(ModelViewSet):
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,
                       SearchFilter, OrderingFilter]
    filterset_class = HouseFilter
    filterset_fields = ['bedrooms', 'bathrooms']
    search_fields = ['name', 'description', 'address__name']
    ordering_fields = ['id', 'date_created', 'price']

    def get_queryset(self):
        user = self.request.user
        if self.request.method in permissions.SAFE_METHODS or user.is_staff:
            return House.objects.prefetch_related('images').select_related('address').select_related('customer__user').all()
        return House.objects.prefetch_related('images').select_related('address').select_related('customer').filter(customer_id=Customer.objects.only('id').get(user_id=user.id))

    def get_serializer_context(self):
        if self.request.user and self.request.user.is_authenticated:
            return {'house_id': self.kwargs.get('pk'), 'customer_id': Customer.objects.only('id').get(user_id=self.request.user.id).id}
        return {'house_id': self.kwargs.get('pk')}


class HouseImageViewSet(ModelViewSet):
    serializer_class = HouseImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return HouseImage.objects.filter(house_id=self.kwargs['house_pk'])

    def get_serializer_context(self):
        return {'house_id': self.kwargs['house_pk'], 'user_id': self.request.user.id}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    @ action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related('customer').filter(house_id=self.kwargs['house_pk'])

    def get_serializer_context(self):
        if self.request.user and self.request.user.is_authenticated:
            return {'house_id': self.kwargs['house_pk'], 'customer_id': Customer.objects.only('id').get(user_id=self.request.user.id).id}
        return {'house_id': self.kwargs['house_pk']}
