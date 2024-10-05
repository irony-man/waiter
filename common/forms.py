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
    phone = CharField()

    class Meta:
        model = LoginPinRequest
        fields = ("phone",)

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone.startswith("322"):
            # Note: Dummy numbers on-demand
            return phone
        try:
            phone_obj = to_python(phone)
        except TypeError as exc:
            raise ValidationError(f"Error processing phone: {exc}")
        else:
            if isinstance(phone_obj, PhoneNumber) and not phone_obj.is_valid():
                raise ValidationError(
                    _("The phone number entered is not valid."),
                    code="invalid_phone_number",
                )
            return phonenumbers.format_number(
                phone_obj, phonenumbers.PhoneNumberFormat.E164
            )

    def clean(self):
        if phone := self.cleaned_data.get("phone"):
            self.cleaned_data[
                "instance"
            ] = LoginPinRequest.rate_limited_create(phone=phone)
        return self.cleaned_data
