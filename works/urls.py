from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_works, name='works'),
    path('productions', views.all_productions, name='productions'),
    path('productions/media/<int:media_id>', views.production_media, name='production_media'),
    path('productions/<slug:slug>/<int:production_id>', views.production, name='production'),
]
