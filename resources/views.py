from django.views.generic import ListView, DetailView

from conference.models import Schedule

from .models import Category


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context["schedule"] = Schedule.objects.get(slug="2016")
        context["is_resources"] = True
        return context


class CategoryView(DetailView):
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context["is_resources"] = True
        return context
