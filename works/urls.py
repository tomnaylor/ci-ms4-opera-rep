from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_works, name='works'),
    path('search', views.search, name='search'),
    path('productions/<slug:slug>', views.production, name='production'),
    path('person/<slug:slug>', views.person, name='person'),
    path('productions', views.all_productions, name='productions'),
]
