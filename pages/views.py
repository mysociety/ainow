from django.views.generic import DetailView

from conference.views import ScheduleMixin

from .models import Page


class PageView(ScheduleMixin, DetailView):
    model = Page
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context['sub_pages'] = context['page'].sub_pages.all()
        context['parent_page'] = context['page'].parent_page
        return context
