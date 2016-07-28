from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import transaction

from conference.models import Attendee, Speaker


class Command(BaseCommand):
    """
    This command creates a speaker profile for each of the attendees given,
    copying their details across.
    """

    help = "Generate Speaker profiles from the supplied Attendees in --slugs."

    def add_arguments(self, parser):
        parser.add_argument('--slugs', nargs='+', required=True, type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        attendees = Attendee.objects.filter(slug__in=options['slugs'])
        for attendee in attendees:
            speaker = Speaker.objects.create(
                user=attendee.user,
                name=attendee.name,
                slug=attendee.slug,
                twitter_username=attendee.twitter_username,
                title=attendee.title,
                organisation=attendee.organisation,
                biography=attendee.biography
            )

            if attendee.photo:
                speaker.photo = File(open(attendee.photo.path, 'rb'))
                speaker.save()
