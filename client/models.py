from django.db import models


class Client(models.Model):
    client_passp_id = models.CharField(default='', max_length=11, primary_key=True, verbose_name='Номер паспорта',
                                       unique=True)
    client_surname = models.CharField(default='', max_length=100, verbose_name='Фамилия')
    client_name = models.CharField(default='', max_length=100, verbose_name='Имя')
    client_patronymic = models.CharField(default='', max_length=100, blank=True, null=True, verbose_name='Очество')
    GENDER = [
        ('W', 'Женский'),
        ('M', 'Мужской')
    ]
    client_gender = models.CharField(default='', max_length=1, choices=GENDER, verbose_name='Пол')
    client_birthday = models.DateField(default='', verbose_name='Дата рожления')
    client_address = models.TextField(default='', verbose_name='Адрес')
    client_phone_number = models.CharField(default='', max_length=13, verbose_name='Номер телефона')
    client_email = models.EmailField(default='', blank=True, null=True, verbose_name='Адресс электронной почты')

    def __str__(self):
        return '%s %s %s' % (self.client_surname, self.client_name, self.client_patronymic)

    class Meta:
        db_table = 'client'
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Visa(models.Model):
    visa_id = models.CharField(default='', max_length=8, primary_key=True, verbose_name='Номер визы', unique=True)
    client_passp = models.ForeignKey(Client, on_delete=models.CASCADE,verbose_name='ФИО')
    visa_date_issue = models.DateField(default='', verbose_name='Дата выдачи')
    visa_duration = models.SmallIntegerField(default='', verbose_name='Длительность')
    visa_begin = models.DateField(default='', verbose_name='Дата начала визы')
    visa_end = models.DateField(default='', verbose_name='Дата окончания визы')
    visa_type = models.CharField(default='', max_length=30, verbose_name='Тип визы', help_text="Выберите одно значение")
    QUANTITY_TRIP = [
        ('1', 'Однократная'),
        ('2', 'Двукратная'),
        ('M', 'Многократная')
    ]
    visa_quantity_trip = models.CharField(default='', choices=QUANTITY_TRIP, max_length=1,
                                          verbose_name='Кратность визы')
    def __str__(self):
        return '%s № %s' % (self.client_passp, self.visa_id)

    class Meta:
        db_table = 'visa'
        verbose_name = "Виза"
        verbose_name_plural = "Визы"
