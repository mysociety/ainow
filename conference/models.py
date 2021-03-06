from django.db import models
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField
from markitup.fields import MarkupField
from autoslug import AutoSlugField

from ainow.models import TimestampedModel

import urllib
import urlparse
import json


def person_photo_upload_to(instance, filename):
    return "conference_{}_photos/{}".format(instance.__class__.__name__.lower(), filename)


# This is abstract because we have two very similar types of people (speakers
# and attendees) who we want to use a similar set of fields for but keep
# separate in the database
class Person(TimestampedModel):
    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_profile"
    )
    name = models.CharField(max_length=1024)
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=True,
        populate_from='name',
        help_text="Used to make a nice url for the page that displays this person."
    )
    photo = ImageField(
        upload_to=person_photo_upload_to,
        blank=True,
        help_text="Photos must be at least 500px by 500px."
        )
    twitter_username = models.CharField(max_length=15, blank=True)
    title = models.CharField(max_length=1024, blank=True)
    organisation = models.CharField(max_length=1024, blank=True)
    sort_order = models.IntegerField(
        default=0,
        blank=True,
        help_text="Order in which the person will appear in a list."
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        """
        Overridden save to ensure that twitter_username is stripped of any @.
        """
        self.twitter_username = self.twitter_username.lstrip('@')
        super(Person, self).save(*args, **kwargs)


class Speaker(Person):
    # We provide a bit more info about speakers
    biography = MarkupField(blank=True)
    website = models.URLField(max_length=1024, blank=True)


class OrganiserType(TimestampedModel):
    # Organisers can come in many flavours
    name = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.name


class Organiser(Person):
    # Organisers are people too, but they have an OrganiserType
    organiser_type = models.ManyToManyField('OrganiserType')
    website = models.URLField(max_length=1024, blank=True)


class Attendee(Person):
    schedules = models.ManyToManyField('Schedule', blank=True)
    external_id = models.IntegerField(blank=True, null=True)
    biography = models.TextField(
        max_length=1500,
        blank=True,
        help_text="Maximum 250 words."
    )


class StandingCommittee(Person):
    website = models.URLField(max_length=1024, blank=True)


class Schedule(TimestampedModel):
    name = models.CharField(max_length=1024)
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=True,
        populate_from='name',
        help_text="Used to make a nice url for the page that displays this schedule."
    )
    private = models.BooleanField(
        default=False,
        help_text="Is this schedule for a private event?"
                  "<br>If this box is checked, this schedule and"
                  " anything connected to it will force you to log"
                  " in to view it.")
    introduction = MarkupField(
        blank=True,
        help_text="The text that's shown at the top of the schedule, before the slots."
    )

    def __unicode__(self):
        return self.name


class Room(TimestampedModel):
    name = models.CharField(max_length=1024)
    location = models.TextField(blank=True)
    order = models.IntegerField(null=True, help_text='Use to override the default (alphabetical) order of rooms.')

    def __unicode__(self):
        return self.name


# A Slot exists purely to provide a Session with a time in which it happens
class Slot(TimestampedModel):

    start = models.DateTimeField()
    end = models.DateTimeField()
    schedule = models.ForeignKey(
        'Schedule',
        null=True,
        blank=True,
        related_name='slots'
    )

    def __unicode__(self):
        return u"{} - {}".format(self.start.strftime('%a %d/%m/%Y %H:%M'), self.end.strftime('%a %d/%m/%Y %H:%M'))

    class Meta:
        ordering = ['start']


# A Session is when something actually happens.
class Session(TimestampedModel):
    KEYNOTE = 'KEYNOTE'
    TALK = 'TALK'
    OTHER = 'OTHER'
    KIND_CHOICES = (
        (KEYNOTE, 'Keynote'),
        (TALK, 'Talk'),
        (OTHER, 'Other'),
    )
    # Slot kinds that can have presentations attached
    PRESENTATION_KINDS = (TALK,)

    name = models.CharField(
        max_length=1024,
        help_text='This will be shown to the user for this session if no'
                  ' presentations are associated with it instead.',
    )
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=True,
        populate_from='name',
        help_text="Used to make a nice url for the page that displays this session."
    )
    short_description = MarkupField(
        blank=True,
        help_text='Extra text to display under this session\'s name in the '
                  ' schedule. Useful if you need a description but don\'t'
                  ' want to associate a whole presentation with it.'
    )
    kind = models.CharField(max_length=100, choices=KIND_CHOICES)
    slot = models.ForeignKey(
        'Slot',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )
    room = models.ForeignKey(
        'Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )

    def __unicode__(self):
        return u"{}: {} ({} in {})".format(self.slot.schedule.name, self.name, self.slot, self.room)

    @property
    def is_presentation_slot(self):
        return self.kind in self.PRESENTATION_KINDS

    @property
    def has_presentation_links(self):
        return self.presentations.exclude(youtube_link__exact='').count() > 1

    class Meta:
        ordering = ['slot__start', 'room__order', 'room__name']


class Presentation(TimestampedModel):
    title = models.CharField(max_length=1024)
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=True,
        populate_from='title',
        help_text="Used to make a nice url for the page that displays this presentation."
    )
    speakers = models.ManyToManyField(
        'Speaker',
        related_name="presentations"
    )
    short_description = MarkupField(
        blank=True
    )
    long_description = MarkupField(
        blank=True
    )
    session = models.ForeignKey(
        'Session',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='presentations'
    )
    youtube_link = models.URLField(
        blank=True,
        max_length=1024,
        help_text='The url for the presentation\'s video on YouTube.<br>'
                  'We can extract everything we need to embed it from that.'
    )

    youtube_embed_html = models.TextField(
        blank=True,
        editable=False
    )

    slideshare_link = models.URLField(
        blank=True,
        max_length=1024,
        help_text='The url for the presentation\'s slides on SlideShare.<br>'
                  'We can extract everything we need to embed it from that.'
    )

    slideshare_embed_html = models.TextField(
        blank=True,
        editable=False
    )

    prezi_link = models.URLField(
        blank=True,
        max_length=1024,
        help_text='The url for the presentation on Prezi.<br>'
                  'We can extract everything we need to embed it from that.'
    )

    order = models.IntegerField(
        default=0,
        help_text='Use to override the order in which presentations appear within a slot. Lower numbers appear first.'
    )

    @property
    def video_id(self):
        return self.youtube_link.split("?v=")[1]

    @property
    def video_thumbnail_url(self):
        return "https://img.youtube.com/vi/{0}/0.jpg".format(self.video_id)

    def __unicode__(self):
        return self.title

    def slug_field(self):
        return 'title'

    class Meta:
        ordering = ['order', 'session__slot__start', 'session__room__name']

    def save(self, *args, **kwargs):

        if self.youtube_link:

            url = 'https://www.youtube.com/oembed?url={}&format=json&maxwidth=700'.format(self.youtube_link)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            html = data['html']
            qs = urlparse.parse_qs(urlparse.urlparse(self.youtube_link)[4])
            if 'start' in qs:
                html = html.replace('feature=oembed', 'feature=oembed&amp;start=' + qs['start'][0])
            self.youtube_embed_html = html

        else:
            self.youtube_embed_html = ''

        if self.slideshare_link:

            url = 'https://www.slideshare.net/api/oembed/2?url={}&format=json&maxwidth=700'.format(self.slideshare_link)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            self.slideshare_embed_html = data['html']

        else:
            self.slideshare_embed_html = ''

        super(Presentation, self).save(*args, **kwargs)


class LiveStream(TimestampedModel):
    name = models.CharField(
        max_length=1024,
        help_text='An internal name for this stream, to help you recognise it'
    )
    youtube_link = models.URLField(
        max_length=1024,
        help_text='The url for the live stream\'s page on YouTube.<br>'
                  'We can extract everything we need to embed it from that.'
    )
    live = models.BooleanField(
        default=False,
        help_text='Is this stream live now?<br>'
                  'Tick the box to make it appear on the homepage.<br>'
                  'Note: this will replace any stream that\'s currently live.'
    )

    def __unicode__(self):
        return self.name

    @property
    def video_id(self):
        return self.youtube_link.split("?v=")[1]

    def save(self, *args, **kwargs):
        """
        Overridden save to ensure that only one stream is live.
        """
        if self.live:
            LiveStream.objects.filter(
                live=True
            ).exclude(id=self.id).update(live=False)
        super(LiveStream, self).save(*args, **kwargs)
