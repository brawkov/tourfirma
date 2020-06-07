from attr import attrs
from dal import autocomplete
from django import forms

from client.models import Client
from sale.models import Sale


class saleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['client_passp', 'tour']


