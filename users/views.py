from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from var_dump import var_dump

from .admin import admin_site
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
