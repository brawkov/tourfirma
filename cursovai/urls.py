"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url

from sale.views import ClientAutocomplete
from users.admin import admin_site

from django.contrib import admin
from django.urls import path, include

from django.views.generic.base import TemplateView
from report import views as ReportView

urlpatterns = [
    # url(r'^city-autocomplete/$', ClientAutocomplete.as_view(), name='city-autocomplete',),

    url(r'^', admin_site.urls),
    # url(r'^admin/', admin_site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'))),
    path('users/', include('django.contrib.auth.urls')),
    path('admin/reports/', ReportView.Reports.view, name='reports'),
    path('admin/report_all/', ReportView.Reports.pdf_view_tour_all, name='report_all'),
    path('admin/report_hotel/', ReportView.Reports.pdf_view_tour_hotel, name='report_hotel'),
    path('admin/report_country/', ReportView.Reports.pdf_view_tour_country, name='report_country'),
    path('admin/report_discount/', ReportView.Reports.pdf_view_tour_discount, name='report_discount'),
]
