from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Address, Customer, House
# Register your models here.

admin.site.register(Address)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ('id', 'first_name', 'last_name', 'is_agent')
    list_select_related = ['user']

    @admin.display(ordering='is_verified')
    def is_agent(self, customer):
        if customer.is_verified:
            return 'Yes'
        return 'No'


class AdressInline(admin.TabularInline):
    model = Address
    list_display = ('id')


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    inlines = [AdressInline]
    list_display = ('id', 'name', 'description', 'price',
                    'bathrooms', 'bedrooms', 'house_address')
    list_editable = ['name', 'price', 'bathrooms', 'bedrooms']
    list_select_related = ['address']
    search_fields = ['name']

    @admin.display()
    def house_address(self, house):
        url = (
            reverse('admin:marketplace_address_changelist')
            + '?'
            + urlencode({
                'house__id': str(house.id)
            }))
        return format_html('<a href="{}">{} Adresses</a>', url, house.address.name)
