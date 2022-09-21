from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from marketplace.models import House
from marketplace.serializers import HouseSerializer
# Create your views here.


class HouseViewSet(ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
