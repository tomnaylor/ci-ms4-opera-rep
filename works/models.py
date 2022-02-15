from django.db import models
from django.conf import settings


class People(models.Model):
    """ Model for all people in productions - ie. Directors, cast, creatives etc.. """
    url = models.SlugField(max_length=254, blank=False)
    facebook = models.SlugField(max_length=254, null=True, blank=True)
    twitter = models.SlugField(max_length=254, null=True, blank=True)

    name = models.CharField(max_length=254, blank=False)
    synopsis = models.TextField()

    hero_image = models.ImageField(null=True, blank=True)
    hero_image_url = models.URLField(max_length=1024, null=True, blank=True)
    thumb_image = models.ImageField(null=True, blank=True)
    thumb_image_url = models.URLField(max_length=1024, null=True, blank=True)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Work(models.Model):
    """ Model for the work """

    url = models.SlugField(max_length=254, blank=False)
    name = models.CharField(max_length=254, blank=False)
    synopsis = models.TextField()
    tagline = models.CharField(max_length=254, blank=False)
    hash_tag = models.CharField(max_length=30, blank=False)
    language = models.CharField(max_length=100, blank=False)
    composer = models.CharField(max_length=100, blank=False)
    librettist = models.CharField(max_length=100, blank=False)
    world_premiere = models.DateField(auto_now=False, auto_now_add=False)
    hero_image = models.ImageField(null=True, blank=True)
    hero_image_url = models.URLField(max_length=1024, null=True, blank=True)
    thumb_image = models.ImageField(null=True, blank=True)
    thumb_image_url = models.URLField(max_length=1024, null=True, blank=True)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    @property
    def image_url(self):
        """ Returns URL to thumbnail or a default no imaage placeholder """
        if self.thumb_image and hasattr(self.thumb_image, 'url'):
            return self.thumb_image.url

        return settings.MEDIA_URL + "no-image.png"


class Production(models.Model):
    """ Model for a production """

    work = models.ForeignKey(
        'Work', null=True, blank=True, on_delete=models.SET_NULL)
    year = models.PositiveSmallIntegerField()
    production_premiere = models.DateField(auto_now=False, auto_now_add=False)
    director = models.ForeignKey('People', null=True, blank=True, on_delete=models.SET_NULL)
    set_designer = models.CharField(max_length=100, null=True, blank=True)
    costume_designer = models.CharField(max_length=100, null=True, blank=True)
    lighting_designer = models.CharField(max_length=100, null=True, blank=True)
    relighter = models.CharField(max_length=100, null=True, blank=True)
    choreographer = models.CharField(max_length=100, null=True, blank=True)
    producer = models.CharField(max_length=100, null=True, blank=True)
    dead = models.BooleanField(default=False, null=True, blank=True)
    hero_image = models.ImageField(null=True, blank=True)
    hero_image_url = models.URLField(max_length=1024, null=True, blank=True)
    thumb_image = models.ImageField(null=True, blank=True)
    thumb_image_url = models.URLField(max_length=1024, null=True, blank=True)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.work.name + " (" + str(self.year) + ")"




class ProductionMedia(models.Model):
    """ Model for a media entry for a production """

    MEDIA_TYPES = (
        ('P', 'photo'),
        ('V', 'video'),
        ('F', 'pdf'),
    )
    type = models.CharField(max_length=1, choices=MEDIA_TYPES)
    production = models.ForeignKey(
        'Production', null=True, blank=True, on_delete=models.SET_NULL)
    url = models.CharField(max_length=254, blank=False)
    name = models.CharField(max_length=254, blank=False)
    thumb_image = models.ImageField(null=True, blank=True)
    thumb_image_url = models.URLField(max_length=1024, null=True, blank=True)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name + " (" + self.production.work.name + \
            " - " + str(self.production.year) + ")"


# Person model - artis, director etc.. . inc. social media details.