# # Standard Library
import io
import secrets

import qrcode
from django.conf import settings
from django.utils import timezone
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer

qr_base_url = f"{settings.BASE_URL}/table/"


def random_pin() -> int:
    return secrets.SystemRandom().randint(100000, 999999)


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
