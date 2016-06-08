from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.shortcuts import get_object_or_404, redirect

from account.mixins import LoginRequiredMixin

from .models import Schedule, Speaker, Presentation, Attendee


class ScheduleMixin(object):
    """
    A view mixin to retrieve the related schedule for other views,
    force logins for private schedules and objects related to
    private schedules, and automatically filter objects to those
    related to the given schedule.
    """

    # Override this if your url uses a different kwarg name for
    # the schedule's slug
    schedule_slug_kwarg = 'schedule_slug'

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden dispatch so that self.schedule is available
        throughout the whole method chain of any view.
        """
        self.schedule = get_object_or_404(
            Schedule,
            slug=kwargs.get(self.schedule_slug_kwarg)
        )
        self.check_schedule_access()
        return super(ScheduleMixin, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Overridden get_queryset to filter the models down to those
        that are related to this schedule.
        """
        return super(ScheduleMixin, self).get_queryset().filter(schedule=self.schedule)

    def get_context_data(self, **kwargs):
        context = super(ScheduleMixin, self).get_context_data(**kwargs)
        context['schedule'] = self.schedule
        return context

    def check_schedule_access(self):
        if self.schedule.private and not request.user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class ScheduleView(DetailView):
    model = Schedule
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context['slots'] = context['schedule'].slots.order_by('start')
        return context


class SpeakerListView(ScheduleMixin, ListView):
    model = Speaker
    context_object_name = 'speakers'

    def get_queryset(self):
        """
        Speakers are linked to a schedule by their presentation's slot.
        """
        return Speaker.objects.filter(presentations__slot__schedule=self.schedule)


class PresentationView(ScheduleMixin, DetailView):
    model = Presentation
    context_object_name = 'presentation'

    def get_queryset(self):
        """
        Presentations are linked to a schedule by their slot.
        """
        return Presentation.objects.filter(slot__schedule=self.schedule)


class AttendeeListView(ScheduleMixin, ListView):
    model = Attendee
    context_object_name = 'attendees'


class AttendeeCreateUpdateView(LoginRequiredMixin,
                                                       SingleObjectTemplateResponseMixin,
                                                       ModelFormMixin,
                                                       ProcessFormView):
    """A combined create and update view for Attendees"""
    # Taken from http://stackoverflow.com/a/30948175
    model = Attendee
    context_object_name = 'attendee'
    template_name = 'conference/attendee_profile_form.html'
    fields = ['user', 'name', 'biography', 'photo', 'twitter_username', 'website', 'facebook', 'schedule']
    success_url = '/profile/'  # Come back to this page

    def dispatch(self, request, *args, **kwargs):
        self.schedule = Schedule.objects.get(slug='workshop')
        return super(AttendeeCreateUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return self.request.user.conference_attendee_profile
        except AttributeError:
            return None

    def get_initial(self):
        initial = super(AttendeeCreateUpdateView, self).get_initial()
        initial['user'] = self.request.user
        initial['schedule'] = self.schedule
        return initial

    def get_form_kwargs(self):
        # Force the submitted user to be request.user and the schedule to be
        # our chosen Schedule
        kwargs = super(AttendeeCreateUpdateView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['data']['user'] = self.request.user.id
            kwargs['data']['schedule'] = self.schedule.id
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AttendeeCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AttendeeCreateUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AttendeeCreateUpdateView, self).get_context_data(*kwargs)
        context['schedule'] = self.schedule
        return context
