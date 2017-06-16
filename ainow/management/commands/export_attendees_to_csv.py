from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from conference.models import Attendee

class Command(BaseCommand):
    """
    This command generates a CSV of data about attendees to be
    run once attendees have filled out all their profile information
    """

    help = "Generate a CSV of every active Attendee."

    def add_arguments(self, parser):
        parser.add_argument('schedule_id', default=2, type=int)

    def handle(self, *args, **options):
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(1)

        self.stdout.write("Name,Email,Title,Organisation,Bio,Three Words,Photo")

        if options['schedule_id']:
            attendees = Attendee.objects.filter(schedule_id=options['schedule_id'])
        else:
            attendees = Attendee.objects.all()
        for attendee in attendees.order_by('external_id'):
            if attendee.photo:
                photo_url = "https://artificialintelligencenow.com" + attendee.photo.url
            else:
                photo_url = ""
            seq = (
                attendee.name,
                attendee.user.email,
                attendee.title,
                attendee.organisation,
                attendee.biography,
                attendee.three_words,
                photo_url
            )
            self.stdout.write(','.join(seq))
