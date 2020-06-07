from .models import Visa, Client
from users.admin import admin_site
from django.contrib import admin


class VisaInline(admin.ModelAdmin):
    model = Visa
    list_display = (
        'client_passp', 'visa_date_issue', 'visa_duration', 'visa_begin', 'visa_end', 'visa_type',
        'visa_quantity_trip')

@admin.register(Client, site=admin_site)
class ClientAdmin(admin.ModelAdmin):

    list_display = (
    'client_surname', 'client_name', 'client_patronymic', 'client_passp_id', 'client_gender', 'client_phone_number',
    'client_email', 'client_birthday', 'client_address')

    search_fields = ('client_surname', 'client_name', 'client_patronymic', 'client_phone_number')

admin_site.register(Visa,VisaInline)
