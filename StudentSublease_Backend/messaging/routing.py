from django.urls import re_path
from django.urls import path

from .consumers import MessageConsumer

websocket_urlpatterns = [
    path('ws/messages/<str:conversation>/<int:user>', MessageConsumer.as_asgi()),
]
