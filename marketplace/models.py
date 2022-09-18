from django.db import models

# Create your models here.


class Address(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longtitude = models.DecimalField(max_digits=9, decimal_places=6)
    house = models.OneToOneField('House', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class House(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    bathrooms = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
