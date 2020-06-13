from django.contrib.auth.models import Permission
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView

from sale.models import Sale, Hotel, Country, Discount
from users.admin import admin_site

from django.http import HttpResponse

from fpdf import FPDF, HTMLMixin

from users.models import Employee


class HtmlPdf(FPDF, HTMLMixin):
    pass


class Reports(TemplateView):
    data = {}

    def view(request):
        permission = Permission.objects.get(codename='can_open_reports')
        print("permission", permission)

        hotel_list = Hotel.objects.all().values("hotel_id", "hotel_name")
        country_list = Country.objects.all().values("country_id", "country_name")
        discount_list = Discount.objects.all().values("discount_id", "discount_name")
        date = datetime.today().strftime("%Y-%m-%d")
        Reports.data = {"admin_site": admin_site, "date":date,
                       "hotel_list": hotel_list, "country_list": country_list, "discount_list": discount_list}
        return render(request, "admin/reports_list.html", context=Reports.data)

    def pdf_view_tour_all(request):
        pdf = HtmlPdf('P', 'mm', 'A4')
        pdf.add_page()
        pdf.add_font('TimesNewRoman', '', 'templates/font/TimesNewRoman.ttf', uni=True)
        pdf.set_font('TimesNewRoman', '', 16)
        date_start = request.GET['data_start']
        date_end = request.GET['data_end']
        if ((not date_start) | (not date_end)):
            Reports.data.update({'error_message': "Не правильно выбрана дата"})
            return render(request, "admin/reports_list.html", context=Reports.data)

        data = Sale.objects.filter(sale_date__range=[date_start, date_end]).select_related('tour') \
            .prefetch_related('tour__hotel') \
            .only("tour__hotel__hotel_name", "tour__hotel__city__country", "tour__transfer__transfer_type",
                  "tour__tour_cost", "sale_date").order_by('sale_date')
        if (not data):
            pdf.cell(190, 15,
                     txt='Проданые туры в этот промежуток времени отсутствуют',
                     align='C')
        else:
            if (date_start == date_end):
                pdf.cell(190, 15,
                     txt="Отчет по количеству проданых туров за {}".format(
                         datetime.strptime(date_start, '%Y-%m-%d').date().strftime("%d.%m.%Y")),
                     ln=1, align='C')
            else:
                pdf.cell(190, 15,
                     txt="Отчет по количеству проданых туров за период с {} по {}".format(
                         datetime.strptime(date_start, '%Y-%m-%d').date().strftime("%d.%m.%Y"),
                         datetime.strptime(date_end, '%Y-%m-%d').date().strftime("%d.%m.%Y")),
                     ln=1, align='C')

            pdf.set_font_size(size=12)
            row_height = pdf.font_size * 2
            i = 0
            sum = 0
            pdf.cell(7, row_height, txt="№", border=1, align='C')
            pdf.cell(70, row_height, txt="Отель", border=1, align='C')
            pdf.cell(40, row_height, txt="Страна", border=1, align='C')
            pdf.cell(30, row_height, "Траспорта", border=1, align='C')
            pdf.cell(25, row_height, txt="Стоимость", border=1, align='C')
            pdf.cell(25, row_height, txt="Дата", border=1, align='C', ln=1)
            for row in data:
                i += 1
                pdf.cell(7, row_height, txt="{}".format(i), border=1, align='C')
                pdf.cell(70, row_height, txt="{}".format(row.tour.hotel.hotel_name), border=1, align='C')
                pdf.cell(40, row_height, txt="{}".format(row.tour.hotel.city.country), border=1, align='C')
                pdf.cell(30, row_height, txt="{}".format(row.tour.transfer.transfer_type), border=1, align='C')
                pdf.cell(25, row_height, txt="{}".format(row.tour.tour_cost), border=1, align='C')
                pdf.cell(25, row_height, txt="{}".format(row.sale_date.strftime("%d.%m.%Y")), border=1, align='C')
                sum += row.tour.tour_cost
                pdf.ln(row_height)
            if (i != 0):
                pdf.set_font_size(size=14)
                pdf.ln(4)
                pdf.cell(160, 6, txt="Итого продано {} туров на сумму: ".format(i), align='R')
                pdf.cell(35, 6, txt="{} {}".format(sum, "руб"), border='B', align='R')

        response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
        response['Content-Type'] = 'application/pdf'
        return response

    def pdf_view_tour_hotel(request):
        pdf = HtmlPdf('P', 'mm', 'A4')
        pdf.add_page()
        pdf.add_font('TimesNewRoman', '', 'templates/font/TimesNewRoman.ttf', uni=True)
        pdf.set_font('TimesNewRoman', '', 16)
        date_start = request.GET['data_start']
        date_end = request.GET['data_end']
        hotel = request.GET['hotel']
        if ((not date_start) | (not date_end)):
            Reports.data.update({'error_message': "Не правильно выбрана дата"})
            return render(request, "admin/reports_list.html", context=Reports.data)

        data = Sale.objects.filter(sale_date__range=[date_start, date_end], tour__hotel=hotel).select_related('tour') \
            .prefetch_related('tour__hotel') \
            .only("tour__hotel__hotel_name", "tour__hotel__city__country", "tour__transfer__transfer_type",
                  "tour__tour_tourists", "tour__tour_cost", "sale_date")

        if (not data):
            pdf.cell(190, 15,
                     txt='Проданые туры в этот отель отсутствуют',
                     align='C')
        else:
            if (date_start == date_end):
                pdf.cell(190, 15,
                         txt='Отчет по количеству проданых туров за период в отель:',
                         align='C')
                pdf.ln(9)
                pdf.cell(190, 15,
                         txt='"{}" за {}'.format(data[0].tour.hotel.hotel_name,
                                                 datetime.strptime(date_start, '%Y-%m-%d').date().strftime("%d.%m.%Y")),
                         ln=1, align='C')
            else:
                pdf.cell(190, 15,
                         txt='Отчет по количеству проданых туров за период в отель:',
                         align='C')
                pdf.ln(9)
                pdf.cell(190, 15,
                         txt='"{}" с {} по {}'.format(data[0].tour.hotel.hotel_name,
                                                      datetime.strptime(date_start, '%Y-%m-%d').date().strftime(
                                                          "%d.%m.%Y"),
                                                      datetime.strptime(date_end, '%Y-%m-%d').date().strftime(
                                                          "%d.%m.%Y")),
                         ln=1, align='C')

            pdf.set_font_size(size=12)
            row_height = pdf.font_size * 2
            i = 0
            sum = 0
            pdf.cell(7, row_height, txt="№", border=1, align='C')
            pdf.cell(70, row_height, txt="Отель", border=1, align='C')
            pdf.cell(40, row_height, txt="Страна", border=1, align='C')
            pdf.cell(30, row_height, "Траспорта", border=1, align='C')
            pdf.cell(25, row_height, txt="Стоимость", border=1, align='C')
            pdf.cell(25, row_height, txt="Дата", border=1, align='C', ln=1)
            for row in data:
                i += 1
                pdf.cell(7, row_height, txt="{}".format(i), border=1, align='C')
                pdf.cell(70, row_height, txt="{}".format(row.tour.hotel.hotel_name), border=1, align='C')
                pdf.cell(40, row_height, txt="{}".format(row.tour.hotel.city.country), border=1, align='C')
                pdf.cell(30, row_height, txt="{}".format(row.tour.transfer.transfer_type), border=1, align='C')
                pdf.cell(25, row_height, txt="{}".format(row.tour.tour_cost), border=1, align='C')
                pdf.cell(25, row_height, txt="{}".format(row.sale_date.strftime("%d.%m.%Y")), border=1, align='C')
                sum += row.tour.tour_cost
                pdf.ln(row_height)
            if (i != 0):
                pdf.set_font_size(size=14)
                pdf.ln(4)
                pdf.cell(160, 6, txt="Итого продано {} туров на сумму: ".format(i), align='R')
                pdf.cell(35, 6, txt="{} {}".format(sum, "руб"), border='B', align='R')

        response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
        response['Content-Type'] = 'application/pdf'
        return response

    def pdf_view_tour_country(request):
        pdf = HtmlPdf('P', 'mm', 'A4')
        pdf.add_page()
        pdf.add_font('TimesNewRoman', '', 'templates/font/TimesNewRoman.ttf', uni=True)
        pdf.set_font('TimesNewRoman', '', 16)
        date_start = request.GET['data_start']
        date_end = request.GET['data_end']
        country = request.GET['country']
        if ((not date_start) | (not date_end)):
            Reports.data.update({'error_message': "Не правильно выбрана дата"})
            return render(request, "admin/reports_list.html", context=Reports.data)

        data = Sale.objects.filter(sale_date__range=[date_start, date_end],
                                   tour__hotel__city__country=country).select_related('tour') \
            .prefetch_related('tour__hotel') \
            .only("tour__hotel__hotel_name", "tour__hotel__city__country", "tour__transfer__transfer_type",
                  "tour__tour_tourists", "tour__tour_cost", "sale_date")

        if (not data):
            pdf.cell(190, 15,
                     txt='Проданые туры в эту страну отсутствуют',
                     align='C')
        else:
            if (date_start == date_end):
                pdf.cell(190, 15,
                         txt='Отчет по количеству проданых туров за период в страну:',
                         align='C')
                pdf.ln(9)
                pdf.cell(190, 15,
                         txt='"{}" за {}'.format(data[0].tour.hotel.city.country,
                                                 datetime.strptime(date_start, '%Y-%m-%d').date().strftime("%d.%m.%Y")),
                         ln=1, align='C')
            else:
                pdf.cell(190, 15,
                         txt='Отчет по количеству проданых туров за период в страну:',
                         align='C')
                pdf.ln(9)
                pdf.cell(190, 15,
                         txt='"{}" с {} по {}'.format(data[0].tour.hotel.city.country,
                                                      datetime.strptime(date_start, '%Y-%m-%d').date().strftime(
                                                          "%d.%m.%Y"),
                                                      datetime.strptime(date_end, '%Y-%m-%d').date().strftime(
                                                          "%d.%m.%Y")),
                         ln=1, align='C')

            pdf.set_font_size(size=12)
            row_height = pdf.font_size * 2
            i = 0
            sum = 0
            pdf.cell(7, row_height, txt="№", border=1, align='C')
            pdf.cell(70, row_height, txt="Отель", border=1, align='C')
            pdf.cell(40, row_height, txt="Страна", border=1, align='C')
            pdf.cell(30, row_height, "Траспорта", border=1, align='C')
            pdf.cell(25, row_height, txt="Стоимость", border=1, align='C')
            pdf.cell(25, row_height, txt="Дата", border=1, align='C', ln=1)
            for row in data:
                i += 1
                pdf.cell(7, row_height, txt="{}".format(i), border=1, align='C')
                pdf.cell(70, row_height, txt="{}".format(row.tour.hotel.hotel_name), border=1, align='C')
                pdf.cell(40, row_height, txt="{}".format(row.tour.hotel.city.country), border=1, align='C')
                pdf.cell(30, row_height, txt="{}".format(row.tour.transfer.transfer_type), border=1, align='C')
                pdf.cell(25, row_height, txt="{}".format(row.tour.tour_cost), border=1, align='C')
                pdf.cell(25, row_height, txt="{}".format(row.sale_date.strftime("%d.%m.%Y")), border=1, align='C')
                sum += row.tour.tour_cost
                pdf.ln(row_height)
            if (i != 0):
                pdf.set_font_size(size=14)
                pdf.ln(4)
                pdf.cell(160, 6, txt="Итого продано {} туров на сумму: ".format(i), align='R')
                pdf.cell(35, 6, txt="{} {}".format(sum, "руб"), border='B', align='R')

        response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
        response['Content-Type'] = 'application/pdf'
        return response

    def pdf_view_tour_discount(request):
        pdf = HtmlPdf('P', 'mm', 'A4')
        pdf.add_page()
        pdf.add_font('TimesNewRoman', '', 'templates/font/TimesNewRoman.ttf', uni=True)
        pdf.set_font('TimesNewRoman', '', 16)
        date_start = request.GET['data_start']
        date_end = request.GET['data_end']
        discount = request.GET['discount']
        if ((not date_start) | (not date_end)):
            Reports.data.update({'error_message': "Не правильно выбрана дата"})
            return render(request, "admin/reports_list.html", context=Reports.data)

        data = Sale.objects.filter(sale_date__range=[date_start, date_end],
                                   tour__discount=discount).select_related('tour') \
            .prefetch_related('tour__hotel') \
            .only("tour__hotel__hotel_name", "tour__hotel__city__country", "tour__transfer__transfer_type",
                  "tour__tour_tourists", "tour__tour_cost", "sale_date", "tour__discount")

        if (not data):
            pdf.cell(190, 15,
                     txt='Проданые туры по этой акции отсутствуют',
                     align='C')
        else:
            if (date_start == date_end):
                pdf.cell(190, 15,
                         txt='Отчет по количеству проданых туров за период по акции:',
                         align='C')
                pdf.ln(9)
                pdf.cell(190, 15,
                         txt='"{}" за {}'.format(data[0].tour.discount,
                                                 datetime.strptime(date_start, '%Y-%m-%d').date().strftime("%d.%m.%Y")),
                         ln=1, align='C')
            else:
                pdf.cell(190, 15,
                         txt='Отчет по количеству проданых туров за период по акции:',
                         align='C')
                pdf.ln(9)
                pdf.cell(190, 15,
                         txt='"{}" с {} по {}'.format(data[0].tour.discount,
                                                      datetime.strptime(date_start, '%Y-%m-%d').date().strftime(
                                                          "%d.%m.%Y"),
                                                      datetime.strptime(date_end, '%Y-%m-%d').date().strftime(
                                                          "%d.%m.%Y")),
                         ln=1, align='C')

            pdf.set_font_size(size=12)
            row_height = pdf.font_size * 2
            i = 0
            sum = 0
            pdf.cell(7, row_height, txt="№", border=1, align='C')
            pdf.cell(70, row_height, txt="Отель", border=1, align='C')
            pdf.cell(40, row_height, txt="Страна", border=1, align='C')
            pdf.cell(30, row_height, "Траспорта", border=1, align='C')
            pdf.cell(25, row_height, txt="Стоимость", border=1, align='C')
            pdf.cell(25, row_height, txt="Дата", border=1, align='C', ln=1)
            for row in data:
                i += 1
                pdf.cell(7, row_height, txt="{}".format(i), border=1, align='C')
                pdf.cell(70, row_height, txt="{}".format(row.tour.hotel.hotel_name), border=1, align='C')
                pdf.cell(40, row_height, txt="{}".format(row.tour.hotel.city.country), border=1, align='C')
                pdf.cell(30, row_height, txt="{}".format(row.tour.transfer.transfer_type), border=1, align='C')
                pdf.cell(25, row_height, txt="{}".format(row.tour.tour_cost), border=1, align='C')
                pdf.cell(25, row_height, txt="{}".format(row.sale_date.strftime("%d.%m.%Y")), border=1, align='C')
                sum += row.tour.tour_cost
                pdf.ln(row_height)
            if (i != 0):
                pdf.set_font_size(size=14)
                pdf.ln(4)
                pdf.cell(160, 6, txt="Итого продано {} туров на сумму: ".format(i), align='R')
                pdf.cell(35, 6, txt="{} {}".format(sum, "руб"), border='B', align='R')

        response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
        response['Content-Type'] = 'application/pdf'
        return response
