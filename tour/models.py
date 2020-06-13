from django.db import models


class Country(models.Model):
    country_id = models.IntegerField(primary_key=True, verbose_name='Код страны', unique=True)
    country_name = models.CharField(default='', max_length=200, verbose_name='Название страны', unique=True)

    def __str__(self):
        return '%s' % (self.country_name)

    class Meta:
        db_table = 'country'
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class City(models.Model):
    city_id = models.AutoField(primary_key=True, verbose_name='Код города', unique=True, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name='Название страны', )
    city_name = models.CharField(default='', max_length=200, verbose_name='Название города', unique=True)

    def __str__(self):
        return '%s' % (self.city_name)

    class Meta:
        db_table = 'city'
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Hotel(models.Model):
    STAR = [
        ('0', 'Без звезд'),
        ('1', 'Одна'),
        ('2', 'Две'),
        ('3', 'Три'),
        ('4', 'Четыре'),
        ('5', 'Пять')
    ]
    hotel_id = models.AutoField(primary_key=True, verbose_name='Код отеля', unique=True, editable=False)
    hotel_name = models.CharField(default='', max_length=200, verbose_name='Название отеля', unique=True)

    hotel_star = models.CharField(default='', max_length=1, choices=STAR, verbose_name='Количество звезд отеля')

    hotel_type = models.CharField(default='', max_length=100, verbose_name='Тип отеля')
    hotel_description = models.TextField(blank=True, null=True, verbose_name='Описание отеля')
    city = models.ForeignKey(City, models.CASCADE, blank=True, null=True, verbose_name='Название города')

    def __str__(self):
        return '%s' % (self.hotel_name)

    class Meta:
        db_table = 'hotel'
        verbose_name = "Отель"
        verbose_name_plural = "Отели"


class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True, unique=True, editable=False)
    discount_name = models.CharField(default='', max_length=200, verbose_name='Название акции', unique=True)
    discount_amount = models.IntegerField(default='', verbose_name='Размер скидки')
    discount_inf = models.TextField(default='', verbose_name='Описание акции')

    def __str__(self):
        return '%s  -%s %% ' % (self.discount_name, self.discount_amount)

    class Meta:
        db_table = 'discount'
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class Nutrition(models.Model):
    nutrition_id = models.AutoField(primary_key=True, verbose_name='Название питания', unique=True, editable=False)
    nutrition_type = models.CharField(default='', max_length=3, verbose_name='Тип питания')
    nutrition_description = models.TextField(default='', verbose_name='Описание питания')

    def __str__(self):
        return '%s' % (self.nutrition_type)

    class Meta:
        db_table = 'nutrition'
        verbose_name = "Питание"
        verbose_name_plural = "Питания"


class Transfer(models.Model):
    transfer_id = models.AutoField(primary_key=True, verbose_name='Код транспорта', unique=True, editable=False)
    city_start = models.ForeignKey(City, models.CASCADE, verbose_name='Название города выезда',
                                   related_name="city_start")
    city_finish = models.ForeignKey(City, models.CASCADE, verbose_name='Название города приезда',
                                    related_name="city_finish")
    transfer_type = models.CharField(default='', max_length=20, verbose_name='Вид транспорта')
    transfer_begin = models.DateTimeField(default='', verbose_name='Время выезда')
    transfer_end = models.DateTimeField(default='', verbose_name='Время приезда')

    def __str__(self):
        return '%s' % (self.transfer_type)

    class Meta:
        db_table = 'transfer'
        verbose_name = "Транспорт"
        verbose_name_plural = "Транспорт"


class Tour(models.Model):
    tour_id = models.AutoField(primary_key=True, verbose_name='Код тура', unique=True, editable=False)
    transfer = models.ForeignKey(Transfer, models.DO_NOTHING, blank=True, null=True, verbose_name='Вид транпорта')
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING, verbose_name="Отель")
    discount = models.ForeignKey(Discount, models.DO_NOTHING, blank=True, null=True, verbose_name="Скидка")
    nutrition = models.ForeignKey(Nutrition, models.DO_NOTHING, verbose_name="Питание")
    tour_begin = models.DateField(default='', verbose_name='Дата начала тура')
    tour_end = models.DateField(default='', verbose_name='Дата окончания тура')
    tour_type_number = models.CharField(default='', max_length=20, verbose_name='Тип номера отеля')
    tour_tourists = models.PositiveSmallIntegerField(default='', verbose_name='Кол. тур-ов')
    tour_cost = models.FloatField(default='', verbose_name='Стоимость')

    def __str__(self):
        return '%s | %s | %s | %s | %s человек | %s руб | тип питания: %s ' % (
            self.hotel, self.hotel.city, self.hotel.city.country, self.transfer, self.tour_tourists, self.tour_cost,
            self.nutrition)

    class Meta:
        db_table = 'tour'
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
