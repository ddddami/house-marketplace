from rest_framework import serializers
from core.models import User
from .models import Cart, CartItem, Customer, House, HouseImage, Address, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date', 'customer']

    def create(self, validated_data):
        review = Review(**validated_data)
        review.house_id = self.context['house_id']
        review.customer_id = self.context['customer_id']
        review.save()
        return review


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id']


class CartItemSerializer(serializers.ModelSerializer):
    house = HouseSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'house']


class AddCartItemSerializer(serializers.ModelSerializer):
    house_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'house_id']

    def validate(self, attrs):
        if CartItem.objects.filter(cart_id=self.context['cart_id'], house_id=attrs['house_id']).exists():
            raise serializers.ValidationError(
                'House with given ID is already in the cart.')
        return attrs

    def save(self, **kwargs):
        self.instance = CartItem.objects.create(
            cart_id=self.context['cart_id'], **self.validated_data)
        return self.instance
