from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField()
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = "__all__"