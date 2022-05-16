from django.db import models
from django.conf import settings


class People(models.Model):
    """ Model for all people in productions - ie. Directors, cast, creatives etc.. """
    url = models.SlugField(max_length=254, blank=False)
    tagline = models.CharField(max_length=254, null=True, blank=True)
    facebook = models.SlugField(max_length=254, null=True, blank=True)
    twitter = models.SlugField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254, blank=False)
    synopsis = models.TextField(null=True, blank=True)
    hero_image_url = models.URLField(max_length=1024, null=True, blank=True)
    thumb_image_url = models.URLField(max_length=1024, null=True, blank=True)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def thumb_image(self):
        """ Returns URL to thumbnail or a default no imaage placeholder """
        if self.thumb_image_url:
            return self.thumb_image_url

        return settings.MEDIA_URL + "no-image.png"


class Role(models.Model):
    """ Model for all roles in a productions """
    name = models.CharField(max_length=254, blank=False)
    person = models.ForeignKey('People', on_delete=models.RESTRICT)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.person.name + ' - ' + self.name


class Work(models.Model):
    """ Model for the work """

    url = models.SlugField(max_length=254, blank=False)
    name = models.CharField(max_length=254, blank=False)
    composer = models.CharField(max_length=100, blank=False)
    librettist = models.CharField(max_length=100, blank=False)
    world_premiere = models.DateField(auto_now=False, auto_now_add=False)
    hero_image_url = models.URLField(max_length=1024, null=True, blank=True)
    thumb_image_url = models.URLField(max_length=1024, null=True, blank=True)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    @property
    def image_url(self):
        """ Returns URL to thumbnail or a default no imaage placeholder """
        if self.thumb_image_url:
            return self.thumb_image_url

        return settings.MEDIA_URL + "no-image.png"


def production_hero_image_path(instance, filename):
    """ Return path for production hero images to be saved """
    return f'production/{instance.url}/heros/{filename}'


def production_thumb_image_path(instance, filename):
    """ Return path for production hero images to be saved """
    return f'production/{instance.url}/thumbs/{filename}'


class Production(models.Model):
    """ Model for a production """

    url = models.SlugField(max_length=254, blank=False)
    work = models.ForeignKey('Work', null=True, blank=True, on_delete=models.SET_NULL)
    year = models.PositiveSmallIntegerField()
    synopsis = models.TextField()
    tagline = models.CharField(max_length=254, blank=False)
    hash_tag = models.CharField(max_length=30, blank=False)
    language = models.CharField(max_length=100, blank=False)
    production_premiere = models.DateField(auto_now=False, auto_now_add=False)
    creatives = models.ManyToManyField(Role, related_name='creatives', blank=True)
    cast = models.ManyToManyField(Role, related_name='cast', blank=True)
    staff = models.ManyToManyField(Role, related_name='staff', blank=True)
    dead = models.BooleanField(default=False, null=True, blank=True)
    hero_image = models.ImageField(null=True, blank=True, upload_to=production_hero_image_path)
    thumb_image = models.ImageField(null=True, blank=True, upload_to=production_thumb_image_path)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)
    rating_total = models.PositiveIntegerField(null=True, blank=True)
    rating_count = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.work.name + " (" + str(self.year) + ")"

    @property
    def thumb_image_url(self):
        """ Returns URL to thumbnail or a default no imaage placeholder """
        if self.thumb_image:
            return self.thumb_image.url

        return settings.STATIC_URL + "template/no-image.png"



class ProductionMedia(models.Model):
    """ Model for a media entry for a production """

    MEDIA_TYPES = (
        ('P', 'photo'),
        ('V', 'video'),
        ('F', 'pdf'),
    )
    type = models.CharField(max_length=1, choices=MEDIA_TYPES)
    production = models.ForeignKey('Production', null=True, blank=True, on_delete=models.SET_NULL)
    url = models.CharField(max_length=254, blank=False)
    name = models.CharField(max_length=254, blank=False)
    thumb_image = models.ImageField(null=True, blank=True)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)
    rating_total = models.PositiveIntegerField(null=True, blank=True)
    rating_count = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name + " (" + self.production.work.name + \
            " - " + str(self.production.year) + ")"

    @property
    def thumb_image_url(self):
        """ Returns URL to thumbnail or a default no imaage placeholder """
        if self.thumb_image:
            return self.thumb_image.url

        return settings.STATIC_URL + "template/no-image.png"
