from rangefilter.filter import DateRangeFilter

from .models import *
from users.admin import admin_site
from django.contrib import admin


class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_id',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'country',)


class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_name', 'hotel_star', 'hotel_type', 'city')


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_name', 'discount_amount', 'discount_inf')


class NutritionAdmin(admin.ModelAdmin):
    list_display = ('nutrition_type', 'nutrition_description')


class TransferAdmin(admin.ModelAdmin):
    list_display = ('transfer_type', 'city_start', 'city_finish', 'transfer_begin', 'transfer_end')


def display_city(self):
    return "%s" % (self.hotel.city)


display_city.short_description = 'Город'
display_city.admin_order_field = 'hotel__city'


def display_country(self):
    return "%s" % (self.hotel.city.country)


display_country.short_description = 'Страна'
display_country.admin_order_field = 'hotel__city__country'


class TourAdmin(admin.ModelAdmin):
    list_display = (display_country, display_city, 'hotel', 'tour_type_number', 'nutrition', 'tour_tourists',
                    'transfer', 'tour_begin', 'tour_end', 'discount', 'tour_cost',)

    search_fields = ('hotel__hotel_name', 'hotel__city__city_name', 'transfer__transfer_type',
                     'hotel__city__country__country_name', 'tour_cost', 'nutrition__nutrition_type')

    list_filter = (
        ('tour_begin', DateRangeFilter),
        ('tour_end', DateRangeFilter),
    )


admin_site.register(Country, CountryAdmin)
admin_site.register(City, CityAdmin)
admin_site.register(Hotel, HotelAdmin)
admin_site.register(Discount, DiscountAdmin)
admin_site.register(Nutrition, NutritionAdmin)
admin_site.register(Transfer, TransferAdmin)
admin_site.register(Tour, TourAdmin)
# admin_site.register( TourAdmin)
