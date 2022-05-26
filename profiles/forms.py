""" Forms for profiles """

from django import forms
from .models import UserProfile, UserComment


class UserProfileForm(forms.ModelForm):
    """ User profile update info """

    class Meta:
        """ setup form fields for profile """
        model = UserProfile
        fields = ['city', 'country']


class ProductionCommentForm(forms.ModelForm):
    """ User comment on production """

    class Meta:
        """ setup form fields for comments """
        model = UserComment
        fields = ['comment']

    comment = forms.CharField(widget=forms.Textarea(attrs={
                                                           'name': 'comment',
                                                           'rows': '3',
                                                           'cols': '5'}))
