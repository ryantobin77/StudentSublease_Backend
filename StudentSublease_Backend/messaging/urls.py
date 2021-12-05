from django.urls import path
from . import views

urlpatterns = [
    path('messages', views.get_messages),
    path('conversations', views.get_conversations),
    path('conversation/new', views.start_conversation)
]
