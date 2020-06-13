from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def show_admin_custom_page(request):
    # some code
    ctx = {'data': 'test'}
    return render(request, 'admin/base.html', ctx)