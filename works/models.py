from django.db import models
from django.conf import settings


# ------------------------------ PEOPLE

def people_thumb_image_path(instance, filename):
    """ Return path for people hero images to be saved """
    return f'people/{instance.url}/thumbs/{filename}'


class People(models.Model):
    """ Model for all people in productions - ie. Directors, cast, creatives etc.. """
    name = models.CharField(max_length=254, blank=False)
    url = models.SlugField(max_length=254, blank=False, unique=True)
    thumb_image = models.ImageField(null=True, blank=True, upload_to=people_thumb_image_path)
    synopsis = models.TextField(null=True, blank=True)
    facebook = models.SlugField(max_length=254, null=True, blank=True, help_text="Only the username portion of the URL", verbose_name="Facebook username")
    twitter = models.SlugField(max_length=254, null=True, blank=True, help_text="Only the username portion of the URL (no @ or #)", verbose_name="Twitter username")
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    @property
    def thumb_image_url(self):
        """ Returns URL to thumbnail or a default no imaage placeholder """
        if self.thumb_image:
            return self.thumb_image.url

        return settings.STATIC_URL + "template/no-image.png"


# ------------------------------ ROLES -> PEOPLE

class Role(models.Model):
    """ Model for all roles in a productions """
    name = models.CharField(max_length=254, blank=False)
    person = models.ForeignKey('People', on_delete=models.RESTRICT)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.person.name + ' - ' + self.name


# ------------------------------ WORKS

class Work(models.Model):
    """ Model for the work """
    url = models.SlugField(max_length=254, blank=False, unique=True)
    name = models.CharField(max_length=254, blank=False)
    composer = models.ForeignKey('People', on_delete=models.RESTRICT)
    world_premiere = models.DateField(auto_now=False, auto_now_add=False)
    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


# ------------------------------ PRODUCTION

def production_hero_image_path(instance, filename):
    """ Return path for production hero images to be saved """
    return f'production/{instance.url}/heros/{filename}'


def production_thumb_image_path(instance, filename):
    """ Return path for production hero images to be saved """
    return f'production/{instance.url}/thumbs/{filename}'


class Production(models.Model):
    """ Model for a production """
    url = models.SlugField(max_length=254, blank=False, unique=True)
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
        """ Returns URL to thumbnail or a default no image placeholder """
        if self.thumb_image:
            return self.thumb_image.url

        return settings.STATIC_URL + "template/no-image.png"


# ------------------------------ PRODUCTION PHOTOS

def production_photo_full_image_path(instance, filename):
    """ Return path for production full photo images to be saved """
    return f'production/{instance.production.url}/photos/full/{filename}'


def production_photo_thumb_image_path(instance, filename):
    """ Return path for production thumb photo images to be saved """
    return f'production/{instance.production.url}/photos/thumbs/{filename}'


class ProductionPhoto(models.Model):
    """ Model for a media entry for a production """

    production = models.ForeignKey('Production', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254, blank=False)
    full_image = models.ImageField(null=True, blank=True, upload_to=production_photo_full_image_path)
    thumb_image = models.ImageField(null=True, blank=True, upload_to=production_photo_thumb_image_path)
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


# ------------------------------ PRODUCTION VIDEOS

def production_video_thumb_image_path(instance, filename):
    """ Return path for production thumb video images to be saved """
    return f'production/{instance.production.url}/videos/thumbs/{filename}'


class ProductionVideo(models.Model):
    """ Model for a video entry for a production """

    production = models.ForeignKey('Production', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254, blank=False)
    source = models.TextField(max_length=2000, blank=True, null=True)
    youtube_source = models.CharField(max_length=100, blank=True, null=True, help_text="https://www.youtube.com/embed/")
    thumb_image = models.ImageField(null=True, blank=True, upload_to=production_video_thumb_image_path)
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
