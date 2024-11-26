"""
ASGI config for waiter project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from dotenv import load_dotenv

load_dotenv()
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "waiter.settings")

asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter  # type: ignore

from common.routing import routes

application = ProtocolTypeRouter(
    {
        "http": asgi_app,
        "websocket": routes,
    }
)
