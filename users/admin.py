from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Employee


class MyAdminSite(AdminSite):
    site_title = 'ООО"Турфирма"'
    site_header = 'Турфирма'
    index_title = ''
    site_url = ""


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Employee
    # list_display = ['username','email' ,'employee_passp_id']
    # fieldsets = UserAdmin.fieldsets + (
    #          (None, {'fields': ('employee_passp_id')}),
    # )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': (
        'first_name', 'employee_patronymic', 'last_name', 'employee_passp_id', 'employee_gender', 'employee_address',
        'email', 'employee_phone')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'employee_passp_id', 'password1', 'password2'),
        }),
    )


admin_site = MyAdminSite(name='myadmin')
admin_site.register(Employee, CustomUserAdmin)

# admin.site.register(Employee, CustomUserAdmin)
