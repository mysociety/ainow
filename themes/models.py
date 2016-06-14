from django.db import models

from markitup.fields import MarkupField
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
        help_text='The page title that will be shown to the user when they view this theme.'
    )
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=True,
        populate_from='title',
        help_text="Used to make a nice url for this Theme's page."
    )
    content = MarkupField(blank=True)
    schedules = models.ManyToManyField(
        'conference.Schedule',
        blank=True,
        help_text="Which schedules is this related to?"
                         " If a schedule is private, this theme will be kept private too, but"
                         " only when viewing it in that context.<br><br>"
                         " You probably only want to select multiple schedules if this theme is"
                         " shared between all schedules.<br><br>"
    )

    def __str__(self):
        return self.name


class Document(TimestampedModel):
    name = models.CharField(
        max_length=1024,
        help_text='An internal name for this document, to help identify it.',
        blank=True
    )
    title = models.CharField(
        max_length=1024,
        help_text='The title for this document that will be shown to the user.'
    )
    description = MarkupField(blank=True)
    file = models.FileField(upload_to='documents/')
    theme = models.ForeignKey('Theme', related_name='documents')

    def __str__(self):
        return self.name
