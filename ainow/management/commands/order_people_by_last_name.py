from django.core.management.base import BaseCommand
from django.db import transaction

from conference.models import Attendee, Speaker, Organiser, StandingCommittee


class Command(BaseCommand):
    """
    This orders people by last name based on spliting the name field
    """

    help = "Select which type of person you want to sort: --organiser, --attendee, --speaker or --all"

    def add_arguments(self, parser):
        parser.add_argument('--organisers', action='store_true', default=False)
        parser.add_argument('--speakers', action='store_true', default=False)
        parser.add_argument('--attendees', action='store_true', default=False)
        parser.add_argument('--standing', action='store_true', default=False)
        parser.add_argument('--all', action='store_true', default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        if options['organisers'] or options['all']:
            people = Organiser.objects.all()
            self.sort_people(people)
        if options['speakers'] or options['all']:
            people = Speaker.objects.all()
            self.sort_people(people)
        if options['attendees'] or options['all']:
            people = Attendee.objects.all()
            self.sort_people(people)
        if options['standing'] or options['all']:
            people = StandingCommittee.objects.all()
            self.sort_people(people)

    def sort_people(self, people):
        sorted_list = sorted(people, key=lambda k: ', '.join(k.name.rsplit(' ', 1)[::-1]))
        order = 0
        for person in sorted_list:
            person.sort_order = order
            person.save()
            order += 1
