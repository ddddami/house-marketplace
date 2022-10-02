from rest_framework import serializers
from core.models import User
from .models import Customer, House, HouseImage, Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'name', 'latitude', 'longitude']


class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        fields = ['id', 'image']

    def validate(self, attrs):
        house_id = self.context['house_id']
        user_id = self.context['user_id']
        customer_id = Customer.objects.get(
            user_id=user_id).id
        if not House.objects.filter(
                id=house_id, customer_id=customer_id).exists():

            raise serializers.ValidationError(
                'House was not posted by given user.')
        return attrs

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

    def create(self, validated_data):
        print(validated_data)
        address_data = dict(validated_data.pop('address'))
        address = Address(**address_data)
        address.house_id = self.context['house_id']
        house = House(**(validated_data))
        house.customer_id = self.context['customer_id']
        house.address = address
        house.save()
        address.save()
        # address = Address(**(validated_data[7:]))
        # address.save()
        # return house
        return house

    def update(self, instance, validated_data):
        address_data = dict(validated_data.pop('address'))
        address = Address(**address_data)
        address.house_id = self.context['house_id']
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.address = address

        instance.save()
        return instance


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
