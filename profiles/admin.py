from django.contrib import admin
from .models import UserProfile, UserLike

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserLike)
