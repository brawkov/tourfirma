from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee

class CustomUserCreationForm(UserCreationForm):


    class Meta(UserCreationForm):
        model = Employee
        fields = ('username', 'employee_passp_id')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        #fields = ('username', 'employee_passp_id')
        fields = '__all__'
