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
    schedules = models.ManyToManyField(
        'conference.Schedule',
        blank=True,
        help_text="Which schedules is this related to?"
                  " If a schedule is private, this page will be kept private too, but"
                  " only when viewing it in that context.<br><br>"
                  "You probably only want to select multiple schedules if this is a"
                  " public page that's shared between all schedules (like the privacy page).<br><br>"
                  "You can't set this individually on child pages, set it once on the top"
                  " level page and it will be applied to all the children automatically.<br><br>"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overridden save to ensure that all sub_pages are in the same
        schedules as their parent.
        """

        # Don't allow sub pages to be in different schedules to their parent
        if self.parent_page:
            self.schedules.set(self.parent_page.schedules.all())

        super(Page, self).save(*args, **kwargs)

        # Cascade any changes to a parent down to it's children
        if bool(self.sub_pages.all()):
            for sub_page in self.sub_pages.all():
                sub_page.schedules.set(self.schedules.all())
                # Set doesn't call save hooks, so trigger it manually
                # to trigger this cascading down any hierarchy
                sub_page.save()
