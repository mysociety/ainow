from django.db import models

from markitup.fields import MarkupField
from autoslug import AutoSlugField

from ainow.models import TimestampedModel


class Page(TimestampedModel):
    name = models.CharField(
        max_length=1024,
        help_text='An internal name for this page, to help identify it.',
        blank=True
    )
    title = models.CharField(
    	max_length=1024, 
    	help_text='The page title that will be shown to the user.'
    )
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=True,
        populate_from='title',
        help_text="Used to make a nice url for this Page."
    )
    content = MarkupField(blank=True)
    parent_page = models.ForeignKey(
    	"self", 
    	help_text="If this page belongs in a section underneath another, choose that parent page here.",
    	related_name='sub_pages',
    	blank=True,
    	null=True
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

