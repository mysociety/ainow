from django.views.generic import DetailView, ListView

from .models import Schedule, Speaker


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
