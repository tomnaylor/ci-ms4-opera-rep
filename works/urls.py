from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_works, name='works'),
    path('productions', views.all_productions, name='productions'),
    #path('<int:product_id>/', views.product_detail, name='product_detail'),
]
