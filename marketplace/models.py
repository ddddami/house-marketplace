from django.db import models
from django.contrib import admin
from django.conf import settings
# Create your models here.


class Address(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    house = models.OneToOneField('House', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name


class House(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    bathrooms = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField()
    parking = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name


class HouseImage(models.Model):
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='marketplace/images')
