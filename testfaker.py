import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cursovai.settings')

import django

django.setup()

from tour.models import *
from faker import Faker

fake = Faker('ru_RU')


def add_Country():
    # for i in range(4):
    fake_id = fake.random_int(min=100, max=500, step=3)
    fake_name = fake.country()
    country = Country.objects.get_or_create(country_id=fake_id, country_name=fake_name)[0]
    country.save()
    return country


def add_City():
    # for i in range(5):
        fake_country = add_Country()
        fake_name = fake.city()
        city = City.objects.get_or_create(country=fake_country, city_name=fake_name)


def add_Hotel():
    hotel_type = ['Бизнес-отель', 'Гостиница', 'Резорт-отель', 'Бутик-отель', 'Апартаменты', 'Хостел']
    for i in range(5):
        fake_city = add_City()
        fake_star = fake.random_int(min=0, max=5)
        fake_name = fake.company()
        fake_type = fake.words(1, hotel_type, True)
        fake_description = fake.text()
        hotel = Hotel.objects.get_or_create(hotel_name=fake_name, hotel_star=fake_star, hotel_type=fake_type,
                                            hotel_description=fake_description, city=fake_city)
# def add_Tour():
#     tour =Tour.objects.get_or_create(tour_id=tour_id, country_name=fake_name)
# add_Country()
# add_City()
add_Hotel()