from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from marketplace.models import Address, House, HouseImage
from marketplace.serializers import AddressSerializer, HouseImageSerializer, HouseSerializer
# Create your views here.


class HouseViewSet(ModelViewSet):
    queryset = House.objects.prefetch_related('images').all()
    serializer_class = HouseSerializer


class HouseImageViewSet(ModelViewSet):
    serializer_class = HouseImageSerializer

    def get_queryset(self):
        return HouseImage.objects.filter(house_id=self.kwargs['house_pk'])

    def get_serializer_context(self):
        return {'house_id': self.kwargs['house_pk']}
