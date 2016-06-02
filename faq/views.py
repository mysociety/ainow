from django.views.generic import DetailView

from .models import FAQPage


class FAQPageView(DetailView):
    model = FAQPage
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super(FAQPageView, self).get_context_data(**kwargs)
        context['questions'] = context['page'].questions.all()
        return context
