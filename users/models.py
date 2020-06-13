from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext_lazy as _


class Employee(AbstractUser):
    GENDER = [
        ('W', 'Женский'),
        ('M', 'Мужской')
    ]

    employee_passp_id = models.CharField(max_length=11, primary_key=True, default='', verbose_name='Номер паспорта')
    employee_patronymic = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name='Отчество')
    employee_address = models.TextField(max_length=500, default='', verbose_name='Адрес')
    employee_phone = models.CharField(max_length=13, default='', verbose_name='Телефон')
    employee_gender = models.CharField(max_length=1, default='', choices=GENDER, verbose_name='Пол')

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.employee_patronymic)


    class Meta:
        db_table = 'Employee'
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
