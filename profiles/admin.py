from django.contrib import admin
from .models import UserProfile, UserLike, UserComment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserLike)
admin.site.register(UserComment)
