from django.db import models

from autoslug import AutoSlugField

from ainow.models import TimestampedModel


class Theme(TimestampedModel):
    name = models.CharField(
        max_length=1024,
        help_text='An internal name for this theme, to help identify it.',
        blank=True
    )
    title = models.CharField(
        max_length=1024,
        help_text='The title for this theme that will be shown to the user.'
    )
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=True,
        populate_from='title',
        help_text="Used to make a nice url for this Theme's page."
    )
    primer_title = models.CharField(
        max_length=1024,
        help_text='The title for the draft report document that will be shown to '
                  'the user.',
        blank=True
    )
    primer = models.FileField(upload_to='documents/', blank=True)

    def __str__(self):
        return self.name
