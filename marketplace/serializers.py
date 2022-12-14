from rest_framework import serializers
from django.db import transaction
from core.models import User
from .models import Cart, CartItem, Customer, House, HouseImage, Address, Order, OrderItem, Review


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


class CartItemSerializer(serializers.ModelSerializer):
    house = HouseSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'house']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    total_price = serializers.SerializerMethodField(source='get_total_price')
    items = CartItemSerializer(read_only=True, many=True)

    def get_total_price(self, cart):
        return sum([item.house.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'items']


class AddCartItemSerializer(serializers.ModelSerializer):
    house_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'house_id']

    def validate(self, attrs):
        if CartItem.objects.filter(cart_id=self.context['cart_id'], house_id=attrs['house_id']).exists():
            raise serializers.ValidationError(
                'House with given ID is already in the cart.')
            if OrderItem.objects.filter(house_id=attrs['house_id']).exists():
                raise serializers.ValidationError(
                    'This house has been already bought.')
        return attrs

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        self.instance = CartItem.objects.create(
            cart_id=self.context['cart_id'], **self.validated_data)
        return self.instance


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'house', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(
                user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects \
                .select_related('house') \
                .filter(cart_id=cart_id)
            order_items = [OrderItem(order=order, house=item.house,
                                     unit_price=item.house.price) for item in cart_items]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
            self.instance = order

            return self.instance


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
