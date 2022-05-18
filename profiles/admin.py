from django.contrib import admin
from .models import UserProfile, UserLike, UserComment


class UserCommentAdmin(admin.ModelAdmin):
    """
    User comment admin list
    """
    list_display = (
        'user',
        'production',
        'comment',
        'record_added',
        'record_edited',
    )

    ordering = ('record_added',)


class UserLikeAdmin(admin.ModelAdmin):
    """
    User like admin list
    """
    list_display = (
        'user',
        'production',
    )

    ordering = ('user',)


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserLike,UserLikeAdmin)
admin.site.register(UserComment,UserCommentAdmin)
