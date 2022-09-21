from rest_framework import serializers
from .models import House, HouseImage


class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ['id', ]


class HouseSerializer(serializers.ModelSerializer):
    images = HouseImageSerializer(many=True, read_only=True)

    class Meta:
        model = House
        fields = ['id', 'name', 'description', 'price',
                  'bathrooms', 'bedrooms', 'parking', 'date_created', 'images']
