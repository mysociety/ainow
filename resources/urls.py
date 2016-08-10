from django.conf.urls import url

from .views import CategoryListView

urlpatterns = [
    url(r'^resources$', CategoryListView.as_view(), name='resources'),
]
