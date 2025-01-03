# # Standard Library
import io
import secrets
import string

import qrcode
from django.conf import settings
from django.utils import timezone
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer

qr_base_url = f"{settings.BASE_URL}/table/"

systemRandom = secrets.SystemRandom()


def random_pin() -> int:
    return systemRandom.randint(100000, 999999)


def generate_username():
    adjectives = [
        "Cool",
        "Fast",
        "Silly",
        "Smart",
        "Brave",
        "Clever",
        "Sneaky",
    ]
    nouns = ["Tiger", "Panda", "Ninja", "Robot", "Eagle", "Wizard", "Phoenix"]
    numbers = "".join(systemRandom.choices(string.digits, k=3))

    adjective = systemRandom.choice(adjectives)
    noun = systemRandom.choice(nouns)

    return f"{adjective}{noun}{numbers}"


def generate_chain_name():
    adjectives = [
        "Tasty",
        "Golden",
        "Spicy",
        "Savory",
        "Fresh",
        "Urban",
        "Classic",
    ]
    nouns = ["Bite", "Table", "Grill", "Kitchen", "Feast", "Flavors", "Diner"]
    suffixes = ["Co.", "House", "Hub", "Express", "Corner", "Palace", "Spot"]

    adjective = systemRandom.choice(adjectives)
    noun = systemRandom.choice(nouns)
    suffix = systemRandom.choice(suffixes)

    return f"{adjective} {noun} {suffix}"


def attach_qr(text: str):
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    QRcode.add_data(f"{qr_base_url}{text}")
    QRcode.make(fit=True)
    QRimg = QRcode.make_image(
        image_factory=StyledPilImage,
        module_drawer=CircleModuleDrawer(),
    )
    bytes_buffer = io.BytesIO()
    QRimg.save(bytes_buffer, "PNG")
    return bytes_buffer


def now_time():
    return timezone.now()
