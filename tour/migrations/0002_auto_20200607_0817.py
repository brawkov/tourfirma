# Generated by Django 3.0.7 on 2020-06-07 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_name',
            field=models.CharField(default='', max_length=200, unique=True, verbose_name='Название акции'),
        ),
    ]
