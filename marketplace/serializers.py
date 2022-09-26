from rest_framework import serializers
from .models import Address, House, HouseImage


class AddressSerializer(serializers.ModelSerializer):
    longitude = serializers.SerializerMethodField()

    def get_longitude(self, address):
        return address.longtitude

    class Meta:
        model = Address
        fields = ['id', 'name', 'latitude', 'longitude']


class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ['id', 'image']

    def create(self, validated_data):
        house_id = self.context['house_id']
        return HouseImage.objects.create(house_id=house_id, **validated_data)


class HouseSerializer(serializers.ModelSerializer):
    images = HouseImageSerializer(many=True, read_only=True)
    address = AddressSerializer()

    class Meta:
        model = House
        fields = ['id', 'name', 'description', 'price',
                  'bathrooms', 'bedrooms', 'parking', 'date_created', 'address', 'images']
