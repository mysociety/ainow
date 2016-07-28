from django.db import models
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField
from markitup.fields import MarkupField
from autoslug import AutoSlugField

from ainow.models import TimestampedModel


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

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name

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


class Attendee(Person):
    schedule = models.ForeignKey('Schedule', blank=True, null=True)
    external_id = models.IntegerField(blank=True, null=True)
    biography = models.TextField(
        max_length=1500,
        blank=True,
        help_text="Maximum 250 words."
    )


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

    def __str__(self):
        return self.name


class Room(TimestampedModel):
    name = models.CharField(max_length=1024)
    location = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Slot(TimestampedModel):
    TALK = 'TALK'
    OTHER = 'OTHER'
    KIND_CHOICES = (
        (TALK, 'Talk'),
        (OTHER, 'Other'),
    )
    # Slot kinds that can have presentations attached
    PRESENTATION_KINDS = (TALK,)

    name = models.CharField(
        max_length=1024,
        help_text='Text that will be shown to the user for this slot if no'
                  ' presentation is associated with it instead.',
        blank=True
    )
    short_description = MarkupField(
        blank=True,
        help_text='Extra text to display under this slot\'s name in the '
                  ' schedule. Useful if you need a description but don\'t'
                  ' want to associate a whole presentation with it.'
    )
    start = models.TimeField()
    end = models.TimeField()
    kind = models.CharField(max_length=100, choices=KIND_CHOICES)
    schedule = models.ForeignKey(
        'Schedule',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='slots'
    )
    room = models.ForeignKey(
        'Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='slots'
    )

    def __str__(self):
        return "{}: {} slot ({} - {}) in {}".format(self.schedule.name, self.name, self.start, self.end, self.room)

    @property
    def is_presentation_slot(self):
        return self.kind in self.PRESENTATION_KINDS

    class Meta:
        ordering = ['start']


class Presentation(TimestampedModel):
    title = models.CharField(max_length=1024)
    slug = AutoSlugField(
        db_index=True,
        unique=True,
        editable=True,
        populate_from='title',
        help_text="Used to make a nice url for the page that displays this presentation."
    )
    primary_speaker = models.ForeignKey(
        'Speaker',
        related_name="presentations"
    )
    additional_speakers = models.ManyToManyField(
        'Speaker',
        related_name="additional_presentations",
        blank=True
    )
    long_description = MarkupField()
    short_description = MarkupField()
    slot = models.OneToOneField(
        'Slot',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='presentation'
    )
    youtube_link = models.URLField(
        blank=True,
        max_length=1024,
        help_text='The url for the presentation\'s video on YouTube.<br>'
                  'We can extract everything we need to embed it from that.'
    )
    schedule = models.ForeignKey(
        'Schedule',
        blank=True,
        null=True,
        help_text='If this presentation isn\'t associated with a slot in a '
                  'schedule directly, but needs to be visible in that '
                  'schedule, e.g. a lightning talk, set the schedule here'
    )

    @property
    def video_id(self):
        return self.youtube_link.split("?v=")[1]

    def __str__(self):
        return self.title

    def slug_field(self):
        return 'title'


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

    def __str__(self):
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
