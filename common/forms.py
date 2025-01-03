# App Imports
from django import forms
from django.forms import BooleanField, CharField
from django.utils.translation import gettext as _


class LoginForm(forms.Form):
    username = CharField(required=False)
    password = CharField(required=False)
    is_guest = BooleanField(required=False)

    class Meta:
        fields = ("username", "password", "is_guest")
