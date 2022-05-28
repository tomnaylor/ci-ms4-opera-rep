from django.contrib import admin
from django.utils.html import format_html
from .models import (
                     Work,
                     Production,
                     ProductionVideo,
                     ProductionPhoto,
                     People,
                     Role)


class ProductionPhotoAdmin(admin.ModelAdmin):
    """
    Production photo admin list
    """
    list_display = (
        'production',
        'name',
        'photo',
        'rating_total',
        'rating_count',
        'record_added',
        'record_edited',
    )

    # show photo in the admin table
    def photo(self, obj):
        """ Show image in list """
        return format_html('<img src="%s" title="%s" style="height:80px" />' %
                           (obj.thumb_image.url, obj.name))

    photo.allow_tags = True
    ordering = ('record_added',)


class PeopleAdmin(admin.ModelAdmin):
    """
    People admin list
    """
    list_display = (
        'name',
        'photo',
        'facebook',
        'twitter',
        'record_added',
        'record_edited',
    )

    # show photo in the admin table
    def photo(self, obj):
        """ Show image in list """
        return format_html(
                           '<img src="%s" title="%s" style="height:50px" />' %
                           (obj.thumb_image_url, obj.name))

    photo.allow_tags = True
    ordering = ('name',)


admin.site.register(Work)
admin.site.register(Production)
admin.site.register(ProductionVideo)
admin.site.register(ProductionPhoto, ProductionPhotoAdmin)
admin.site.register(People, PeopleAdmin)
admin.site.register(Role)
