import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# 1. Set settings FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_guidance_system.settings')

# 2. Initialize Django BEFORE importing anything that touches models
django_asgi_app = get_asgi_application()

# 3. NOW it's safe to import Django-dependent modules
from notifications.middleware import JWTAuthMiddleware
from notifications.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})