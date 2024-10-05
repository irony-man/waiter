# Standard Library
from typing import List, Optional

# App Imports
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from loguru import logger


def safe_send_email(
    template,
    context: dict,
    subj: str,
    to: List[str],
    cc=None,
    bcc=None,
    attachments: Optional[List] = None,
):
    txt = render_to_string(f"{template}.txt", context)
    html = render_to_string(f"{template}.html", context)
    if settings.ENABLE_OUTGOING_EMAIL:
        message = EmailMultiAlternatives(
            subject=subj,
            body=txt,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to,
            cc=cc,
            bcc=bcc,
        )
        message.attach_alternative(html, "text/html")
        if attachments:
            for item in attachments:
                data = item["file"]
                if hasattr(item["file"], "read"):
                    data = item["file"].read()
                message.attach(item["filename"], data, item["content_type"])
        message.send(fail_silently=False)
    else:
        logger.warning(
            "Outgoing email disabled via env var ENABLE_OUTGOING_EMAIL"
        )
