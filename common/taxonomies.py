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
