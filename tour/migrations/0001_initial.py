# Generated by Django 3.0.7 on 2020-06-06 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Код города')),
                ('city_name', models.CharField(default='', max_length=200, unique=True, verbose_name='Название города')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Код страны')),
                ('country_name', models.CharField(default='', max_length=200, unique=True, verbose_name='Название страны')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('discount_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('discount_name', models.CharField(default='', max_length=200, unique=True, verbose_name='Название скидки')),
                ('discount_amount', models.IntegerField(default='', verbose_name='Размер скидки')),
                ('discount_inf', models.TextField(default='', verbose_name='Описание акции')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
                'db_table': 'discount',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('hotel_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Код отеля')),
                ('hotel_name', models.CharField(default='', max_length=200, unique=True, verbose_name='Название отеля')),
                ('hotel_star', models.CharField(choices=[('0', 'Без звезд'), ('1', 'Одна'), ('2', 'Две'), ('3', 'Три'), ('4', 'Четыре'), ('5', 'Пять')], default='', max_length=1, verbose_name='Количество звезд отеля')),
                ('hotel_type', models.CharField(default='', max_length=100, verbose_name='Тип отеля')),
                ('hotel_description', models.TextField(blank=True, null=True, verbose_name='Описание отеля')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tour.City', verbose_name='Название города')),
            ],
            options={
                'verbose_name': 'Отель',
                'verbose_name_plural': 'Отели',
                'db_table': 'hotel',
            },
        ),
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('nutrition_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Название питания')),
                ('nutrition_type', models.CharField(default='', max_length=3, verbose_name='Тип питания')),
                ('nutrition_description', models.TextField(default='', verbose_name='Описание питания')),
            ],
            options={
                'verbose_name': 'Питание',
                'verbose_name_plural': 'Питания',
                'db_table': 'nutrition',
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('transfer_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Код транспорта')),
                ('transfer_type', models.CharField(default='', max_length=20, verbose_name='Вид транспорта')),
                ('transfer_begin', models.DateTimeField(default='', verbose_name='Время выезда')),
                ('transfer_end', models.DateTimeField(default='', verbose_name='Время приезда')),
                ('city_finish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_finish', to='tour.City', verbose_name='Название города приезда')),
                ('city_start', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_start', to='tour.City', verbose_name='Название города выезда')),
            ],
            options={
                'verbose_name': 'Транспорт',
                'verbose_name_plural': 'Транспорта',
                'db_table': 'transfer',
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('tour_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Код тура')),
                ('tour_begin', models.DateField(default='', verbose_name='Дата начала тура')),
                ('tour_end', models.DateField(default='', verbose_name='Дата окончания тура')),
                ('tour_type_number', models.CharField(default='', max_length=20, verbose_name='Тип номера отеля')),
                ('tour_tourists', models.PositiveSmallIntegerField(default='', verbose_name='Колличество туристов')),
                ('tour_cost', models.FloatField(default='', verbose_name='Стоимость')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tour.Discount', verbose_name='Скидка')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tour.Hotel', verbose_name='Отель')),
                ('nutrition', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tour.Nutrition', verbose_name='Питание')),
                ('transfer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tour.Transfer', verbose_name='Вид транпорта')),
            ],
            options={
                'verbose_name': 'Тур',
                'verbose_name_plural': 'Туры',
                'db_table': 'tour',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tour.Country', verbose_name='Название страны'),
        ),
    ]
