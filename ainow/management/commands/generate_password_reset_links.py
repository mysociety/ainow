from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.http import int_to_base36
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from account.views import PasswordResetView


class Command(BaseCommand):
    """
    This command creates a password reset token for each of the
    non-staff users in the database and prints it out as a CSV.
    """

    help = "Generate password reset links for every non-staff user as a CSV."

    def handle(self, *args, **options):
        User = get_user_model()
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(1)

        self.stdout.write("Email, Reset Link")
        for user in User.objects.filter(is_active=True, is_staff=False, is_superuser=False):
            # Most of this is just lifted/adapted from django-user-accounts' PasswordResetView
            # https://github.com/pinax/django-user-accounts/blob/ca45e17425dbe8d2b24a377ec165c727c7b2f02d/account/views.py#L537
            uid = int_to_base36(user.id)
            token = default_token_generator.make_token(user)
            password_reset_url = "{0}://{1}{2}".format(
                protocol,
                current_site.domain,
                reverse("account_password_reset_token", kwargs=dict(uidb36=uid, token=token))
            )
            self.stdout.write("{0},{1}".format(user.email, password_reset_url))

