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

    def handle(self, *args, **options):
        User = get_user_model()
        reader = csv.DictReader(options['csv'])
        for row in reader:
            if row['Email']:
                first_name = row['First Name'].strip()
                last_name = row['Last Name'].strip()
                username = slugify("{0}_{1}".format(first_name, last_name))
                username.replace('-', '_')
                # Just in case there are two people with the same name
                n = 1
                while User.objects.filter(username=username).exists():
                    username = "{0}_{1}".format(username, n)
                    n = n + 1
                email = row['Email'].strip()
                # We never need to know the password, just make it long and random
                password = uuid.uuid4()

                # Create the user object - this'll trigger creating an Account
                # and the related EmailAddress object too.
                user = User.objects.create_user(
                    username,
                    email,
                    password,
                    first_name=first_name,
                    last_name=last_name
                )

                # Confirm the email address so that they can log into their
                # account after they reset the password
                email_address = EmailAddress.objects.get(user=user, email=email)
                email_address.verified = True
                email_address.save()

                # Create a basic Attendee profile for them too
                organisation = row.get('Affiliation', '').strip()
                external_id = row.get('ID Number', '').strip()
                if (not external_id):
                    external_id = None
                Attendee.objects.create(
                    user=user,
                    name=user.get_full_name(),
                    organisation=organisation,
                    schedule=Schedule.objects.get(slug='workshop'),
                    external_id=external_id
                )
            else:
                name = "{0} {1}".format(row.get('First Name'), row.get('Last Name'))
                msg = "Skipping {0} because they don't have an email address".format(name)
                self.stdout.write(msg)
