from django.db import models

from markitup.fields import MarkupField
from autoslug import AutoSlugField

from ainow.models import TimestampedModel


class Block(TimestampedModel):
    name = models.CharField(
        max_length=1024,
        help_text='An internal name for this block of content, to help identify it.',
        blank=False
    )
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=False,
        populate_from='name',
        help_text="Used to identify this block of content when we include it in pages."
    )
    content = MarkupField(blank=True)

    def __str__(self):
        return self.name
