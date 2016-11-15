from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import transaction

from conference.models import Organiser, StandingCommittee


class Command(BaseCommand):
    """
    This command copies across details from Organisers to the StandingCommittee.
    """

    help = "Generate StandingCommittee profiles from the supplied Organisers in --slugs."

    def add_arguments(self, parser):
        parser.add_argument('--slugs', nargs='+', required=True, type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        organisers = Organiser.objects.filter(slug__in=options['slugs'])
        for organiser in organisers:
            member = StandingCommittee.objects.create(
                user=organiser.user,
                name=organiser.name,
                slug=organiser.slug,
                twitter_username=organiser.twitter_username,
                title=organiser.title,
                organisation=organiser.organisation,
                sort_order=organiser.sort_order,
            )

            if organiser.photo:
                member.photo = File(open(organiser.photo.path, 'rb'))
                member.save()
