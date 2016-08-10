from django.db import models

from markitup.fields import MarkupField
from autoslug import AutoSlugField

from ainow.models import TimestampedModel


class Category(TimestampedModel):
    name = models.CharField(
        max_length=1024,
        help_text='An internal name for this category, to help identify it.',
        blank=True
    )
    title = models.CharField(
        max_length=1024,
        help_text='The title for this category that will be shown to the user.'
    )
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=False,
        populate_from='title',
        help_text="Used to identify this category when we link to it."
    )
    introduction = MarkupField(
        blank=True,
        help_text='This will be shown above the documents in this category.'
    )

    class Meta:
        verbose_name_plural = "categories"

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
    category = models.ForeignKey('Category', related_name='documents')

    def __str__(self):
        return self.name
