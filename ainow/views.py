from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


class RSVPView(TemplateView):
    template_name = 'rsvp.html'


class PrivacyView(TemplateView):
    template_name = 'privacy.html'
