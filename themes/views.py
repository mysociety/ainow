from django.views.generic import ListView

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
