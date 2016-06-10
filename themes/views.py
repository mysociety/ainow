from django.views.generic import DetailView, ListView

from conference.views import ScheduleMixin

from .models import Theme


class ThemeListView(ScheduleMixin, ListView):
    model = Theme
    context_object_name = 'themes'

    def get_queryset(self):
        """
        Filter all the themes by the selected schedule
        """
        return Theme.objects.filter(schedules=self.schedule)


class ThemeView(ScheduleMixin, DetailView):
    model = Theme
    context_object_name = 'theme'

    def get_context_data(self, **kwargs):
        context = super(ThemeView, self).get_context_data(**kwargs)
        context['documents'] = context['theme'].documents.all()
        return context

    def get_queryset(self):
        """
        Themes can have multiple schedules so we have to alter the
        queryset a little bit from ScheduleMixin.
        """
        return Theme.objects.filter(schedules=self.schedule)


