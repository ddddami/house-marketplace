from django_filters.rest_framework import FilterSet
from .models import House


class HouseFilter(FilterSet):
    class Meta:
        model = House
        fields = {
            'price': ['gt', 'lt']
        }
