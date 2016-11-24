from django.views.generic import TemplateView
from django.conf import settings
from django.utils import timezone

from conference.models import Schedule, LiveStream
from blocks.models import Block
from themes.models import Theme
from resources.models import Document


class HomeView(TemplateView):
    template_name = 'theme/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['is_homepage'] = True
        context['intro_block'] = Block.objects.get(slug='homepage-introduction').content
        context['tickets_block'] = Block.objects.get(slug='homepage-tickets').content
        context['tickets_button_tagline'] = Block.objects.get(slug='homepage-tickets-button-tagline').content

        # We have to pass a schedule in for the footer links to use
        # TODO: Stop the madness.
        context['schedule'] = Schedule.objects.get(slug=settings.CONFERENCE_DEFAULT_SCHEDULE)

        context['themes'] = Theme.objects.exclude(primer='')
        try:
            context['summary_document'] = Document.objects.get(name='Summary Report and Recommendations')
        except Document.DoesNotExist:
            pass

        # Get the current datetime in CONFERENCE_TIMEZONE
        with timezone.override(settings.CONFERENCE_TIMEZONE):
            now = timezone.localtime(timezone.now())
        if now.date() < settings.CONFERENCE_START.date():
            # Before the day of the conference we don't want to show any livestream stuff
            context['pre_conference'] = True
        elif now.date() >= settings.CONFERENCE_START.date() and now < settings.CONFERENCE_END:
            # Whilst the conference is running, show the livestream
            context['show_livestream'] = True
            try:
                context['livestream'] = LiveStream.objects.get(live=True)
            except LiveStream.DoesNotExist:
                context['livestream'] = None
        else:
            # Conference has finished, so immediately hide livestream and other pre-conference bits (e.g. ticket links)
            context['post_conference'] = True
            context['post_conference_block'] = Block.objects.get(slug='homepage-post-stream').content
        return context
