from django.views.generic import ListView

from conference.models import Schedule

from .models import Category


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context["schedule"] = Schedule.objects.get(slug="conference")
        return context
