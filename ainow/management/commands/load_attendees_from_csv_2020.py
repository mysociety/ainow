from argparse import FileType
import uuid

import unicodecsv as csv

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from account.models import EmailAddress

from conference.models import Attendee, Schedule


class Command(BaseCommand):
    """
    This command takes a path to a CSV file and loads in a set of users from
    it, creating accounts and Attendee profiles for each of them.
    """

    help = "Create users from the supplied CSV, with accounts and attendee profiles to match."

    def add_arguments(self, parser):
        parser.add_argument('csv', type=FileType('r'))
        parser.add_argument('schedule')

    def handle(self, *args, **options):
        User = get_user_model()
        reader = csv.DictReader(options['csv'])
        schedule = Schedule.objects.get(slug=options['schedule'])
        for row in reader:
            name = ' '.join([row['First Name'].strip(), row['Surname'].strip()])
            organisation = row.get('Organisation', '').strip()
            title = row.get('Job Title', '').strip()
            try:
                attendee, created = Attendee.objects.get_or_create(
                    name=name,
                    organisation=organisation,
                    title=title,
                )
                if created:
                    self.stdout.write(u"Created {}\n".format(attendee))
                else:
                    self.stdout.write(u"Found   {}\n".format(attendee))
            except:
                print row
                print [a.user for a in Attendee.objects.filter(
                    name=name,
                    organisation=organisation,
                    title=title,
                ) if a.user]

            attendee.schedules.add(schedule)

            attendee.save()

