from django.urls import path
from . import views

urlpatterns = [
    path('messages', views.get_messages),
    path('conversations', views.get_conversations),
    path('conversation/new', views.start_conversation),
    path('socket/test', views.test_web_socket)
]
