from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_works, name='works'),
    path('productions/<slug:slug>', views.production, name='production'),
    path('person/<slug:slug>', views.person, name='person'),
    path('productions', views.all_productions, name='productions'),
    path('productions/media/<int:media_id>', views.production_media, name='production_media'),
]
