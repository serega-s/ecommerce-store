from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from .models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

# class CustomUserChangeForm(UserChangeForm):
#     first_name = forms.CharField(max_length=50, required=True)
#     last_name = forms.CharField(max_length=50, required=True)
#     email = forms.EmailField(max_length=255, required=True)
#
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'email']
