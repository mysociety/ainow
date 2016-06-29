from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.http import int_to_base36
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from conference.models import Attendee


class Command(BaseCommand):
    """
    This command creates a password reset token for each of the active
    Attendees in the database and prints it out as a CSV.
    """

    help = "Generate password reset links for every active Attendee as a CSV."

    def add_arguments(self, parser):
        parser.add_argument('--pks', nargs='+', required=False, type=int)

    def handle(self, *args, **options):
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(1)

        self.stdout.write("ID Number,Email,Reset Link")

        if options['pks']:
            attendees = Attendee.objects.filter(id__in=options['pks'])
        else:
            attendees = Attendee.objects.all()
        for attendee in attendees.order_by('external_id'):
            user = attendee.user
            if user and user.is_active and not user.is_staff:
                # Most of this is just lifted/adapted from django-user-accounts' PasswordResetView
                # https://github.com/pinax/django-user-accounts/blob/ca45e17425dbe8d2b24a377ec165c727c7b2f02d/account/views.py#L537
                uid = int_to_base36(user.id)
                token = default_token_generator.make_token(user)
                password_reset_url = "{0}://{1}{2}".format(
                    protocol,
                    current_site.domain,
                    reverse("account_password_reset_token", kwargs=dict(uidb36=uid, token=token))
                )
                self.stdout.write("{0},{1},{2}".format(attendee.external_id, user.email, password_reset_url))
