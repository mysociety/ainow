from django.db import models
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField
from markitup.fields import MarkupField
from autoslug import AutoSlugField

from ainow.models import TimestampedModel


def person_photo_upload_to(instance, filename):
    return "conference_{}_photos/{}".format(instance.__class__.__name__.lower(), filename)


# This is abstract because we have two very similar types of people (speakers
# and attendees) who we want to use the same set of fields for but keep
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
    biography = MarkupField(blank=True)
    photo = ImageField(upload_to=person_photo_upload_to, blank=True)
    twitter_username = models.CharField(max_length=15, blank=True)
    website = models.URLField(max_length=1024, blank=True)
    facebook = models.URLField(max_length=1024, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Speaker(Person):
    pass


class Attendee(Person):
    schedule = models.ForeignKey('Schedule', blank=True, null=True)


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

    def __str__(self):
        return self.name


class Room(TimestampedModel):
    name = models.CharField(max_length=1024)
    location = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Slot(TimestampedModel):
    COFFEE_BREAK = 'COFFEE'
    LUNCH_BREAK = 'LUNCH'
    KEYNOTE = 'KEYNOTE'
    WORKSHOP = 'WORKSHOP'
    TALK = 'TALK'
    KIND_CHOICES = (
        (COFFEE_BREAK, 'Coffee break'),
        (LUNCH_BREAK, 'Lunch break'),
        (KEYNOTE, 'Keynote'),
        (WORKSHOP, 'Workshop'),
        (TALK, 'Talk'),
    )
    # Slot kinds that can have presentations attached
    PRESENTATION_KINDS = (KEYNOTE, WORKSHOP, TALK)

    name = models.CharField(
        max_length=1024,
        help_text='Only shown to admins, something to help you identify this '
                  'slot in other forms.',
        blank=True
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
        return "{} slot ({} - {}) in {}".format(self.name, self.start, self.end, self.room)

    @property
    def is_presentation_slot(self):
        return self.kind in self.PRESENTATION_KINDS


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
    short_description = models.TextField()
    slot = models.OneToOneField(
        'Slot',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='presentation'
    )

    def __str__(self):
        return self.title

    def slug_field(self):
        return 'title'
