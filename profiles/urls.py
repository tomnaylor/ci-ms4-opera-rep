from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('comment-delete/<int:comment_id>/', views.comment_remove, name='comment_remove'),
    path('comment-edit/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('comment-add/<int:prod_id>/', views.comment_add, name='comment_add'),
]
