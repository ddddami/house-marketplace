from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Address, House
# Register your models here.

admin.site.register(Address)


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
        return format_html('<a href="{}">{}</a>', url, house.address.name)
