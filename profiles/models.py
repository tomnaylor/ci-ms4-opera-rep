from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

from works.models import Production



class UserProfile(models.Model):
    """
    User profiles for restricted access and saving favourites
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    # default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    # default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    # default_postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False, default="GB")

    def __str__(self):
        return self.user.username + ' - ' + self.user.email


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()


class UserLike(models.Model):
    """
    Likes for productions
    """
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    production = models.ForeignKey('works.Production', on_delete=models.RESTRICT)

    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' - ' + self.user.email


class UserComment(models.Model):
    """
    comments for productions
    """
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    production = models.ForeignKey('works.Production', on_delete=models.RESTRICT)
    comment = models.CharField(max_length=600, null=False, blank=False)

    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' regarding ' + self.production.work.name + ' wrote: ' + self.comment
    
    class Meta:
        unique_together = ('user', 'production',)