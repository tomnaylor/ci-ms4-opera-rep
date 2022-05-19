from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation, name='donation'),
]
