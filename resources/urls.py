from django.conf.urls import url

from .views import CategoryListView, CategoryView

urlpatterns = [
    url(r'^resources/(?P<slug>[-\w]+)$', CategoryView.as_view(), name='category'),
    url(r'^resources$', CategoryListView.as_view(), name='resources'),
]
