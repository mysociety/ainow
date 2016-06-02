from django.db import models

from markitup.fields import MarkupField

from ainow.models import SluggedModel


class FAQPage(SluggedModel):
    name = models.CharField(
        max_length=1024,
        help_text='An internal name for this page, to help identify it.',
        blank=True
    )
    title = models.CharField(max_length=1024)
    introduction = MarkupField(blank=True)

    def __str__(self):
        return self.name


class FAQQuestion(SluggedModel):
    question = models.CharField(max_length=1024)
    answer = MarkupField()
    pages = models.ManyToManyField(
        'FAQPage',
        blank=True,
        related_name='questions'
    )

    def __str__(self):
        return self.question
