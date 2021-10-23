from django.urls import path
from . import views

urlpatterns = [
    path('listing/create', views.create_listing),
    path('search', views.search_listings),
]