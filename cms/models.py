from __future__ import unicode_literals

import datetime

from django.db import models
from conference.models import Schedule

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, BaseChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock

class HomePage(Page):
    parent_page_types = []

    mission = RichTextField(blank=True)
    features = StreamField([
        ('feature', blocks.StructBlock(
            [
                ('heading', blocks.CharBlock(required=True)),
                ('text', blocks.RichTextBlock()),
                ('links', blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ('text', blocks.CharBlock(required=True)),
                            ('page', blocks.PageChooserBlock()),
                        ],
                        template='cms/blocks/link.html',
                    )
                ))
            ],
            template='cms/blocks/feature.html',
            icon='doc-full'
        ))
    ])
    themes = StreamField(
        [
            ('heading', blocks.CharBlock(
                icon='title'
            )),
            ('theme', blocks.StructBlock(
                [
                    ('heading', blocks.CharBlock(required=True)),
                    ('text', blocks.RichTextBlock()),
                ],
                icon='doc-full'
            ))
        ],
        default=[],
    )

    content_panels = Page.content_panels + [
        FieldPanel('mission', classname="full"),
        StreamFieldPanel('features'),
        StreamFieldPanel('themes'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['latest_research'] = Research.objects.live()[0]
        return context

class SimplePage(Page):
    parent_page_types = ['cms.HomePage']

    name = models.CharField(
        max_length=1024,
        help_text='An internal name for this page, to help identify it.',
        blank=True
    )
    body = RichTextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('body', classname="full"),
    ]

class PersonIndexPage(Page):
    parent_page_types = []

class Person(Page):
    parent_page_types = ['cms.PersonIndexPage']

    position = models.CharField(max_length=1024, blank=True)
    organisation = models.CharField(max_length=1024, blank=True)
    twitter = models.CharField(max_length=15, blank=True)
    body = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('position'),
        FieldPanel('organisation'),
        FieldPanel('twitter'),
        FieldPanel('body', classname="full"),
        ImageChooserPanel('image'),
    ]

class ResearchIndexPage(Page):
    parent_page_types = []

class Research(Page):
    parent_page_types = ['cms.ResearchIndexPage']

    excerpt = RichTextField(blank=True)
    intro = RichTextField(blank=True)
    research_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    external_link = models.URLField("External link", blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('excerpt', classname="full"),
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('image'),
        DocumentChooserPanel('research_file'),
        FieldPanel('external_link')
    ]

class EventsIndexPage(Page):
    parent_page_types = []

    def get_context(self, request):
        context = super(EventsIndexPage, self).get_context(request)
        context['upcoming_events'] = Events.objects.filter(start__gte=datetime.datetime.now())
        context['previous_events'] = Events.objects.filter(start__lte=datetime.datetime.now())
        return context

class Events(Page):
    parent_page_types = ['cms.EventsIndexPage']

    body = RichTextField()
    start = models.DateTimeField("Start date/time")
    end = models.DateTimeField("End date/time")
    location = models.CharField(max_length=1024, blank=True)
    schedule = models.ForeignKey(
        'conference.Schedule',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('start'),
        FieldPanel('end'),
        FieldPanel('location'),
        FieldPanel('schedule')
    ]
