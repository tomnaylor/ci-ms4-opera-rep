from django.urls import path
from . import views
from .stripe_webhooks import webhook

urlpatterns = [
    path('', views.donation, name='donation'),
    path('<donation_number>', views.donation_success, name='donation_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('stripewh/', webhook, name='webhook'),
]
