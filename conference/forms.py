from django import forms
from django.core.files.images import get_image_dimensions

from .models import Attendee


class AttendeeForm(forms.ModelForm):
    """A custom form for attendees"""

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if photo:
            w, h = get_image_dimensions(photo)
            if w < 500 or h < 500:
                raise forms.ValidationError("Do you have a bigger picture? Photos must be at least 500px by 500px.")
        return photo

    class Meta:
        model = Attendee
        fields = ['user', 'name', 'title', 'organisation', 'biography', 'photo', 'twitter_username']
        widgets = {
            'photo': forms.FileInput()
        }
        labels = {
            'organisation': 'Organization:',
            'biography': 'Bio:',
            'title': 'Job Title:'
        }
