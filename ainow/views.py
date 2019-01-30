from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.conf import settings
from django.utils import timezone

import account.forms
import account.views

from conference.models import Schedule, LiveStream, Presentation
from blocks.models import Block
from themes.models import Theme
from resources.models import Document

from forms import SignupForm


class HomeView(TemplateView):
    template_name = 'ainow/index.html'

    def get_context_data(self, **kwargs):

        context = super(HomeView, self).get_context_data(**kwargs)

        context['schedule'] = Schedule.objects.get(slug=settings.CONFERENCE_DEFAULT_SCHEDULE)

        context['intro_block'] = Block.objects.get(slug='homepage-introduction').content
        context['tickets_block'] = Block.objects.get(slug='homepage-tickets').content
        context['testimonials_block'] = Block.objects.get(slug='homepage-testimonials').content
        context['call_block'] = Block.objects.get(slug='homepage-call-for-papers').content
        context['venue_block'] = Block.objects.get(slug='homepage-venue').content
        context['florence_block'] = Block.objects.get(slug='homepage-about-florence').content
        context['inspired_block'] = Block.objects.get(slug='homepage-get-inspired').content
        context['conduct_block'] = Block.objects.get(slug='homepage-code-of-conduct').content

        # Get the current datetime in CONFERENCE_TIMEZONE
        with timezone.override(settings.CONFERENCE_TIMEZONE):
            now = timezone.localtime(timezone.now())
        if now.date() < settings.CONFERENCE_START.date():
            # Before the day of the conference we don't want to show any livestream stuff
            context['pre_conference'] = True
        else:
            # Conference has finished, so immediately hide livestream and other pre-conference bits (e.g. ticket links)
            context['post_conference'] = True
        return context


class LoginView(account.views.LoginView):
    """ Override account.views.LoginView to use the email-only version """
    form_class = account.forms.LoginEmailForm


class SignupView(account.views.SignupView):
    """ Override account.views.SignupView to use our email-only SignupForm """
    form_class = SignupForm

    def generate_username(self, form):
        # Return the email address as the username (Django's user model needs
        # something to store there).
        return form.cleaned_data['email']


class ConfirmEmailView(account.views.ConfirmEmailView):
    """
    Override account.views.ConfirmEmailView so that it automatically
    confirms the user's account on GET, logs them in immediately and redirects
    them on.
    """

    # Don't allow the inherited post method, just to be clear
    http_method_names = ['get']

    def get(self, *args, **kwargs):
        """
        Does mostly what account.views.ConfirmEmailView.post does, with some
        simplification because we always want to redirect to a specific URL,
        and the addition of logging the user in directly.
        """
        self.object = confirmation = self.get_object()
        confirmation.confirm()
        self.after_confirmation(confirmation)
        self.login_user(user=confirmation.email_address.user)
        if self.messages.get("email_confirmed"):
            messages.add_message(
                self.request,
                self.messages["email_confirmed"]["level"],
                self.messages["email_confirmed"]["text"].format(**{
                    "email": confirmation.email_address.email
                })
            )
        return redirect(settings.LOGIN_REDIRECT_URL)

    def login_user(self, user):
        """
        Automatically log a user in without knowing their password
        (otherwise you could just use authenticate() followed by login()).
        """
        if user is not None and not user.is_superuser:
            # This what authenticate() does that login() needs
            user.backend = 'account.auth_backends.EmailAuthenticationBackend'
            login(self.request, user)

    def get_queryset(self):
        """
        Alter the queryset returned by
        account.views.ConfirmEmailView.get_queryset so that it only looks in
        unconfirmed EmailConfirmations, to avoid double-confirming.
        """
        qs = super(ConfirmEmailView, self).get_queryset()
        return qs.filter(email_address__verified=False)

    def get_object(self, queryset=None):
        """
        Add an extra check on the object returned by
        account.views.ConfirmEmailView.get_object in order to check that the
        confirmation key hasn't expired.
        """
        obj = super(ConfirmEmailView, self).get_object(queryset)
        if obj.key_expired():
            raise Http404()
        return obj


class PrivacyView(TemplateView):
    template_name = 'ainow/privacy.html'


class PressView(TemplateView):
    template_name = 'ainow/press.html'
