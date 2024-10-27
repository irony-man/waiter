from typing import Any, Dict, List

from django.db.models import TextChoices
from django.utils.translation import gettext as _


def serialize(klass) -> List[Dict[str, Any]]:
    return [
        {"name": x[1], "value": x[0]} for x in getattr(klass, "choices", [])
    ]


class MenuType(TextChoices):
    VEG = "VEG", _("Veg")
    NON_VEG = "NON_VEG", _("Non Veg")


class PriceType(TextChoices):
    HALF = "HALF", _("Half")
    FULL = "FULL", _("Full")


class OrderStatus(TextChoices):
    PENDING = "PENDING", _("Pending")
    ACCEPTED = "ACCEPTED", _("Accepted")
    REJECTED = "REJECTED", _("Rejected")
    MAKING = "MAKING", _("Making")
    EXPIRED = "EXPIRED", _("Expired")
    COMPLETED = "COMPLETED", _("Completed")
