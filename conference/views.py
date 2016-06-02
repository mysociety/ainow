from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from account.mixins import LoginRequiredMixin

from .models import Schedule, Speaker, Presentation, Attendee


class ScheduleView(DetailView):
    model = Schedule
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context['slots'] = context['schedule'].slots.order_by('start')
        return context


class SpeakerListView(ListView):
    model = Speaker
    context_object_name = 'speakers'


class PresentationView(DetailView):
    model = Presentation
    context_object_name = 'presentation'


class AttendeeListView(ListView):
    model = Attendee
    context_object_name = 'attendees'


class SpeakerCreateUpdateView(LoginRequiredMixin,
                              SingleObjectTemplateResponseMixin,
                              ModelFormMixin,
                              ProcessFormView):
    """A combined create and update view for Speakers"""
    # Taken from http://stackoverflow.com/a/30948175
    model = Speaker
    context_object_name = 'speaker'
    template_name = 'conference/speaker_profile_form.html'
    fields = ['user', 'name', 'biography', 'photo', 'twitter_username', 'website', 'facebook']
    success_url = '/profile/'  # Come back to this page

    def get_object(self, queryset=None):
        try:
            return self.request.user.conference_speaker_profile
        except AttributeError:
            return None

    def get_initial(self):
        initial = super(SpeakerCreateUpdateView, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def get_form_kwargs(self):
        # Force the submitted user to be request.user
        kwargs = super(SpeakerCreateUpdateView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['data']['user'] = self.request.user.id
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SpeakerCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SpeakerCreateUpdateView, self).post(request, *args, **kwargs)
