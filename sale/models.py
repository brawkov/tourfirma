from django.db import models
from client.models import Client
from tour.models import *
from users.models import Employee


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True, verbose_name='Код продажи', editable=False)
    client_passp = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True, verbose_name='Клиент')
    employee_passp = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True,
                                       verbose_name='Сотрудник')
    tour = models.ForeignKey(Tour, models.DO_NOTHING, blank=True, null=True, verbose_name='Тур')
    sale_date = models.DateField(verbose_name='Дата продажи')

    def __str__(self):
        # return '%s %s' % (self.client_passp, self.employee_passp)
        return f"{self.client_passp} - {self.tour}"


    class Meta:
        db_table = 'sale'
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
        permissions = (
            ("can_open_reports","Доступ к отчетам"),
        )