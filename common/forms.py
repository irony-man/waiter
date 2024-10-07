# App Imports
import phonenumbers
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.utils.translation import gettext as _
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python
from phonenumbers import PhoneNumber

from common.models import LoginPinRequest


class LoginForm(forms.Form):
    phone = PhoneNumberField()
    pin = forms.IntegerField(min_value=1000, max_value=9999)

    def clean(self):
        phone = self.cleaned_data["phone"]
        user = User.objects.filter(username=phone).first()
        if not user:
            raise ValidationError(
                {"pin": _("Incorrect or an expired pin.")}, code="invalid"
            )
        pin = self.cleaned_data.get("pin")
        instance = (
            LoginPinRequest.objects.filter(pin=pin, user__username=phone)
            .order_by("-generated_at")
            .first()
        )
        if instance and instance.is_valid(user=user):
            self.cleaned_data["user"] = user
            return self.cleaned_data
        raise ValidationError(
            {"pin": _("Incorrect or an expired pin.")}, code="invalid"
        )


class LoginPinRequestForm(forms.ModelForm):
    username = CharField(required=False)

    class Meta:
        model = User
        fields = ("username",)

    def clean(self):
        self.cleaned_data["instance"] = User.objects.all().first()
        return self.cleaned_data
