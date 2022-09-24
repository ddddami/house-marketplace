from rest_framework import serializers
from .models import Customer, House, HouseImage, Address


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


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date']

    def validate(self, value):
        user_id = self.context['user_id']

        if Customer.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError(
                'Customer with user already exists.')
        return user_id

    def create(self, validated_data):
        user_id = self.context['user_id']
        return Customer.objects.create(user_id=user_id, **validated_data)