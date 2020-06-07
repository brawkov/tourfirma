from datetime import datetime

from django.contrib import admin

from .forms import saleForm
from .models import *
from users.admin import admin_site


def display_hotel(self):
    return "%s" % (self.tour.hotel)


display_hotel.short_description = 'Отель'
display_hotel.admin_order_field = 'tour__hotel__hotel_name'


def display_city(self):
    return "%s" % (self.tour.hotel.city)


display_city.short_description = 'Город'
display_city.admin_order_field = 'tour__hotel__city'


def display_country(self):
    return "%s" % (self.tour.hotel.city.country)


display_country.short_description = 'Страна'
display_country.admin_order_field = 'tour__hotel__city__country'


def display_tour_cost(self):
    return "%s" % (self.tour.tour_cost)


display_tour_cost.short_description = 'Цена'
display_tour_cost.admin_order_field = 'tour__tour_cost'


class SaleAdmin(admin.ModelAdmin):
    model = Sale
    form = saleForm

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.employee_passp = request.user
            obj.sale_date = datetime.today().strftime("%Y-%m-%d")
            obj.save()

    list_display = (
        'client_passp', 'employee_passp', display_hotel, display_city, display_country, display_tour_cost, 'sale_date')

    list_filter = ('sale_date',)
    autocomplete_fields = ('client_passp', 'tour')


admin_site.register(Sale, SaleAdmin)
