from django.contrib.auth.models import Permission
from django.shortcuts import render

from dal import autocomplete
from client.models import Client


class ClientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Client.objects.none()
        qs = Client.objects.all()
        # if self.q:
        #     qs = qs.filter(title__istartswith=self.q)

        return qs
