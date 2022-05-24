from django import forms
from .models import UserProfile, UserComment


class UserProfileForm(forms.ModelForm):
    """ User profile update info """
    
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        
        super().__init__(*args, **kwargs)
        placeholders = {
            # 'default_phone_number': 'Phone Number',
            # 'default_postcode': 'Postal Code',
            'city': 'Town or City',
            # 'default_street_address1': 'Street Address 1',
            # 'default_street_address2': 'Street Address 2',
            'country': 'Country',
        }

        # self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]

                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = ('border-black '
                                                        'rounded-0 '
                                                        'profile-form-input')
            self.fields[field].label = False


class ProductionCommentForm(forms.ModelForm):
    """ User comment on production """
    
    class Meta:
        model = UserComment
        exclude = ('user','production')

    comment = forms.CharField(widget=forms.Textarea(attrs={ 'name': 'comment', 'rows': '3', 'cols': '5' }))